"""
Canonical Frozen Strategy Contracts — CAND-024 + CAND-035

ARCHITECTURE:
  FrozenStrategyContract  → executable semantics only (hash input)
  HistoricalEvidence      → research results (NOT in hash)
  EnvironmentMapping      → broker/runtime (NOT in hash)

A change to historical performance must never change strategy identity.
A change to broker must never change strategy identity.
Only a change to executable semantics may change the canonical contract hash.

Ratified: 2026-08-27
"""

import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


# ---------------------------------------------------------------------------
# Canonical Serialization
# ---------------------------------------------------------------------------
# Algorithm:
#   1. Take ONLY Category A executable fields (FrozenStrategyContract as dict)
#   2. Canonical JSON: json.dumps(data, sort_keys=True, separators=(',', ':'))
#   3. UTF-8 encode
#   4. SHA-256
#   5. Full hex digest stored; first 8 chars used as short display hash
#
# Properties:
#   - Deterministic (same input → same hash, every run)
#   - Order-stable (sort_keys)
#   - Whitespace-stable (separators eliminate extra spaces)
#   - Environment-independent (no broker/server/mapping fields)
#   - Evidence-independent (no historical statistics)
# ---------------------------------------------------------------------------

HASH_ALGORITHM = "SHA-256"
HASH_TRUNCATION = 8  # short display hash length


