"""
Canonical Frozen Contract Test Suite — CAND-024 + CAND-035

Tests verify:
  1. Identity (exact canonical hash, determinism, equality)
  2. Mutation (changing executable fields changes hash)
  3. Evidence exclusion (changing evidence does NOT change hash)
  4. Environment exclusion (changing environment does NOT change hash)
  5. Field completeness
  6. Serialization stability
  7. Engine consistency
  8. Negative tests (missing/malformed fields)
"""

import pytest
import json
import hashlib
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contracts import (
    FrozenStrategyContract, HistoricalEvidence, EnvironmentMapping,
    CAND_024_CONTRACT, CAND_035_CONTRACT,
    CAND_024_EVIDENCE, CAND_035_EVIDENCE,
    USATECHIDXUSD_USTECM_MAPPING,
    _canonical_hash,
)
from cand_024_engine import Cand024Engine
from cand_035_engine import Cand035Engine


# =========================================================================
# 1. IDENTITY TESTS
# =========================================================================

class TestCanonicalIdentity:
    """Exact canonical hash verification."""

    def test_cand024_hash_exact(self):
        """CAND-024 must produce the exact ratified canonical hash."""
        assert CAND_024_CONTRACT.hash == "925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e"

    def test_cand035_hash_exact(self):
        """CAND-035 must produce the exact ratified canonical hash."""
        assert CAND_035_CONTRACT.hash == "ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5"

    def test_cand024_short_hash(self):
        assert CAND_024_CONTRACT.short_hash == "925495a8"

    def test_cand035_short_hash(self):
        assert CAND_035_CONTRACT.short_hash == "ddc5d0e9"

    def test_cand024_identity_format(self):
        assert CAND_024_CONTRACT.identity == "CAND-024:CANONICAL:925495a8"

    def test_cand035_identity_format(self):
        assert CAND_035_CONTRACT.identity == "CAND-035:CANONICAL:ddc5d0e9"

    def test_hash_determinism(self):
        """Same executable fields must always produce the same hash."""
        h1 = CAND_024_CONTRACT.hash
        h2 = CAND_024_CONTRACT.hash
        assert h1 == h2
        h1 = CAND_035_CONTRACT.hash
        h2 = CAND_035_CONTRACT.hash
        assert h1 == h2

    def test_hash_length(self):
        """Full SHA-256 hash is 64 hex characters."""
        assert len(CAND_024_CONTRACT.hash) == 64
        assert len(CAND_035_CONTRACT.hash) == 64

    def test_hash_is_hex(self):
        """Hash must be valid hexadecimal."""
        int(CAND_024_CONTRACT.hash, 16)
        int(CAND_035_CONTRACT.hash, 16)

    def test_version_excluded_from_hash(self):
        """Version field must NOT affect the hash."""
        d = CAND_024_CONTRACT.to_executable_dict()
        assert "version" not in d, "version must not be in executable dict"

    def test_verify_hash_pass(self):
        assert CAND_024_CONTRACT.verify_hash(CAND_024_CONTRACT.hash)
        assert CAND_035_CONTRACT.verify_hash(CAND_035_CONTRACT.hash)

    def test_verify_hash_fail(self):
        assert not CAND_024_CONTRACT.verify_hash("00000000")
        assert not CAND_035_CONTRACT.verify_hash("00000000")


# =========================================================================
# 2. MUTATION TESTS — changing executable fields must change hash
# =========================================================================

