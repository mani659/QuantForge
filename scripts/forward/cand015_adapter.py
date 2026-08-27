import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

try:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'research', 'g6_forward'))
    from signal_engine import Cand015SignalEngine
    from cand015_identity import FROZEN_CAND015_IDENTITY
    CAND015_AVAILABLE = True
except Exception:
    CAND015_AVAILABLE = False


class Cand015Adapter:
    def __init__(self, market_data):
        self._market_data = market_data
        self._engine = None
        self._state = "STOPPED"
        self._last_bar_time = None
        self._ticks_received = 0
        self._signals_generated = 0
        self._last_signal = None
        self._init_time = None
        self._broker_symbol = "USTECm"
        self._logical_symbol = "USATECHIDXUSD"

        if not CAND015_AVAILABLE:
            self._state = "UNAVAILABLE"
            return

        try:
            self._engine = Cand015SignalEngine(FROZEN_CAND015_IDENTITY)
            self._state = "INITIALIZED"
        except Exception:
            self._state = "INIT_FAILED"

    def initialize(self) -> bool:
        if self._engine is None:
            return False
        self._init_time = time.time()
        self._state = "ACTIVE"
        return True

    def process_market_data(self, quote: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if self._state not in ("ACTIVE", "INITIALIZED"):
            return None

        if self._engine is None:
            return None

        if quote.get("status") != "DATA_FRESH":
            return None

        bar_result = self._market_data.latest_completed_bar(self._broker_symbol, "M1")

        if bar_result.get("status") != "DATA_FRESH":
            return None

        bar_time = bar_result.get("time")
        if bar_time == self._last_bar_time:
            return None

        self._last_bar_time = bar_time
        self._ticks_received += 1

        if isinstance(bar_time, (int, float)):
            observation_timestamp = datetime.fromtimestamp(bar_time, tz=timezone.utc)
        else:
            observation_timestamp = bar_time

        tick = {
            "symbol": self._logical_symbol,
            "observation_timestamp": observation_timestamp,
            "open": bar_result["open"],
            "high": bar_result["high"],
            "low": bar_result["low"],
            "close": bar_result["close"],
        }

        try:
            signal = self._engine.process_tick(tick)
        except Exception:
            return None

        if signal is not None:
            self._signals_generated += 1
            self._last_signal = signal
            return signal

        return None

    def status(self) -> Dict[str, Any]:
        base = {
            "candidate_id": "CAND-015",
            "engine": "Cand015SignalEngine",
            "architectural_note": "EXTERNAL_PROTECTED",
            "state": self._state,
            "logical_symbol": self._logical_symbol,
            "broker_symbol": self._broker_symbol,
            "ticks_received": self._ticks_received,
            "signals_generated": self._signals_generated,
        }
        if self._last_signal is not None:
            base["last_signal"] = self._last_signal
        if self._init_time is not None:
            base["uptime_seconds"] = round(time.time() - self._init_time, 1)
        return base

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def shutdown(self):
        self._state = "STOPPED"
        self._engine = None