def _canonical_hash(executable_fields: Dict[str, Any]) -> str:
    """Compute canonical SHA-256 hash from executable fields only."""
    canonical = json.dumps(executable_fields, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


# ---------------------------------------------------------------------------
# FrozenStrategyContract — Category A executable semantics only
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FrozenStrategyContract:
    """
    Immutable strategy contract containing ONLY executable semantic fields.

    Fields:
      candidate_id     — identity
      version          — contract version (for compatibility)
      name             — human-readable identity
      instrument       — what is traded
      timezone         — session time reference
      preconditions    — state conditions for event qualification
      trigger          — exact time/event that fires entry
      direction        — Long or Short
      entry            — how the position is opened
      exit             — how/when the position is closed
      rearm_rule       — duplicate prevention / cooldown
      session_boundaries — required tracking windows
    """
    candidate_id: str
    version: str
    name: str
    instrument: str
    timezone: str
    preconditions: tuple  # tuple for immutability
    trigger: str
    direction: str
    entry: str
    exit: str
    rearm_rule: str
    session_boundaries: dict  # frozen via __post_init__ check

    def __post_init__(self):
        # Validate required fields are non-empty
        for f in ['candidate_id', 'name', 'instrument', 'timezone',
                   'trigger', 'direction', 'entry', 'exit', 'rearm_rule']:
            val = getattr(self, f)
            if not val or (isinstance(val, str) and not val.strip()):
                raise ValueError(f"Required field '{f}' is empty")
        if not self.preconditions or len(self.preconditions) == 0:
            raise ValueError("At least one precondition is required")

    def to_executable_dict(self) -> Dict[str, Any]:
        """Return dict of ONLY executable fields (hash input).

        NOTE: version is excluded — it is governance metadata, not executable
        semantics. A version bump does not change what the machine does.
        """
        return {
            "candidate_id": self.candidate_id,
            "name": self.name,
            "instrument": self.instrument,
            "timezone": self.timezone,
            "preconditions": list(self.preconditions),
            "trigger": self.trigger,
            "direction": self.direction,
            "entry": self.entry,
            "exit": self.exit,
            "rearm_rule": self.rearm_rule,
            "session_boundaries": dict(self.session_boundaries),
        }

    @property
    def hash(self) -> str:
        """Full SHA-256 canonical hash."""
        return _canonical_hash(self.to_executable_dict())

    @property
    def short_hash(self) -> str:
        """First 8 chars of canonical hash (display only)."""
        return self.hash[:HASH_TRUNCATION]

    @property
    def identity(self) -> str:
        """Canonical contract identity string."""
        return f"{self.candidate_id}:CANONICAL:{self.short_hash}"

    def verify_hash(self, expected_hash: str) -> bool:
        """Verify this contract's hash matches an expected value."""
        return self.hash == expected_hash


# ---------------------------------------------------------------------------
# HistoricalEvidence — Category C research results (NOT in hash)
# ---------------------------------------------------------------------------

@dataclass
class HistoricalEvidence:
    """
    Research results. These must NOT be part of strategy identity.

    A change to these fields must never change the canonical contract hash.
    """
    candidate_id: str
    historical_n: int
    historical_frequency: float  # events per year
    historical_mean_net: str     # e.g. "+40.59 bps"
    historical_median_net: str   # e.g. "+34.00 bps"
    scientific_status: str       # e.g. "Qualified"
    friction_assumption: str     # e.g. "2.0 index points round-trip"
    mechanism_family: str        # e.g. "D — Session Mechanics"
    data_required: str           # e.g. "USATECHIDXUSD (M5/H1/D1)"
    counterfactual: str = ""
    economic_plausibility: str = ""
    failure_mode: str = ""


# ---------------------------------------------------------------------------
# EnvironmentMapping — Category B broker/runtime (NOT in hash)
# ---------------------------------------------------------------------------

@dataclass
class EnvironmentMapping:
    """
    Broker and runtime representation. Separate from strategy identity.

    A change to these fields must never change the canonical contract hash.
    """
    logical_symbol: str     # e.g. "USATECHIDXUSD"
    broker_symbol: str      # e.g. "USTECm"
    broker: str             # e.g. "Exness Technologies Ltd"
    server: str             # e.g. "Exness-MT5Trial15"
    mapping_id: str         # e.g. "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0"


# ---------------------------------------------------------------------------
# CAND-024 — Canonical Ratified Contract
# Source: TRADEABLE_EDGE_DISCOVERY_SCREENING_V8.md lines 119–146
# ---------------------------------------------------------------------------

CAND_024_CONTRACT = FrozenStrategyContract(
    candidate_id="CAND-024",
    version="1.0",
    name="Friday De-Risking Conditioned by Morning Exhaustion",
    instrument="USATECHIDXUSD",
    timezone="America/New_York",
    preconditions=(
        "The High between 08:00 and 12:00 exceeds the Weekly High (prior to Friday)",
        "The 12:00 open price is LOWER than the 08:00 open price (Morning Exhaustion State)",
    ),
    trigger="Friday 12:00:00 EST open",
    direction="Short",
    entry="Market order at 12:00:00 EST open",
    exit="15:45:00 EST open",
    rearm_rule="Maximum one event per week",
    session_boundaries={
        "morning_tracking_start": "08:00:00 EST",
        "morning_tracking_end": "12:00:00 EST",
        "trigger_time": "12:00:00 EST",
        "exit_time": "15:45:00 EST",
    },
)

CAND_024_EVIDENCE = HistoricalEvidence(
    candidate_id="CAND-024",
    historical_n=13,
    historical_frequency=4.55,
    historical_mean_net="+40.59 bps",
    historical_median_net="+34.00 bps",
    scientific_status="Qualified",
    friction_assumption="2.0 index points round-trip",
    mechanism_family="D — Session Mechanics",
    data_required="USATECHIDXUSD (M5/H1/D1)",
    counterfactual="Failed standalone promotion purely on frequency",
    economic_plausibility="Positional de-risking when buyers are explicitly exhausted",
    failure_mode="Very low opportunity frequency or algorithmic dip-buying",
)


# ---------------------------------------------------------------------------
# CAND-035 — Canonical Ratified Contract
# Source: TRADEABLE_EDGE_DISCOVERY_SCREENING_V12.md lines 29–48
# ---------------------------------------------------------------------------

CAND_035_CONTRACT = FrozenStrategyContract(
    candidate_id="CAND-035",
    version="1.0",
    name="Month-End Final-Hour Imbalance Acceleration",
    instrument="USATECHIDXUSD",
    timezone="America/New_York",
    preconditions=(
        "Last trading day of the month",
        "USATECHIDXUSD 15:00 ET price is > 09:30 ET open (Up Day)",
    ),
    trigger="Last trading day of month at 15:00 ET",
    direction="Long",
    entry="15:00 ET (Market)",
    exit="16:00 ET (Market close)",
    rearm_rule="1 event per month maximum. No overlap.",
    session_boundaries={
        "reference_open": "09:30 ET",
        "trigger_time": "15:00 ET",
        "exit_time": "16:00 ET",
    },
)

CAND_035_EVIDENCE = HistoricalEvidence(
    candidate_id="CAND-035",
    historical_n=11,
    historical_frequency=4.09,
    historical_mean_net="+62.36 bps",
    historical_median_net="+55.92 bps",
    scientific_status="Qualified",
    friction_assumption="2.0 index points round-trip",
    mechanism_family="B — Forced Flow / Scheduled Mechanics",
    data_required="M1 USATECHIDXUSD",
    counterfactual="Same NY session return on 15th of month (mid-month day)",
    economic_plausibility="Forced price-insensitive structural flow at month-end",
    failure_mode="Benchmark tracking flow absent or trend not established by 15:00",
)


# ---------------------------------------------------------------------------
# Environment Mapping (separate governed object)
# ---------------------------------------------------------------------------

USATECHIDXUSD_USTECM_MAPPING = EnvironmentMapping(
    logical_symbol="USATECHIDXUSD",
    broker_symbol="USTECm",
    broker="Exness Technologies Ltd",
    server="Exness-MT5Trial15",
    mapping_id="MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0",
)


# ---------------------------------------------------------------------------
# Legacy compatibility — engines import these names
# ---------------------------------------------------------------------------

# For backward compatibility with engine files that do:
#   from contracts import CAND_024_CONTRACT, CAND_035_CONTRACT
# The new FrozenStrategyContract is the contract object.
# Engines reference: self.contract.hash, self.contract.candidate_id, etc.