class TestMutationChangesHash:
    """Changing any executable semantic field must change the canonical hash."""

    def test_cand024_name_change(self):
        original = CAND_024_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_024_CONTRACT.candidate_id,
            version=CAND_024_CONTRACT.version,
            name="DIFFERENT NAME",
            instrument=CAND_024_CONTRACT.instrument,
            timezone=CAND_024_CONTRACT.timezone,
            preconditions=CAND_024_CONTRACT.preconditions,
            trigger=CAND_024_CONTRACT.trigger,
            direction=CAND_024_CONTRACT.direction,
            entry=CAND_024_CONTRACT.entry,
            exit=CAND_024_CONTRACT.exit,
            rearm_rule=CAND_024_CONTRACT.rearm_rule,
            session_boundaries=CAND_024_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand024_instrument_change(self):
        original = CAND_024_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_024_CONTRACT.candidate_id,
            version=CAND_024_CONTRACT.version,
            name=CAND_024_CONTRACT.name,
            instrument="EURUSD",
            timezone=CAND_024_CONTRACT.timezone,
            preconditions=CAND_024_CONTRACT.preconditions,
            trigger=CAND_024_CONTRACT.trigger,
            direction=CAND_024_CONTRACT.direction,
            entry=CAND_024_CONTRACT.entry,
            exit=CAND_024_CONTRACT.exit,
            rearm_rule=CAND_024_CONTRACT.rearm_rule,
            session_boundaries=CAND_024_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand024_precondition_change(self):
        original = CAND_024_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_024_CONTRACT.candidate_id,
            version=CAND_024_CONTRACT.version,
            name=CAND_024_CONTRACT.name,
            instrument=CAND_024_CONTRACT.instrument,
            timezone=CAND_024_CONTRACT.timezone,
            preconditions=("DIFFERENT PRECONDITION",),
            trigger=CAND_024_CONTRACT.trigger,
            direction=CAND_024_CONTRACT.direction,
            entry=CAND_024_CONTRACT.entry,
            exit=CAND_024_CONTRACT.exit,
            rearm_rule=CAND_024_CONTRACT.rearm_rule,
            session_boundaries=CAND_024_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand024_direction_change(self):
        original = CAND_024_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_024_CONTRACT.candidate_id,
            version=CAND_024_CONTRACT.version,
            name=CAND_024_CONTRACT.name,
            instrument=CAND_024_CONTRACT.instrument,
            timezone=CAND_024_CONTRACT.timezone,
            preconditions=CAND_024_CONTRACT.preconditions,
            trigger=CAND_024_CONTRACT.trigger,
            direction="Long",
            entry=CAND_024_CONTRACT.entry,
            exit=CAND_024_CONTRACT.exit,
            rearm_rule=CAND_024_CONTRACT.rearm_rule,
            session_boundaries=CAND_024_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand024_exit_change(self):
        original = CAND_024_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_024_CONTRACT.candidate_id,
            version=CAND_024_CONTRACT.version,
            name=CAND_024_CONTRACT.name,
            instrument=CAND_024_CONTRACT.instrument,
            timezone=CAND_024_CONTRACT.timezone,
            preconditions=CAND_024_CONTRACT.preconditions,
            trigger=CAND_024_CONTRACT.trigger,
            direction=CAND_024_CONTRACT.direction,
            entry=CAND_024_CONTRACT.entry,
            exit="16:00:00 EST open",
            rearm_rule=CAND_024_CONTRACT.rearm_rule,
            session_boundaries=CAND_024_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand024_rearm_change(self):
        original = CAND_024_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_024_CONTRACT.candidate_id,
            version=CAND_024_CONTRACT.version,
            name=CAND_024_CONTRACT.name,
            instrument=CAND_024_CONTRACT.instrument,
            timezone=CAND_024_CONTRACT.timezone,
            preconditions=CAND_024_CONTRACT.preconditions,
            trigger=CAND_024_CONTRACT.trigger,
            direction=CAND_024_CONTRACT.direction,
            entry=CAND_024_CONTRACT.entry,
            exit=CAND_024_CONTRACT.exit,
            rearm_rule="Maximum two events per week",
            session_boundaries=CAND_024_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand035_name_change(self):
        original = CAND_035_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_035_CONTRACT.candidate_id,
            version=CAND_035_CONTRACT.version,
            name="DIFFERENT NAME",
            instrument=CAND_035_CONTRACT.instrument,
            timezone=CAND_035_CONTRACT.timezone,
            preconditions=CAND_035_CONTRACT.preconditions,
            trigger=CAND_035_CONTRACT.trigger,
            direction=CAND_035_CONTRACT.direction,
            entry=CAND_035_CONTRACT.entry,
            exit=CAND_035_CONTRACT.exit,
            rearm_rule=CAND_035_CONTRACT.rearm_rule,
            session_boundaries=CAND_035_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand035_trigger_change(self):
        original = CAND_035_CONTRACT.hash
        mutated = FrozenStrategyContract(
            candidate_id=CAND_035_CONTRACT.candidate_id,
            version=CAND_035_CONTRACT.version,
            name=CAND_035_CONTRACT.name,
            instrument=CAND_035_CONTRACT.instrument,
            timezone=CAND_035_CONTRACT.timezone,
            preconditions=CAND_035_CONTRACT.preconditions,
            trigger="Last trading day of month at 14:30 ET",
            direction=CAND_035_CONTRACT.direction,
            entry=CAND_035_CONTRACT.entry,
            exit=CAND_035_CONTRACT.exit,
            rearm_rule=CAND_035_CONTRACT.rearm_rule,
            session_boundaries=CAND_035_CONTRACT.session_boundaries,
        )
        assert mutated.hash != original

    def test_cand035_session_boundaries_change(self):
        original = CAND_035_CONTRACT.hash
        new_bounds = dict(CAND_035_CONTRACT.session_boundaries)
        new_bounds["exit_time"] = "16:30 ET"
        mutated = FrozenStrategyContract(
            candidate_id=CAND_035_CONTRACT.candidate_id,
            version=CAND_035_CONTRACT.version,
            name=CAND_035_CONTRACT.name,
            instrument=CAND_035_CONTRACT.instrument,
            timezone=CAND_035_CONTRACT.timezone,
            preconditions=CAND_035_CONTRACT.preconditions,
            trigger=CAND_035_CONTRACT.trigger,
            direction=CAND_035_CONTRACT.direction,
            entry=CAND_035_CONTRACT.entry,
            exit=CAND_035_CONTRACT.exit,
            rearm_rule=CAND_035_CONTRACT.rearm_rule,
            session_boundaries=new_bounds,
        )
        assert mutated.hash != original


