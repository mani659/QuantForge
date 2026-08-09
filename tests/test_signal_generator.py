import unittest
from strategy.signal_generator import SignalGenerator


class TestSignalGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = SignalGenerator()
        
        # Mock DNA profile using realistic values from XAUUSD
        self.mock_dna = {
            "candle_structure": {
                "body_size": {
                    "mean": 0.48,
                    "p95": 1.64,
                    "p99": 3.86
                }
            },
            "intraday_activity": [
                {"hour": 15, "average_body": 0.50}
            ]
        }
        
        # Mock strategy recommendation
        self.mock_strategy_recoil = {
            "strategy_class": "recoil",
            "holding_style": "intraday",
            "confidence": 0.85
        }

    def test_no_expansion_yields_no_trade(self):
        # Normal candle (body size 0.20 < p95 threshold 1.64)
        market_data = {
            "timestamp": "2026-07-15 15:00:00",
            "open": 2400.00,
            "high": 2401.00,
            "low": 2399.50,
            "close": 2400.20,
            "volume": 10.0
        }
        
        result = self.generator.generate_signal(
            self.mock_strategy_recoil, market_data, self.mock_dna
        )
        self.assertEqual(result["signal"], "NO_TRADE")
        self.assertEqual(result["signal_strength"], 0.0)

    def test_bullish_expansion_recoil_yields_sell_signal(self):
        # Bullish extreme candle (body size 2.50 > p95 threshold 1.64)
        market_data = {
            "timestamp": "2026-07-15 15:00:00",
            "open": 2400.00,
            "high": 2403.00,
            "low": 2399.50,
            "close": 2402.50,
            "volume": 10.0
        }
        
        result = self.generator.generate_signal(
            self.mock_strategy_recoil, market_data, self.mock_dna
        )
        self.assertEqual(result["signal"], "SELL")
        self.assertGreater(result["signal_strength"], 0.5)
        self.assertGreater(result["confidence"], 0.6)

    def test_bearish_expansion_recoil_yields_buy_signal(self):
        # Bearish extreme candle (body size 2.50 > p95 threshold 1.64)
        market_data = {
            "timestamp": "2026-07-15 15:00:00",
            "open": 2402.50,
            "high": 2403.00,
            "low": 2399.50,
            "close": 2400.00,
            "volume": 10.0
        }
        
        result = self.generator.generate_signal(
            self.mock_strategy_recoil, market_data, self.mock_dna
        )
        self.assertEqual(result["signal"], "BUY")
        self.assertGreater(result["signal_strength"], 0.5)

    def test_invalid_input_fails_gracefully(self):
        incomplete_market_data = {
            "timestamp": "2026-07-15 15:00:00"
            # Missing pricing fields
        }
        with self.assertRaises(ValueError):
            self.generator.generate_signal(
                self.mock_strategy_recoil, incomplete_market_data, self.mock_dna
            )


if __name__ == "__main__":
    unittest.main()