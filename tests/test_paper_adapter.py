import unittest
from types import MappingProxyType
from datetime import datetime

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.execution import (
    PaperTradingAdapter,
    PaperTradingAdapterConfig,
    ExecutionResult,
    ExecutionStatus,
    InvalidPaperExecution,
    PaperConfigurationError
)
from boe.risk.specification import PositionSpecification

class TestPaperAdapter(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"env": "test"})
        self.config = PaperTradingAdapterConfig(
            broker_name="PaperBroker",
            metadata=self.metadata
        )
        self.spec_open = PositionSpecification(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=0.5,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )
        self.spec_close = PositionSpecification(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=0.0,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )
        self.spec_reverse = PositionSpecification(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="o_1",
            schema_version="1.0",
            position_size_multiplier=1.0,
            exposure_fraction=-0.5,
            risk_units=1.0,
            metadata=self.metadata,
            timestamp=self.dt
        )
        self.snap_100 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="s_100",
            instrument="EURUSD",
            timeframe="M1",
            source="test",
            market_state=MappingProxyType({"close": 100.0}),
            timestamp=self.dt
        )
        self.snap_110 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="s_110",
            instrument="EURUSD",
            timeframe="M1",
            source="test",
            market_state=MappingProxyType({"close": 110.0}),
            timestamp=self.dt
        )
        self.snap_90 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="s_90",
            instrument="EURUSD",
            timeframe="M1",
            source="test",
            market_state=MappingProxyType({"close": 90.0}),
            timestamp=self.dt
        )

    def test_opening_trades(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        
        result = adapter.dispatch(self.spec_open)
        
        self.assertIsInstance(result, ExecutionResult)
        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertEqual(result.metadata["leg_0_action"], "BUY")
        self.assertEqual(result.metadata["leg_0_volume"], 500.0) # (100k * 0.5) / 100 = 500
        self.assertEqual(adapter.account.open_positions["c_1"]["volume"], 500.0)
        self.assertEqual(adapter.account.open_positions["c_1"]["direction"], "BUY")
        self.assertEqual(len(adapter.account.closed_positions), 0)

    def test_closing_trades(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        adapter.dispatch(self.spec_open) # Open 500
        
        adapter.update_market_state(self.snap_110)
        result = adapter.dispatch(self.spec_close) # Close to 0.0
        
        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertEqual(result.metadata["leg_0_action"], "CLOSE")
        self.assertNotIn("c_1", adapter.account.open_positions)
        self.assertEqual(len(adapter.account.closed_positions), 1)
        self.assertEqual(adapter.account.closed_positions[0]["volume"], 500.0)
        # PnL = (110 - 100) * 500 = 5000
        self.assertEqual(adapter.account.closed_positions[0]["pnl"], 5000.0)
        self.assertEqual(adapter.account.realised_pnl, 5000.0)
        self.assertEqual(adapter.account.balance, 105000.0)

    def test_paper_account_updates_reversal(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        adapter.dispatch(self.spec_open) # BUY 500 @ 100
        
        adapter.update_market_state(self.snap_110)
        adapter.dispatch(self.spec_reverse) # Reverses to SELL 0.5 -> 105000 * 0.5 / 110 = 477.27
        
        # PnL realized = (110-100)*500 = 5000. Balance is now 105000.
        self.assertEqual(adapter.account.realised_pnl, 5000.0)
        self.assertEqual(adapter.account.balance, 105000.0)
        
        # New volume = (105000 * 0.5) / 110 = 477.2727...
        new_vol = (105000.0 * 0.5) / 110.0
        self.assertAlmostEqual(adapter.account.open_positions["c_1"]["volume"], new_vol)
        self.assertEqual(adapter.account.open_positions["c_1"]["direction"], "SELL")

    def test_immutable_execution_result_and_deterministic_replay(self):
        adapter1 = PaperTradingAdapter(self.config)
        result1 = adapter1.dispatch(self.spec_open)
        
        adapter2 = PaperTradingAdapter(self.config)
        result2 = adapter2.dispatch(self.spec_open)
        
        self.assertEqual(result1, result2)
        self.assertEqual(hash(result1), hash(result2))

    def test_invalid_execution(self):
        adapter = PaperTradingAdapter(self.config)
        
        with self.assertRaises(InvalidPaperExecution):
            adapter.dispatch({"invalid": "request"}) # type: ignore

    def test_configuration_validation(self):
        with self.assertRaises(PaperConfigurationError):
            PaperTradingAdapter("BadConfig") # type: ignore

    def test_paper_adapter_market_price_sync(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_110)
        self.assertEqual(adapter.account.current_price, 110.0)

    def test_paper_adapter_partial_close_realized_pnl(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        adapter.dispatch(self.spec_open) # BUY 500 @ 100
        
        adapter.update_market_state(self.snap_110)
        spec_partial = PositionSpecification(
            candidate_id="c_1", timeline_id="t_1", observation_id="o_1",
            schema_version="1.0", position_size_multiplier=1.0,
            exposure_fraction=0.25, risk_units=1.0,
            metadata=self.metadata, timestamp=self.dt
        )
        adapter.dispatch(spec_partial) # Reduce to 0.25
        
        # Original exposure was 0.5 (volume 500). Target exposure is 0.25.
        # But wait! Target volume is based on CURRENT equity (100k balance + 5000 unrealized = 105k)
        # Target volume = (105000 * 0.25) / 110 = 238.636...
        # Closed volume = 500 - 238.636 = 261.36...
        target_vol = (105000.0 * 0.25) / 110.0
        closed_vol = 500.0 - target_vol
        
        expected_pnl = (110.0 - 100.0) * closed_vol
        
        self.assertAlmostEqual(adapter.account.realised_pnl, expected_pnl)
        self.assertAlmostEqual(adapter.account.open_positions["c_1"]["volume"], target_vol)

    def test_paper_adapter_pnl_signs(self):
        # Test SELL profit
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_110)
        spec_sell = PositionSpecification(
            candidate_id="c_2", timeline_id="t_1", observation_id="o_1",
            schema_version="1.0", position_size_multiplier=1.0,
            exposure_fraction=-0.5, risk_units=1.0,
            metadata=self.metadata, timestamp=self.dt
        )
        adapter.dispatch(spec_sell) # SELL at 110
        # Volume = (100000 * 0.5) / 110 = 454.5454
        sell_vol = (100000 * 0.5) / 110.0
        
        adapter.update_market_state(self.snap_90)
        spec_close2 = PositionSpecification(
            candidate_id="c_2", timeline_id="t_1", observation_id="o_1",
            schema_version="1.0", position_size_multiplier=1.0,
            exposure_fraction=0.0, risk_units=1.0,
            metadata=self.metadata, timestamp=self.dt
        )
        adapter.dispatch(spec_close2) # CLOSE at 90
        # PnL = (110 - 90) * vol
        expected_pnl = 20.0 * sell_vol
        self.assertAlmostEqual(adapter.account.realised_pnl, expected_pnl)

    def test_full_close_metadata(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        adapter.dispatch(self.spec_open) # BUY 500 @ 100
        
        adapter.update_market_state(self.snap_110)
        result = adapter.dispatch(self.spec_close) # CLOSE @ 110
        
        self.assertEqual(result.metadata["leg_count"], 1)
        self.assertEqual(result.metadata["leg_0_action"], "CLOSE")
        self.assertEqual(result.metadata["leg_0_direction"], "BUY")
        self.assertEqual(result.metadata["leg_0_volume"], 500.0)
        self.assertEqual(result.metadata["leg_0_price"], 110.0)
        self.assertEqual(result.metadata["leg_0_realized_pnl"], 5000.0)

    def test_partial_close_metadata(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        adapter.dispatch(self.spec_open) # BUY 500 @ 100
        
        adapter.update_market_state(self.snap_110)
        spec_partial = PositionSpecification(
            candidate_id="c_1", timeline_id="t_1", observation_id="o_1",
            schema_version="1.0", position_size_multiplier=1.0,
            exposure_fraction=0.25, risk_units=1.0,
            metadata=self.metadata, timestamp=self.dt
        )
        result = adapter.dispatch(spec_partial) # REDUCE @ 110
        
        self.assertEqual(result.metadata["leg_count"], 1)
        self.assertEqual(result.metadata["leg_0_action"], "REDUCE")
        self.assertEqual(result.metadata["leg_0_direction"], "BUY")
        
        target_vol = (105000.0 * 0.25) / 110.0
        closed_vol = 500.0 - target_vol
        expected_pnl = (110.0 - 100.0) * closed_vol
        
        self.assertEqual(result.metadata["leg_0_volume"], closed_vol)
        self.assertEqual(result.metadata["leg_0_price"], 110.0)
        self.assertEqual(result.metadata["leg_0_realized_pnl"], expected_pnl)

    def test_reversal_metadata(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        adapter.dispatch(self.spec_open) # BUY 500 @ 100
        
        adapter.update_market_state(self.snap_110)
        result = adapter.dispatch(self.spec_reverse) # REVERSE to -0.5 @ 110
        
        self.assertEqual(result.metadata["leg_count"], 2)
        
        # Leg 1: CLOSE
        self.assertEqual(result.metadata["leg_0_action"], "CLOSE")
        self.assertEqual(result.metadata["leg_0_direction"], "BUY")
        self.assertEqual(result.metadata["leg_0_volume"], 500.0)
        self.assertEqual(result.metadata["leg_0_price"], 110.0)
        self.assertEqual(result.metadata["leg_0_realized_pnl"], 5000.0)
        
        # Leg 2: SELL
        new_vol = (105000.0 * 0.5) / 110.0
        self.assertEqual(result.metadata["leg_1_action"], "SELL")
        self.assertEqual(result.metadata["leg_1_direction"], "SELL")
        self.assertAlmostEqual(result.metadata["leg_1_volume"], new_vol)
        self.assertEqual(result.metadata["leg_1_price"], 110.0)
        self.assertEqual(result.metadata["leg_1_realized_pnl"], 0.0)

    def test_metadata_pnl_reconstruction(self):
        adapter = PaperTradingAdapter(self.config)
        adapter.update_market_state(self.snap_100)
        res1 = adapter.dispatch(self.spec_open) # BUY
        
        adapter.update_market_state(self.snap_110)
        res2 = adapter.dispatch(self.spec_reverse) # REVERSE
        
        adapter.update_market_state(self.snap_90)
        res3 = adapter.dispatch(self.spec_close) # CLOSE
        
        reconstructed_pnl = 0.0
        for res in [res1, res2, res3]:
            for i in range(res.metadata["leg_count"]):
                reconstructed_pnl += res.metadata[f"leg_{i}_realized_pnl"]
                
        # internal PnL
        internal_pnl = adapter.account.realised_pnl
        self.assertAlmostEqual(reconstructed_pnl, internal_pnl)

    def test_five_tick_end_to_end_reconciliation(self):
        adapter = PaperTradingAdapter(self.config)
        exposures = [0.02, 0.04, 0.01, -0.02, 0.00]
        prices = [1.1000, 1.1010, 1.1020, 1.1030, 1.1040]
        
        reconstructed_pnl = 0.0
        
        for price, exposure in zip(prices, exposures):
            snap = EnvironmentSnapshot(
                schema_version="1.0.0", snapshot_id="s", instrument="EURUSD",
                timeframe="M1", source="test", market_state=MappingProxyType({"close": price}),
                timestamp=self.dt
            )
            spec = PositionSpecification(
                candidate_id="c_1", timeline_id="t_1", observation_id="o_1",
                schema_version="1.0", position_size_multiplier=1.0,
                exposure_fraction=exposure, risk_units=1.0,
                metadata=self.metadata, timestamp=self.dt
            )
            
            adapter.update_market_state(snap)
            result = adapter.dispatch(spec)
            
            for i in range(result.metadata["leg_count"]):
                reconstructed_pnl += result.metadata[f"leg_{i}_realized_pnl"]
                
        self.assertAlmostEqual(adapter.account.realised_pnl, 4.545447283891815, places=9)
        self.assertAlmostEqual(reconstructed_pnl, 4.545447283891815, places=9)

if __name__ == '__main__':
    unittest.main()
