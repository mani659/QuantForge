"""
QuantForge Signal Generator (v1.0.0)
Converts adaptive strategy recommendations and market DNA profiles into deterministic trading signals.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger("QuantForge.SignalGenerator")


class SignalGenerator:
    """
    SignalGenerator translates strategic decisions from the Adaptive Strategy Engine 
    and the statistical boundaries from the DNA Profiler into executable entry signals.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = {
            "default_trigger_quantile": "p95",
            "extreme_trigger_quantile": "p99",
            "min_confidence_threshold": 0.40
        }
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str) -> None:
        """Loads externalized configuration thresholds."""
        try:
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
            logger.info(f"SignalGenerator configuration loaded successfully from {config_path}")
        except Exception as e:
            logger.error(f"Failed to load config from {config_path}: {e}")
            raise

    def generate_signal(self, 
                        adaptive_strategy: Dict[str, Any], 
                        market_data: Dict[str, Any], 
                        dna_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a deterministic signal (BUY, SELL, NO_TRADE) using market DNA statistics.
        """
        # Validate inputs
        self._validate_inputs(adaptive_strategy, market_data, dna_profile)

        # Extract strategy recommendation
        strategy_class = adaptive_strategy.get("strategy_class", "recoil").lower()
        strategy_confidence = adaptive_strategy.get("confidence", 0.5)

        # Calculate latest bar metrics
        open_px = market_data["open"]
        high_px = market_data["high"]
        low_px = market_data["low"]
        close_px = market_data["close"]
        
        body_size = abs(close_px - open_px)
        is_bullish = close_px > open_px
        is_bearish = close_px < open_px

        # Extract thresholds from Market DNA Profile
        candle_structure = dna_profile.get("candle_structure", {})
        body_stats = candle_structure.get("body_size", {})
        
        p95_threshold = body_stats.get(self.config["default_trigger_quantile"], 0.0)
        p99_threshold = body_stats.get(self.config["extreme_trigger_quantile"], 0.0)

        if p95_threshold == 0.0 or p99_threshold == 0.0:
            raise ValueError("Invalid DNA profile structure: Missing body_size quantile thresholds.")

        signal = "NO_TRADE"
        signal_strength = 0.0
        confidence = 0.0
        trigger_reason = "No expansion detected"

        # 1. Deterministic Entry Detection (Expansion Check)
        if body_size >= p95_threshold:
            # Calculate expansion ratio
            expansion_ratio = body_size / p95_threshold
            signal_strength = min(1.0, 0.5 + ((body_size - p95_threshold) / (p99_threshold - p95_threshold)) * 0.4)
            
            # 2. Strategy-Aware Signal Logic
            if strategy_class in ["recoil", "mean_reversion"]:
                # Bullish expansion triggers SELL recoil; Bearish expansion triggers BUY recoil
                if is_bullish:
                    signal = "SELL"
                    trigger_reason = f"Bullish expansion ({body_size:.4f}) exceeded p95 recoil limit ({p95_threshold:.4f})"
                elif is_bearish:
                    signal = "BUY"
                    trigger_reason = f"Bearish expansion ({body_size:.4f}) exceeded p95 recoil limit ({p95_threshold:.4f})"
            
            elif strategy_class in ["momentum", "breakout"]:
                # Bullish expansion triggers BUY breakout; Bearish expansion triggers SELL breakout
                if is_bullish:
                    signal = "BUY"
                    trigger_reason = f"Bullish momentum breakout ({body_size:.4f}) confirmed above p95 ({p95_threshold:.4f})"
                elif is_bearish:
                    signal = "SELL"
                    trigger_reason = f"Bearish momentum breakout ({body_size:.4f}) confirmed above p95 ({p95_threshold:.4f})"

            # 3. Confidence Scoring with Intraday Activity Confluence
            confidence = self._calculate_confidence(
                base_confidence=strategy_confidence,
                signal_strength=signal_strength,
                market_data=market_data,
                dna_profile=dna_profile,
                body_size=body_size
            )

        # Safeguard: enforce confidence thresholds
        if confidence < self.config["min_confidence_threshold"]:
            signal = "NO_TRADE"
            trigger_reason += f" (Suppressed: confidence {confidence:.2f} below threshold {self.config['min_confidence_threshold']})"

        return {
            "signal": signal,
            "signal_strength": round(signal_strength, 4),
            "confidence": round(confidence, 4),
            "reason": [trigger_reason],
            "timestamp": market_data["timestamp"],
            "strategy_used": strategy_class,
            "metadata": {
                "trigger_reason": trigger_reason,
                "body_size": round(body_size, 4),
                "dna_p95_threshold": round(p95_threshold, 4),
                "dna_p99_threshold": round(p99_threshold, 4)
            }
        }

    def _calculate_confidence(self, 
                              base_confidence: float, 
                              signal_strength: float, 
                              market_data: Dict[str, Any], 
                              dna_profile: Dict[str, Any], 
                              body_size: float) -> float:
        """Calculates dynamic confidence by matching intraday statistical anomalies."""
        confidence = base_confidence * 0.6 + signal_strength * 0.4
        
        # Confluence Check: Intraday activity statistical validation
        try:
            dt = datetime.strptime(market_data["timestamp"], "%Y-%m-%d %H:%M:%S")
            hour = dt.hour
            intraday_data = dna_profile.get("intraday_activity", [])
            
            for hourly_stat in intraday_data:
                if hourly_stat.get("hour") == hour:
                    avg_body_for_hour = hourly_stat.get("average_body", 1.0)
                    # If the candle is at least 3x larger than average for this hour, increase confidence
                    if body_size >= (avg_body_for_hour * 3):
                        confidence = min(1.0, confidence * 1.15)
                    break
        except Exception as e:
            logger.warning(f"Could not parse hourly confluence data: {e}")
            
        return confidence

    def _validate_inputs(self, 
                         adaptive_strategy: Dict[str, Any], 
                         market_data: Dict[str, Any], 
                         dna_profile: Dict[str, Any]) -> None:
        """Strict validation of the incoming dictionaries to preserve deterministic output."""
        required_strategy = ["strategy_class", "confidence"]
        required_market = ["timestamp", "open", "high", "low", "close"]
        required_dna = ["candle_structure", "intraday_activity"]

        for k in required_strategy:
            if k not in adaptive_strategy:
                raise ValueError(f"Missing required adaptive strategy parameter: '{k}'")
        for k in required_market:
            if k not in market_data:
                raise ValueError(f"Missing required market data parameter: '{k}'")
        for k in required_dna:
            if k not in dna_profile:
                raise ValueError(f"Missing required DNA profile field: '{k}'")