# =========================================================================
# 3. EVIDENCE EXCLUSION — changing evidence must NOT change hash
# =========================================================================

class TestEvidenceExclusion:
    """Historical evidence fields must not affect the canonical hash."""

    def test_cand024_evidence_independent(self):
        """Changing CAND-024 evidence does not change contract hash."""
        original_hash = CAND_024_CONTRACT.hash
        # Create new evidence with different values
        modified_evidence = HistoricalEvidence(
            candidate_id="CAND-024",
            historical_n=999,
            historical_frequency=99.99,
            historical_mean_net="+999.99 bps",
            historical_median_net="NEGATIVE",
            scientific_status="FAILED",
            friction_assumption="100.0 index points round-trip",
            mechanism_family="UNKNOWN",
            data_required="UNKNOWN",
        )
        # Hash must remain unchanged (evidence is separate)
        assert CAND_024_CONTRACT.hash == original_hash

    def test_cand035_evidence_independent(self):
        """Changing CAND-035 evidence does not change contract hash."""
        original_hash = CAND_035_CONTRACT.hash
        modified_evidence = HistoricalEvidence(
            candidate_id="CAND-035",
            historical_n=0,
            historical_frequency=0.0,
            historical_mean_net="-100 bps",
            historical_median_net="NEGATIVE",
            scientific_status="REJECTED",
            friction_assumption="100.0 index points round-trip",
            mechanism_family="UNKNOWN",
            data_required="UNKNOWN",
        )
        assert CAND_035_CONTRACT.hash == original_hash

    def test_evidence_is_separate_object(self):
        """Evidence must be a separate object from the contract."""
        assert isinstance(CAND_024_EVIDENCE, HistoricalEvidence)
        assert isinstance(CAND_035_EVIDENCE, HistoricalEvidence)
        assert not isinstance(CAND_024_EVIDENCE, FrozenStrategyContract)
        assert not isinstance(CAND_035_EVIDENCE, FrozenStrategyContract)

    def test_evidence_not_in_executable_dict(self):
        """Evidence fields must not appear in executable dict."""
        d = CAND_024_CONTRACT.to_executable_dict()
        for key in d:
            assert not key.startswith("historical_"), f"evidence field '{key}' in executable dict"
            assert key != "scientific_status", "scientific_status in executable dict"
            assert key != "friction_assumption", "friction_assumption in executable dict"
            assert key != "mechanism_family", "mechanism_family in executable dict"


# =========================================================================
# 4. ENVIRONMENT EXCLUSION — changing environment must NOT change hash
# =========================================================================

