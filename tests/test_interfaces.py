"""Regression validation for the frozen QuantForge decision-layer contracts."""

import unittest
from pathlib import Path
import sys
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from strategy.adaptive_strategy_engine import AdaptiveStrategyEngine
from strategy.risk_engine import RiskEngine
from strategy.signal_generator import SignalGenerator


class TestDecisionLayerInterfaces(unittest.TestCase):
    """Verifies the producer/consumer contracts in INTERFACES.md and TradePlan.md."""

    def setUp(self) -> None:
        self.adaptive_engine = AdaptiveStrategyEngine(
            str(PROJECT_ROOT / "config" / "adaptive_rules.json")
        )
        self.signal_generator = SignalGenerator()
        self.risk_engine = RiskEngine()
        self.dna_profile = {
            "dataset_information": {"instrument": "EURUSD"},
            "volatility_profile": {"coefficient_of_variation": 0.9},
            "atr_profile": {"mean": 0.0001},
            "trend_persistence": {"average_trend_length": 1.8},
            "pullback_statistics": {"mean": 0.0002},
            "expansion_statistics": {
                "size": {"mean": 0.00015},
                "duration_steps": {"mean": 2.0},
            },
            "candle_structure": {
                "body_size": {"p95": 0.001, "p99": 0.002},
            },
            "intraday_activity": [{"hour": 15, "average_body": 0.0002}],
        }
        self.market_data = {
            "timestamp": "2026-07-16 15:00:00",
            "open": 1.1000,
            "high": 1.1020,
            "low": 1.0995,
            "close": 1.1015,
        }
        self.account = {
            "balance": 10000.0,
            "equity": 10000.0,
            "daily_loss_percent": 0.0,
            "drawdown_percent": 0.0,
            "open_positions": 0,
            "consecutive_losses": 0,
        }

    def _adaptive_strategy(self) -> Dict[str, Any]:
        return self.adaptive_engine.analyze_profile(self.dna_profile)

    @staticmethod
    def _contract_strategy() -> Dict[str, Any]:
        """A valid Interface 4 fixture for isolated downstream contract checks."""
        return {
            "strategy_class": "mean_reversion",
            "holding_style": "intraday",
            "risk_profile": "Low",
            "confidence": 0.83,
            "reason": ["Fixture strategy conforms to Interface 4"],
        }

    def _signal(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        return self.signal_generator.generate_signal(
            strategy, self.market_data, self.dna_profile
        )

    def _assert_required_keys(
        self, output: Dict[str, Any], required_keys: set[str]
    ) -> None:
        self.assertTrue(
            required_keys.issubset(output),
            f"Missing required contract keys: {sorted(required_keys.difference(output))}",
        )

    def test_adaptive_strategy_interface(self) -> None:
        """Adaptive Strategy must produce the INTERFACES.md contract exactly."""
        strategy = self._adaptive_strategy()
        required_keys = {
            "strategy_class",
            "holding_style",
            "risk_profile",
            "confidence",
            "reason",
        }
        self._assert_required_keys(strategy, required_keys)
        self.assertIsInstance(strategy["strategy_class"], str)
        self.assertIsInstance(strategy["holding_style"], str)
        self.assertIsInstance(strategy["risk_profile"], str)
        self.assertIsInstance(strategy["confidence"], float)
        self.assertIsInstance(strategy["reason"], list)
        self.assertGreaterEqual(strategy["confidence"], 0.0)
        self.assertLessEqual(strategy["confidence"], 1.0)

    def test_signal_generator_interface(self) -> None:
        """Signal Generator must produce the INTERFACES.md signal contract."""
        signal = self._signal(self._contract_strategy())
        required_keys = {"signal", "signal_strength", "confidence", "reason"}
        self._assert_required_keys(signal, required_keys)
        self.assertIn(signal["signal"], {"BUY", "SELL", "NO_TRADE"})
        self.assertIsInstance(signal["signal_strength"], float)
        self.assertGreaterEqual(signal["signal_strength"], 0.0)
        self.assertLessEqual(signal["signal_strength"], 1.0)
        self.assertIsInstance(signal["confidence"], float)
        self.assertGreaterEqual(signal["confidence"], 0.0)
        self.assertLessEqual(signal["confidence"], 1.0)
        self.assertIsInstance(signal["reason"], list)

    def test_risk_engine_tradeplan_interface(self) -> None:
        """Risk Engine must produce the frozen TradePlan v1.0 top-level schema."""
        strategy = self._contract_strategy()
        signal = self._signal(strategy)
        trade_plan = self.risk_engine.create_trade_plan(strategy, signal, self.account)
        required_keys = {
            "schema_version",
            "plan_id",
            "timestamp",
            "instrument",
            "timeframe",
            "direction",
            "trade_allowed",
            "strategy",
            "signal",
            "risk",
            "execution",
            "validation",
            "decision_trace",
            "metadata",
        }
        self._assert_required_keys(trade_plan, required_keys)
        for key in {
            "strategy",
            "signal",
            "risk",
            "execution",
            "validation",
            "decision_trace",
            "metadata",
        }:
            self.assertIsInstance(trade_plan[key], dict)
        self.assertIsInstance(trade_plan["trade_allowed"], bool)

    def test_pipeline_compatibility(self) -> None:
        """Each decision-layer producer output must be accepted by its consumer."""
        strategy = self._adaptive_strategy()
        signal = self._signal(strategy)
        trade_plan = self.risk_engine.create_trade_plan(strategy, signal, self.account)
        self.assertIsInstance(trade_plan, dict)
        self.assertIn("schema_version", trade_plan)

    def test_schema_regression_required_keys(self) -> None:
        """Required-key checks fail immediately if a frozen contract field changes."""
        strategy = self._adaptive_strategy()
        self._assert_required_keys(
            strategy,
            {"strategy_class", "holding_style", "risk_profile", "confidence", "reason"},
        )
        signal = self._signal(self._contract_strategy())
        self._assert_required_keys(
            signal, {"signal", "signal_strength", "confidence", "reason"}
        )


if __name__ == "__main__":
    print("================================================")
    print("QUANTFORGE INTERFACE VALIDATION")
    print("================================================")
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        print("Adaptive Strategy\nPASS")
        print("Signal Generator\nPASS")
        print("Risk Engine\nPASS")
        print("Pipeline\nPASS")
        print("TradePlan\nPASS")
        print("================================================")
        print("INTERFACE VALIDATION PASSED")
