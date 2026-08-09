import unittest
from dataclasses import FrozenInstanceError
from boe.strategy.strategy import Strategy
from boe.strategy.strategy_status import StrategyStatus
from boe.strategy.strategy_errors import InvalidStrategyComponentError

def create_valid_strategy(strategy_id="strat-123"):
    return Strategy(
        _strategy_id=strategy_id,
        _name="Mean Reversion X",
        _version="1.0.0",
        _validation_id="val-456",
        _interpretation_model_id="int-789",
        _decision_policy_id="dec-101",
        _risk_policy_id="risk-202",
        _supported_markets=frozenset(["EURUSD", "GBPUSD"]),
        _status=StrategyStatus.READY,
        _created_at=1700000000.0
    )

class TestStrategy(unittest.TestCase):
    def test_strategy_valid_construction(self):
        strat = create_valid_strategy()
        self.assertEqual(strat.strategy_id, "strat-123")
        self.assertEqual(strat.name, "Mean Reversion X")
        self.assertEqual(strat.version, "1.0.0")
        self.assertEqual(strat.validation_id, "val-456")
        self.assertEqual(strat.interpretation_model_id, "int-789")
        self.assertEqual(strat.decision_policy_id, "dec-101")
        self.assertEqual(strat.risk_policy_id, "risk-202")
        self.assertEqual(strat.supported_markets, frozenset(["EURUSD", "GBPUSD"]))
        self.assertEqual(strat.status, StrategyStatus.READY)
        self.assertEqual(strat.created_at, 1700000000.0)

    def test_strategy_immutability(self):
        strat = create_valid_strategy()
        with self.assertRaises(FrozenInstanceError):
            strat._status = StrategyStatus.LIVE

    def test_strategy_invalid_components(self):
        with self.assertRaises(InvalidStrategyComponentError):
            Strategy(
                _strategy_id="",
                _name="Name",
                _version="1.0",
                _validation_id="val-1",
                _interpretation_model_id="int-1",
                _decision_policy_id="dec-1",
                _risk_policy_id="risk-1",
                _supported_markets=frozenset(["EURUSD"]),
                _status=StrategyStatus.DRAFT,
                _created_at=1.0
            )

        with self.assertRaises(InvalidStrategyComponentError):
            Strategy(
                _strategy_id="strat-1",
                _name="Name",
                _version="1.0",
                _validation_id="val-1",
                _interpretation_model_id="int-1",
                _decision_policy_id="dec-1",
                _risk_policy_id="risk-1",
                _supported_markets=set(), # Empty markets
                _status=StrategyStatus.DRAFT,
                _created_at=1.0
            )
            
        with self.assertRaises(InvalidStrategyComponentError):
            Strategy(
                _strategy_id="strat-1",
                _name="Name",
                _version="1.0",
                _validation_id="val-1",
                _interpretation_model_id="int-1",
                _decision_policy_id="dec-1",
                _risk_policy_id="risk-1",
                _supported_markets=frozenset(["EURUSD"]),
                _status="NOT_AN_ENUM", # Invalid enum
                _created_at=1.0
            )

    def test_strategy_equality_and_hashing(self):
        strat1 = create_valid_strategy(strategy_id="strat-1")
        strat2 = create_valid_strategy(strategy_id="strat-1")
        strat3 = create_valid_strategy(strategy_id="strat-2")
        
        self.assertEqual(strat1, strat2)
        self.assertNotEqual(strat1, strat3)
        
        self.assertEqual(hash(strat1), hash(strat2))
        self.assertNotEqual(hash(strat1), hash(strat3))
        
        # Can be used in a set/dict
        strat_set = {strat1, strat2, strat3}
        self.assertEqual(len(strat_set), 2)

if __name__ == '__main__':
    unittest.main()