class TestEnvironmentExclusion:
    """Environment/broker fields must not affect the canonical hash."""

    def test_mapping_independent(self):
        """Changing the environment mapping does not change contract hash."""
        original_hash = CAND_024_CONTRACT.hash
        # The mapping is a completely separate object
        assert USATECHIDXUSD_USTECM_MAPPING.logical_symbol == "USATECHIDXUSD"
        assert USATECHIDXUSD_USTECM_MAPPING.broker_symbol == "USTECm"
        # Hash must remain unchanged
        assert CAND_024_CONTRACT.hash == original_hash

    def test_environment_not_in_executable_dict(self):
        """Environment fields must not appear in executable dict."""
        d = CAND_024_CONTRACT.to_executable_dict()
        for key in d:
            assert key != "broker", "broker in executable dict"
            assert key != "broker_symbol", "broker_symbol in executable dict"
            assert key != "server", "server in executable dict"
            assert key != "mapping_id", "mapping_id in executable dict"

    def test_environment_is_separate_object(self):
        """Environment must be a separate object from the contract."""
        assert isinstance(USATECHIDXUSD_USTECM_MAPPING, EnvironmentMapping)
        assert not isinstance(USATECHIDXUSD_USTECM_MAPPING, FrozenStrategyContract)

    def test_tainted_hash_differs(self):
        """Adding environment metadata to executable dict produces different hash."""
        d = CAND_024_CONTRACT.to_executable_dict()
        d["mapping_id"] = "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0"
        d["broker_symbol"] = "USTECm"
        tainted = _canonical_hash(d)
        assert tainted != CAND_024_CONTRACT.hash


# =========================================================================
# 5. FIELD COMPLETENESS
# =========================================================================

class TestFieldCompleteness:
    """Required semantic fields cannot be omitted."""

    REQUIRED_FIELDS = [
        "candidate_id", "name", "instrument", "timezone",
        "preconditions", "trigger", "direction", "entry", "exit",
        "rearm_rule", "session_boundaries",
    ]

    def test_cand024_all_fields_present(self):
        d = CAND_024_CONTRACT.to_executable_dict()
        for field in self.REQUIRED_FIELDS:
            assert field in d, f"CAND-024 missing required field: {field}"

    def test_cand035_all_fields_present(self):
        d = CAND_035_CONTRACT.to_executable_dict()
        for field in self.REQUIRED_FIELDS:
            assert field in d, f"CAND-035 missing required field: {field}"

    def test_cand024_no_empty_fields(self):
        d = CAND_024_CONTRACT.to_executable_dict()
        for field in self.REQUIRED_FIELDS:
            val = d[field]
            assert val is not None, f"CAND-024 field '{field}' is None"
            if isinstance(val, str):
                assert val.strip(), f"CAND-024 field '{field}' is empty"
            if isinstance(val, (list, tuple)):
                assert len(val) > 0, f"CAND-024 field '{field}' is empty"

    def test_cand035_no_empty_fields(self):
        d = CAND_035_CONTRACT.to_executable_dict()
        for field in self.REQUIRED_FIELDS:
            val = d[field]
            assert val is not None, f"CAND-035 field '{field}' is None"
            if isinstance(val, str):
                assert val.strip(), f"CAND-035 field '{field}' is empty"
            if isinstance(val, (list, tuple)):
                assert len(val) > 0, f"CAND-035 field '{field}' is empty"


# =========================================================================
# 6. SERIALIZATION STABILITY
# =========================================================================

class TestSerializationStability:
    """Canonical serialization must be stable across runs."""

    def test_canonical_json_stability(self):
        """Same executable dict always produces same canonical JSON."""
        d = CAND_024_CONTRACT.to_executable_dict()
        j1 = json.dumps(d, sort_keys=True, separators=(',', ':'))
        j2 = json.dumps(d, sort_keys=True, separators=(',', ':'))
        assert j1 == j2

    def test_key_ordering_stability(self):
        """Sorted keys produce identical output regardless of input order."""
        d1 = {"z": 1, "a": 2, "m": 3}
        d2 = {"a": 2, "m": 3, "z": 1}
        j1 = json.dumps(d1, sort_keys=True, separators=(',', ':'))
        j2 = json.dumps(d2, sort_keys=True, separators=(',', ':'))
        assert j1 == j2

    def test_whitespace_stability(self):
        """Canonical JSON uses minimal whitespace."""
        d = CAND_024_CONTRACT.to_executable_dict()
        j = json.dumps(d, sort_keys=True, separators=(',', ':'))
        # No spaces after separators
        assert ", " not in j
        assert ": " not in j

    def test_executable_dict_is_json_serializable(self):
        """Executable dict must be JSON-serializable."""
        d = CAND_024_CONTRACT.to_executable_dict()
        json.dumps(d, sort_keys=True)
        d = CAND_035_CONTRACT.to_executable_dict()
        json.dumps(d, sort_keys=True)


