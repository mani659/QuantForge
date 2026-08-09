import unittest

from strategy.risk_engine import RiskEngine


class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RiskEngine()
        self.strategy = {"risk_profile": "Low", "confidence": 0.83}
        self.signal = {"signal": "BUY", "signal_strength": 0.91, "confidence": 0.88}
        self.account = {
            "balance": 10000,
            "equity": 9950,
            "daily_loss_percent": 0.8,
            "drawdown_percent": 1.5,
            "open_positions": 1,
            "consecutive_losses": 1,
        }

    def test_normal_trade_is_approved(self):
        result = self.engine.create_trade_plan(self.strategy, self.signal, self.account)
        self.assertTrue(result["trade_allowed"])
        self.assertEqual(result["risk_percent"], 0.5)
        self.assertEqual(result["risk_dollars"], 50.0)
        self.assertIn("Trade Approved", result["reason"])

    def test_no_trade_signal_is_rejected(self):
        signal = {**self.signal, "signal": "NO_TRADE"}
        result = self.engine.create_trade_plan(self.strategy, signal, self.account)
        self.assertFalse(result["trade_allowed"])
        self.assertIn("Signal is NO_TRADE", result["reason"])

    def test_daily_loss_limit_is_enforced(self):
        account = {**self.account, "daily_loss_percent": 5.0}
        result = self.engine.create_trade_plan(self.strategy, self.signal, account)
        self.assertFalse(result["trade_allowed"])
        self.assertIn("Maximum daily loss exceeded", result["reason"])

    def test_drawdown_limit_is_enforced(self):
        account = {**self.account, "drawdown_percent": 20.0}
        result = self.engine.create_trade_plan(self.strategy, self.signal, account)
        self.assertFalse(result["trade_allowed"])
        self.assertIn("Maximum drawdown exceeded", result["reason"])

    def test_open_position_limit_is_enforced(self):
        account = {**self.account, "open_positions": 5}
        result = self.engine.create_trade_plan(self.strategy, self.signal, account)
        self.assertFalse(result["trade_allowed"])
        self.assertIn("Maximum open positions reached", result["reason"])

    def test_consecutive_loss_limit_is_enforced(self):
        account = {**self.account, "consecutive_losses": 5}
        result = self.engine.create_trade_plan(self.strategy, self.signal, account)
        self.assertFalse(result["trade_allowed"])
        self.assertIn("Maximum consecutive losses reached", result["reason"])

    def test_low_confidence_signal_is_rejected(self):
        signal = {**self.signal, "confidence": 0.59}
        result = self.engine.create_trade_plan(self.strategy, signal, self.account)
        self.assertFalse(result["trade_allowed"])
        self.assertIn("Signal confidence below threshold", result["reason"])


if __name__ == "__main__":
    unittest.main()
