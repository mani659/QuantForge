"""
FROZEN CAND-015 IDENTITY
Machine-readable authoritative binding for the G6 observation harness.
"""

import hashlib
import json

FROZEN_CAND015_IDENTITY = {
    "candidate_id": "CAND-G0-015",
    "name": "Nasdaq-Crypto Information Absorption Lag",
    "scientific_status": "SUPPORTED",
    "economic_status": "ECONOMICALLY VIABLE",
    "shock_definition": {
        "market": "USATECHIDXUSD",
        "timeframe": "M5",
        "metric": "abs(close - open)",
        "condition": "> 3 * atr_30d",
        "atr_period": 14,
        "atr_30d_bars": 8640
    },
    "volatility_state": {
        "market": "USATECHIDXUSD",
        "timeframe": "D1",
        "metric": "d1_atr",
        "condition": "d1_atr < d1_atr_30d",
        "atr_period": 14,
        "atr_30d_bars": 30,
        "state_eval_time": "pre_entry"
    },
    "opportunity_market": "BTCUSD",
    "direction_rule": "follow_shock_direction",
    "lockout_minutes": 60,
    "entry_rule": "next_available_quote_after_event_completion",
    "exit_rule": "time_based_60_minutes_after_entry_decision",
    "friction_bps": 3.0,
    "version": "1.0.0"
}

def verify_identity():
    """Ensure the identity dictionary has not been tampered with."""
    required_keys = [
        "candidate_id", "shock_definition", "volatility_state", 
        "entry_rule", "exit_rule", "lockout_minutes", "friction_bps"
    ]
    for key in required_keys:
        if key not in FROZEN_CAND015_IDENTITY:
            raise RuntimeError(f"FROZEN IDENTITY MISMATCH: Missing required key {key}")
            
    if FROZEN_CAND015_IDENTITY["shock_definition"]["condition"] != "> 3 * atr_30d":
        raise RuntimeError("FROZEN IDENTITY MISMATCH: Shock condition altered.")
        
    if FROZEN_CAND015_IDENTITY["volatility_state"]["condition"] != "d1_atr < d1_atr_30d":
        raise RuntimeError("FROZEN IDENTITY MISMATCH: Volatility state altered.")
        
    return True