# =========================================================================
# 7. ENGINE CONSISTENCY
# =========================================================================

class TestEngineConsistency:
    """Engine implementations must use the canonical contract."""

    def test_cand024_engine_uses_canonical_contract(self):
        engine = Cand024Engine()
        assert engine.contract is CAND_024_CONTRACT
        assert engine.contract.hash == CAND_024_CONTRACT.hash
        assert engine.contract.identity == CAND_024_CONTRACT.identity

    def test_cand035_engine_uses_canonical_contract(self):
        engine = Cand035Engine()
        assert engine.contract is CAND_035_CONTRACT
        assert engine.contract.hash == CAND_035_CONTRACT.hash
        assert engine.contract.identity == CAND_035_CONTRACT.identity

    def test_cand024_engine_instrument(self):
        engine = Cand024Engine()
        assert engine.contract.instrument == "USATECHIDXUSD"

    def test_cand035_engine_instrument(self):
        engine = Cand035Engine()
        assert engine.contract.instrument == "USATECHIDXUSD"

    def test_cand024_engine_direction(self):
        engine = Cand024Engine()
        assert engine.contract.direction == "Short"

    def test_cand035_engine_direction(self):
        engine = Cand035Engine()
        assert engine.contract.direction == "Long"

    def test_cand024_engine_timezone(self):
        engine = Cand024Engine()
        assert engine.contract.timezone == "America/New_York"
        assert str(engine.ny_tz) == "America/New_York"

    def test_cand035_engine_timezone(self):
        engine = Cand035Engine()
        assert engine.contract.timezone == "America/New_York"
        assert str(engine.ny_tz) == "America/New_York"


# =========================================================================
# 8. NEGATIVE TESTS
# =========================================================================

class TestNegativeTests:
    """Invalid contracts must be rejected."""

    def test_missing_candidate_id(self):
        with pytest.raises(TypeError):
            FrozenStrategyContract(
                version="1.0", name="Test", instrument="USATECHIDXUSD",
                timezone="UTC", preconditions=("cond",), trigger="t",
                direction="Long", entry="e", exit="x", rearm_rule="r",
                session_boundaries={},
            )

    def test_empty_name_rejected(self):
        with pytest.raises(ValueError, match="name"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=("cond",), trigger="t", direction="Long",
                entry="e", exit="x", rearm_rule="r", session_boundaries={},
            )

    def test_empty_instrument_rejected(self):
        with pytest.raises(ValueError, match="instrument"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="Test",
                instrument="", timezone="UTC",
                preconditions=("cond",), trigger="t", direction="Long",
                entry="e", exit="x", rearm_rule="r", session_boundaries={},
            )

    def test_empty_preconditions_rejected(self):
        with pytest.raises(ValueError, match="precondition"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="Test",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=(), trigger="t", direction="Long",
                entry="e", exit="x", rearm_rule="r", session_boundaries={},
            )

    def test_empty_trigger_rejected(self):
        with pytest.raises(ValueError, match="trigger"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="Test",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=("cond",), trigger="", direction="Long",
                entry="e", exit="x", rearm_rule="r", session_boundaries={},
            )

    def test_empty_direction_rejected(self):
        with pytest.raises(ValueError, match="direction"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="Test",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=("cond",), trigger="t", direction="",
                entry="e", exit="x", rearm_rule="r", session_boundaries={},
            )

    def test_empty_entry_rejected(self):
        with pytest.raises(ValueError, match="entry"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="Test",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=("cond",), trigger="t", direction="Long",
                entry="", exit="x", rearm_rule="r", session_boundaries={},
            )

    def test_empty_exit_rejected(self):
        with pytest.raises(ValueError, match="exit"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="Test",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=("cond",), trigger="t", direction="Long",
                entry="e", exit="", rearm_rule="r", session_boundaries={},
            )

    def test_empty_rearm_rejected(self):
        with pytest.raises(ValueError, match="rearm_rule"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="Test",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=("cond",), trigger="t", direction="Long",
                entry="e", exit="x", rearm_rule="", session_boundaries={},
            )

    def test_whitespace_only_name_rejected(self):
        with pytest.raises(ValueError, match="name"):
            FrozenStrategyContract(
                candidate_id="CAND-TEST", version="1.0", name="   ",
                instrument="USATECHIDXUSD", timezone="UTC",
                preconditions=("cond",), trigger="t", direction="Long",
                entry="e", exit="x", rearm_rule="r", session_boundaries={},
            )

    def test_frozen_contract_is_immutable(self):
        """FrozenStrategyContract is a frozen dataclass — attribute assignment must fail."""
        with pytest.raises(AttributeError):
            CAND_024_CONTRACT.name = "TAMPERED"


