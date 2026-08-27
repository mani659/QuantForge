import hashlib
import json

class FrozenContract:
    def __init__(self, candidate_id: str, version: str, definition: dict):
        self.candidate_id = candidate_id
        self.version = version
        self.definition = definition
        self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        # Sort keys to ensure deterministic hashing
        contract_str = json.dumps(self.definition, sort_keys=True)
        return hashlib.sha256(contract_str.encode('utf-8')).hexdigest()

    def get_identity(self) -> str:
        return f"{self.candidate_id}:{self.version}:{self.hash[:8]}"

CAND_024_DEF = {
    "name": "Friday Afternoon Positional De-Risking",
    "mechanism_family": "Session / Market-Mechanics Behavior",
    "event_definition": "Friday 12:00 NY time (EST).",
    "preconditions": [
        "The High printed between 08:00 EST and 12:00 EST must exceed the Weekly High (prior to Friday)",
        "12:00 EST open price must be lower than the 08:00 EST open price (Morning Exhaustion State)"
    ],
    "entry": "Market order short on USATECHIDXUSD exactly at 12:00:00 EST open.",
    "exit": "15:45:00 EST open.",
    "direction": "Short",
    "duplicate_rearm_rule": "Maximum one event per week. Re-arms next Friday.",
    "market": "USATECHIDXUSD",
    "session_timezone": "America/New_York",
    "friction_assumption": "2.0 index points round-trip",
    "historical_n": 13,
    "historical_frequency": 4.55,
    "historical_mean_net": "+40.59 bps",
    "historical_median_net": "+34.00 bps",
    "scientific_status": "Qualified"
}

CAND_035_DEF = {
    "name": "Month-End Final-Hour Imbalance Acceleration",
    "mechanism_family": "Forced Flow / Scheduled Mechanics",
    "event_definition": "Last trading day of the month at 15:00 ET.",
    "preconditions": [
        "USATECHIDXUSD 15:00 ET open is > 09:30 ET open (Up Day)"
    ],
    "entry": "Market order long on USATECHIDXUSD exactly at 15:00 ET.",
    "exit": "16:00 ET (Market close).",
    "direction": "Long",
    "duplicate_rearm_rule": "1 event per month maximum. No overlap.",
    "market": "USATECHIDXUSD",
    "session_timezone": "America/New_York",
    "friction_assumption": "2.0 index points round-trip",
    "historical_n": 13,
    "historical_frequency": 4.09,
    "historical_mean_net": "+62.36 bps",
    "historical_median_net": "Positive",
    "scientific_status": "Qualified"
}

CAND_024_CONTRACT = FrozenContract("CAND-024", "1.0", CAND_024_DEF)
CAND_035_CONTRACT = FrozenContract("CAND-035", "1.0", CAND_035_DEF)