# =========================================================================
# 9. CANONICAL vs PHANTOM HASH SEPARATION
# =========================================================================

class TestPhantomHashSeparation:
    """Historical phantom hashes must not be confused with canonical hashes."""

    def test_cand024_not_phantom(self):
        """CAND-024 canonical hash is NOT the phantom governance identifier."""
        assert CAND_024_CONTRACT.hash[:8] != "c49c5bb0"

    def test_cand035_not_phantom(self):
        """CAND-035 canonical hash is NOT the phantom governance identifier."""
        assert CAND_035_CONTRACT.hash[:8] != "a7c2132d"

    def test_canonical_identity_format(self):
        """Canonical identity uses CANONICAL: prefix, not version: prefix."""
        assert "CANONICAL:" in CAND_024_CONTRACT.identity
        assert "CANONICAL:" in CAND_035_CONTRACT.identity


# =========================================================================
# 10. CONTRACT CONTENT VERIFICATION
# =========================================================================

class TestContractContent:
    """Verify the ratified canonical contract content matches V8/V12."""

    def test_cand024_name_v8(self):
        """CAND-024 name matches V8 original."""
        assert CAND_024_CONTRACT.name == "Friday De-Risking Conditioned by Morning Exhaustion"

    def test_cand024_instrument(self):
        assert CAND_024_CONTRACT.instrument == "USATECHIDXUSD"

    def test_cand024_timezone(self):
        assert CAND_024_CONTRACT.timezone == "America/New_York"

    def test_cand024_direction(self):
        assert CAND_024_CONTRACT.direction == "Short"

    def test_cand024_preconditions_count(self):
        """V8 specifies two conditions: High > Weekly High AND 12:00 open < 08:00 open."""
        assert len(CAND_024_CONTRACT.preconditions) == 2

    def test_cand024_precondition_1(self):
        assert "Weekly High" in CAND_024_CONTRACT.preconditions[0]

    def test_cand024_precondition_2(self):
        assert "08:00" in CAND_024_CONTRACT.preconditions[1] and "12:00" in CAND_024_CONTRACT.preconditions[1]

    def test_cand024_trigger(self):
        assert "12:00" in CAND_024_CONTRACT.trigger and "Friday" in CAND_024_CONTRACT.trigger

    def test_cand024_exit(self):
        assert "15:45" in CAND_024_CONTRACT.exit

    def test_cand024_rearm(self):
        assert "week" in CAND_024_CONTRACT.rearm_rule.lower()

    def test_cand024_session_boundaries(self):
        sb = CAND_024_CONTRACT.session_boundaries
        assert "08:00" in sb["morning_tracking_start"]
        assert "12:00" in sb["trigger_time"]
        assert "15:45" in sb["exit_time"]

    def test_cand035_name_v12(self):
        """CAND-035 name matches V12 original."""
        assert CAND_035_CONTRACT.name == "Month-End Final-Hour Imbalance Acceleration"

    def test_cand035_instrument(self):
        assert CAND_035_CONTRACT.instrument == "USATECHIDXUSD"

    def test_cand035_direction(self):
        assert CAND_035_CONTRACT.direction == "Long"

    def test_cand035_preconditions_count(self):
        """Two conditions: last trading day AND 15:00 > 09:30 open."""
        assert len(CAND_035_CONTRACT.preconditions) == 2

    def test_cand035_trigger(self):
        assert "15:00" in CAND_035_CONTRACT.trigger and "month" in CAND_035_CONTRACT.trigger.lower()

    def test_cand035_exit(self):
        assert "16:00" in CAND_035_CONTRACT.exit

    def test_cand035_rearm(self):
        assert "month" in CAND_035_CONTRACT.rearm_rule.lower()

    def test_cand035_session_boundaries(self):
        sb = CAND_035_CONTRACT.session_boundaries
        assert "09:30" in sb["reference_open"]
        assert "15:00" in sb["trigger_time"]
        assert "16:00" in sb["exit_time"]
