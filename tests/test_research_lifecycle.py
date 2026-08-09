"""Complete unittest coverage for Phase 8.1 — Research Lifecycle domain.

Tests:
- Immutability of all frozen dataclasses
- Equality and hashing determinism
- Deterministic builder behaviour
- Invalid data rejection for every object
- Provenance preservation through the builder
- Auto-conversion of mutable inputs to immutable types
"""

import unittest
from datetime import datetime

from research.lifecycle.research_candidate import ResearchCandidate
from research.lifecycle.provenance import Provenance
from research.lifecycle.strategy_manifest import StrategyManifest
from research.lifecycle.strategy_manifest_builder import StrategyManifestBuilder
from research.lifecycle.research_errors import (
    InvalidResearchCandidateData,
    InvalidProvenanceData,
    InvalidStrategyManifestData,
    ManifestBuildError,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_candidate(**overrides) -> ResearchCandidate:
    """Build a valid ResearchCandidate with sensible defaults."""
    defaults = dict(
        candidate_id="RC-001",
        hypothesis_id="HYP-001",
        research_name="Mean Reversion Recoil",
        behaviour_name="recoil_after_displacement",
        description="Test whether displaced price exhibits statistically significant recoil.",
        creation_timestamp=datetime(2026, 8, 1, 12, 0, 0),
        research_version="1.0.0",
        assumptions=("Markets exhibit mean-reverting behaviour after extreme displacement.",),
        success_criteria=("Recoil observed in >60% of displacement events.",),
        metadata=(("author", "Researcher A"), ("market", "XAUUSD")),
    )
    defaults.update(overrides)
    return ResearchCandidate(**defaults)


def _make_provenance(**overrides) -> Provenance:
    """Build a valid Provenance with sensible defaults."""
    defaults = dict(
        research_candidate_id="RC-001",
        validation_id="VAL-001",
        experiment_id="EXP-001",
        strategy_manifest_id="STRAT-001",
        created_timestamp=datetime(2026, 8, 1, 14, 0, 0),
    )
    defaults.update(overrides)
    return Provenance(**defaults)


def _make_manifest(**overrides) -> StrategyManifest:
    """Build a valid StrategyManifest with sensible defaults."""
    defaults = dict(
        strategy_id="STRAT-001",
        behaviour_name="recoil_after_displacement",
        observer_ids=("obs-recoil-001", "obs-persist-001"),
        interpretation_model_id="interp-mr-001",
        decision_policy_id="dp-deterministic-001",
        risk_policy_id="rp-fixed-001",
        deployment_profile="paper",
        manifest_version="1.0.0",
        provenance=_make_provenance(),
    )
    defaults.update(overrides)
    return StrategyManifest(**defaults)


# ===========================================================================
# ResearchCandidate Tests
# ===========================================================================


class TestResearchCandidateConstruction(unittest.TestCase):
    """Valid construction and field access."""

    def test_valid_construction(self):
        rc = _make_candidate()
        self.assertEqual(rc.candidate_id, "RC-001")
        self.assertEqual(rc.hypothesis_id, "HYP-001")
        self.assertEqual(rc.research_name, "Mean Reversion Recoil")
        self.assertEqual(rc.behaviour_name, "recoil_after_displacement")
        self.assertEqual(rc.research_version, "1.0.0")
        self.assertIsInstance(rc.creation_timestamp, datetime)
        self.assertIsInstance(rc.assumptions, tuple)
        self.assertIsInstance(rc.success_criteria, tuple)
        self.assertIsInstance(rc.metadata, tuple)

    def test_empty_assumptions_and_criteria(self):
        """Empty tuples are valid — a candidate may have no assumptions yet."""
        rc = _make_candidate(assumptions=(), success_criteria=())
        self.assertEqual(rc.assumptions, ())
        self.assertEqual(rc.success_criteria, ())

    def test_empty_metadata(self):
        rc = _make_candidate(metadata=())
        self.assertEqual(rc.metadata, ())


class TestResearchCandidateImmutability(unittest.TestCase):
    """Frozen dataclass — cannot set attributes after construction."""

    def test_cannot_mutate_candidate_id(self):
        rc = _make_candidate()
        with self.assertRaises(AttributeError):
            rc.candidate_id = "RC-002"  # type: ignore

    def test_cannot_mutate_assumptions(self):
        rc = _make_candidate()
        with self.assertRaises(AttributeError):
            rc.assumptions = ("new",)  # type: ignore

    def test_cannot_mutate_metadata(self):
        rc = _make_candidate()
        with self.assertRaises(AttributeError):
            rc.metadata = ()  # type: ignore


class TestResearchCandidateEquality(unittest.TestCase):
    """Same fields → equal objects and identical hashes."""

    def test_equality(self):
        rc1 = _make_candidate()
        rc2 = _make_candidate()
        self.assertEqual(rc1, rc2)

    def test_hash_equality(self):
        rc1 = _make_candidate()
        rc2 = _make_candidate()
        self.assertEqual(hash(rc1), hash(rc2))

    def test_usable_in_sets(self):
        rc1 = _make_candidate()
        rc2 = _make_candidate()
        self.assertEqual(len({rc1, rc2}), 1)

    def test_usable_as_dict_key(self):
        rc = _make_candidate()
        d = {rc: "value"}
        self.assertEqual(d[_make_candidate()], "value")

    def test_inequality_on_different_id(self):
        rc1 = _make_candidate(candidate_id="RC-001")
        rc2 = _make_candidate(candidate_id="RC-002")
        self.assertNotEqual(rc1, rc2)


class TestResearchCandidateDeterminism(unittest.TestCase):
    """Same inputs → identical objects, always."""

    def test_deterministic(self):
        for _ in range(10):
            rc = _make_candidate()
            self.assertEqual(rc, _make_candidate())
            self.assertEqual(hash(rc), hash(_make_candidate()))


class TestResearchCandidateAutoConversion(unittest.TestCase):
    """Lists auto-converted to tuples, dicts to sorted tuple of items."""

    def test_list_assumptions_converted_to_tuple(self):
        rc = _make_candidate(assumptions=["assumption1", "assumption2"])
        self.assertIsInstance(rc.assumptions, tuple)
        self.assertEqual(rc.assumptions, ("assumption1", "assumption2"))

    def test_list_success_criteria_converted_to_tuple(self):
        rc = _make_candidate(success_criteria=["criterion1"])
        self.assertIsInstance(rc.success_criteria, tuple)

    def test_dict_metadata_converted_to_sorted_tuple(self):
        rc = _make_candidate(metadata={"market": "XAUUSD", "author": "A"})
        self.assertIsInstance(rc.metadata, tuple)
        self.assertEqual(rc.metadata, (("author", "A"), ("market", "XAUUSD")))


class TestResearchCandidateInvalidData(unittest.TestCase):
    """Invalid data raises InvalidResearchCandidateData."""

    def test_empty_candidate_id(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(candidate_id="")

    def test_whitespace_candidate_id(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(candidate_id="   ")

    def test_empty_hypothesis_id(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(hypothesis_id="")

    def test_empty_research_name(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(research_name="")

    def test_empty_behaviour_name(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(behaviour_name=" ")

    def test_empty_description(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(description="")

    def test_invalid_research_version_format(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(research_version="v1.0")

    def test_invalid_research_version_not_semantic(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(research_version="1.0")

    def test_invalid_timestamp_type(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(creation_timestamp="2026-01-01")  # type: ignore

    def test_non_string_in_assumptions(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(assumptions=(123,))  # type: ignore

    def test_non_string_in_success_criteria(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(success_criteria=(None,))  # type: ignore

    def test_invalid_metadata_not_pair(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(metadata=(("key",),))  # type: ignore

    def test_invalid_metadata_non_string_key(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(metadata=((123, "val"),))  # type: ignore

    def test_assumptions_wrong_type(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(assumptions="not a tuple")  # type: ignore

    def test_success_criteria_wrong_type(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(success_criteria=42)  # type: ignore

    def test_metadata_wrong_type(self):
        with self.assertRaises(InvalidResearchCandidateData):
            _make_candidate(metadata=42)  # type: ignore


# ===========================================================================
# Provenance Tests
# ===========================================================================


class TestProvenanceConstruction(unittest.TestCase):

    def test_valid_construction(self):
        p = _make_provenance()
        self.assertEqual(p.research_candidate_id, "RC-001")
        self.assertEqual(p.validation_id, "VAL-001")
        self.assertEqual(p.experiment_id, "EXP-001")
        self.assertEqual(p.strategy_manifest_id, "STRAT-001")
        self.assertIsInstance(p.created_timestamp, datetime)


class TestProvenanceImmutability(unittest.TestCase):

    def test_cannot_mutate(self):
        p = _make_provenance()
        with self.assertRaises(AttributeError):
            p.research_candidate_id = "RC-999"  # type: ignore
        with self.assertRaises(AttributeError):
            p.validation_id = "VAL-999"  # type: ignore


class TestProvenanceEquality(unittest.TestCase):

    def test_equality(self):
        p1 = _make_provenance()
        p2 = _make_provenance()
        self.assertEqual(p1, p2)

    def test_hash_equality(self):
        p1 = _make_provenance()
        p2 = _make_provenance()
        self.assertEqual(hash(p1), hash(p2))

    def test_usable_in_set(self):
        self.assertEqual(len({_make_provenance(), _make_provenance()}), 1)

    def test_inequality(self):
        p1 = _make_provenance(validation_id="VAL-001")
        p2 = _make_provenance(validation_id="VAL-002")
        self.assertNotEqual(p1, p2)


class TestProvenanceInvalidData(unittest.TestCase):

    def test_empty_research_candidate_id(self):
        with self.assertRaises(InvalidProvenanceData):
            _make_provenance(research_candidate_id="")

    def test_empty_validation_id(self):
        with self.assertRaises(InvalidProvenanceData):
            _make_provenance(validation_id=" ")

    def test_empty_experiment_id(self):
        with self.assertRaises(InvalidProvenanceData):
            _make_provenance(experiment_id="")

    def test_empty_strategy_manifest_id(self):
        with self.assertRaises(InvalidProvenanceData):
            _make_provenance(strategy_manifest_id="")

    def test_invalid_timestamp(self):
        with self.assertRaises(InvalidProvenanceData):
            _make_provenance(created_timestamp="not a datetime")  # type: ignore


# ===========================================================================
# StrategyManifest Tests
# ===========================================================================


class TestStrategyManifestConstruction(unittest.TestCase):

    def test_valid_construction(self):
        m = _make_manifest()
        self.assertEqual(m.strategy_id, "STRAT-001")
        self.assertEqual(m.behaviour_name, "recoil_after_displacement")
        self.assertEqual(m.observer_ids, ("obs-recoil-001", "obs-persist-001"))
        self.assertEqual(m.interpretation_model_id, "interp-mr-001")
        self.assertEqual(m.decision_policy_id, "dp-deterministic-001")
        self.assertEqual(m.risk_policy_id, "rp-fixed-001")
        self.assertEqual(m.deployment_profile, "paper")
        self.assertEqual(m.manifest_version, "1.0.0")
        self.assertIsInstance(m.provenance, Provenance)

    def test_contains_only_identifiers(self):
        """Manifest fields are all strings or tuples of strings — no logic objects."""
        m = _make_manifest()
        for field_name in ("strategy_id", "behaviour_name", "interpretation_model_id",
                           "decision_policy_id", "risk_policy_id", "deployment_profile",
                           "manifest_version"):
            self.assertIsInstance(getattr(m, field_name), str)
        self.assertIsInstance(m.observer_ids, tuple)
        for o in m.observer_ids:
            self.assertIsInstance(o, str)


class TestStrategyManifestImmutability(unittest.TestCase):

    def test_cannot_mutate(self):
        m = _make_manifest()
        with self.assertRaises(AttributeError):
            m.strategy_id = "STRAT-999"  # type: ignore
        with self.assertRaises(AttributeError):
            m.observer_ids = ()  # type: ignore
        with self.assertRaises(AttributeError):
            m.provenance = None  # type: ignore


class TestStrategyManifestEquality(unittest.TestCase):

    def test_equality(self):
        m1 = _make_manifest()
        m2 = _make_manifest()
        self.assertEqual(m1, m2)

    def test_hash_equality(self):
        m1 = _make_manifest()
        m2 = _make_manifest()
        self.assertEqual(hash(m1), hash(m2))

    def test_usable_in_set(self):
        self.assertEqual(len({_make_manifest(), _make_manifest()}), 1)


class TestStrategyManifestInvalidData(unittest.TestCase):

    def test_empty_strategy_id(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(strategy_id="")

    def test_empty_behaviour_name(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(behaviour_name="")

    def test_empty_observer_ids(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(observer_ids=())

    def test_observer_ids_with_empty_string(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(observer_ids=("obs-1", ""))

    def test_empty_interpretation_model_id(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(interpretation_model_id="")

    def test_empty_decision_policy_id(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(decision_policy_id=" ")

    def test_empty_risk_policy_id(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(risk_policy_id="")

    def test_empty_deployment_profile(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(deployment_profile="")

    def test_invalid_manifest_version(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(manifest_version="v2")

    def test_invalid_provenance_type(self):
        with self.assertRaises(InvalidStrategyManifestData):
            _make_manifest(provenance="not-a-provenance")  # type: ignore

    def test_list_observer_ids_auto_converted(self):
        """Lists should be auto-converted to tuples."""
        m = _make_manifest(observer_ids=["obs-1", "obs-2"])
        self.assertIsInstance(m.observer_ids, tuple)
        self.assertEqual(m.observer_ids, ("obs-1", "obs-2"))


# ===========================================================================
# StrategyManifestBuilder Tests
# ===========================================================================


class TestStrategyManifestBuilderDeterministic(unittest.TestCase):
    """Builder produces identical manifests from identical inputs."""

    def _build_manifest(self):
        ts = datetime(2026, 8, 1, 15, 0, 0)
        candidate = _make_candidate()
        return (
            StrategyManifestBuilder()
            .with_candidate(candidate)
            .with_validation("VAL-001", "EXP-001")
            .with_observers(["obs-recoil-001", "obs-persist-001"])
            .with_interpretation_model("interp-mr-001")
            .with_decision_policy("dp-deterministic-001")
            .with_risk_policy("rp-fixed-001")
            .with_deployment_profile("paper")
            .build(
                strategy_id="STRAT-001",
                manifest_version="1.0.0",
                provenance_timestamp=ts,
            )
        )

    def test_deterministic_build(self):
        m1 = self._build_manifest()
        m2 = self._build_manifest()
        self.assertEqual(m1, m2)
        self.assertEqual(hash(m1), hash(m2))

    def test_repeated_builds_identical(self):
        for _ in range(5):
            self.assertEqual(self._build_manifest(), self._build_manifest())


class TestStrategyManifestBuilderProvenance(unittest.TestCase):
    """Builder constructs correct provenance chain."""

    def test_provenance_links_to_candidate(self):
        ts = datetime(2026, 8, 1, 15, 0, 0)
        candidate = _make_candidate(candidate_id="RC-CUSTOM")
        m = (
            StrategyManifestBuilder()
            .with_candidate(candidate)
            .with_validation("VAL-X", "EXP-X")
            .with_observers(("obs-1",))
            .with_interpretation_model("interp-1")
            .with_decision_policy("dp-1")
            .with_risk_policy("rp-1")
            .with_deployment_profile("demo")
            .build(strategy_id="STRAT-X", manifest_version="2.0.0", provenance_timestamp=ts)
        )
        self.assertEqual(m.provenance.research_candidate_id, "RC-CUSTOM")
        self.assertEqual(m.provenance.validation_id, "VAL-X")
        self.assertEqual(m.provenance.experiment_id, "EXP-X")
        self.assertEqual(m.provenance.strategy_manifest_id, "STRAT-X")
        self.assertEqual(m.provenance.created_timestamp, ts)

    def test_behaviour_name_inherited_from_candidate(self):
        candidate = _make_candidate(behaviour_name="my_behaviour")
        m = (
            StrategyManifestBuilder()
            .with_candidate(candidate)
            .with_validation("V", "E")
            .with_observers(("o",))
            .with_interpretation_model("i")
            .with_decision_policy("d")
            .with_risk_policy("r")
            .with_deployment_profile("live")
            .build(strategy_id="S", manifest_version="1.0.0",
                   provenance_timestamp=datetime(2026, 1, 1))
        )
        self.assertEqual(m.behaviour_name, "my_behaviour")


class TestStrategyManifestBuilderMissingInputs(unittest.TestCase):
    """Builder rejects incomplete configurations."""

    def test_missing_candidate(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_validation("V", "E")
                .with_observers(("o",))
                .with_interpretation_model("i")
                .with_decision_policy("d")
                .with_risk_policy("r")
                .with_deployment_profile("paper")
                .build(strategy_id="S", manifest_version="1.0.0")
            )

    def test_missing_validation(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_observers(("o",))
                .with_interpretation_model("i")
                .with_decision_policy("d")
                .with_risk_policy("r")
                .with_deployment_profile("paper")
                .build(strategy_id="S", manifest_version="1.0.0")
            )

    def test_missing_observers(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_validation("V", "E")
                .with_interpretation_model("i")
                .with_decision_policy("d")
                .with_risk_policy("r")
                .with_deployment_profile("paper")
                .build(strategy_id="S", manifest_version="1.0.0")
            )

    def test_missing_interpretation_model(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_validation("V", "E")
                .with_observers(("o",))
                .with_decision_policy("d")
                .with_risk_policy("r")
                .with_deployment_profile("paper")
                .build(strategy_id="S", manifest_version="1.0.0")
            )

    def test_missing_decision_policy(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_validation("V", "E")
                .with_observers(("o",))
                .with_interpretation_model("i")
                .with_risk_policy("r")
                .with_deployment_profile("paper")
                .build(strategy_id="S", manifest_version="1.0.0")
            )

    def test_missing_risk_policy(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_validation("V", "E")
                .with_observers(("o",))
                .with_interpretation_model("i")
                .with_decision_policy("d")
                .with_deployment_profile("paper")
                .build(strategy_id="S", manifest_version="1.0.0")
            )

    def test_missing_deployment_profile(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_validation("V", "E")
                .with_observers(("o",))
                .with_interpretation_model("i")
                .with_decision_policy("d")
                .with_risk_policy("r")
                .build(strategy_id="S", manifest_version="1.0.0")
            )


class TestStrategyManifestBuilderInvalidInputs(unittest.TestCase):
    """Builder rejects invalid individual inputs."""

    def test_invalid_candidate_type(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_candidate("not a candidate")  # type: ignore

    def test_empty_validation_id(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_validation("", "EXP-001")

    def test_empty_experiment_id(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_validation("VAL-001", "")

    def test_empty_observers(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_observers([])

    def test_observer_with_empty_string(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_observers(["obs-1", ""])

    def test_empty_interpretation_model(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_interpretation_model("")

    def test_empty_decision_policy(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_decision_policy(" ")

    def test_empty_risk_policy(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_risk_policy("")

    def test_empty_deployment_profile(self):
        with self.assertRaises(ManifestBuildError):
            StrategyManifestBuilder().with_deployment_profile("")

    def test_invalid_strategy_id_at_build(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_validation("V", "E")
                .with_observers(("o",))
                .with_interpretation_model("i")
                .with_decision_policy("d")
                .with_risk_policy("r")
                .with_deployment_profile("paper")
                .build(strategy_id="", manifest_version="1.0.0")
            )

    def test_invalid_manifest_version_at_build(self):
        with self.assertRaises(ManifestBuildError):
            (
                StrategyManifestBuilder()
                .with_candidate(_make_candidate())
                .with_validation("V", "E")
                .with_observers(("o",))
                .with_interpretation_model("i")
                .with_decision_policy("d")
                .with_risk_policy("r")
                .with_deployment_profile("paper")
                .build(strategy_id="S", manifest_version="bad")
            )


class TestStrategyManifestBuilderResultImmutability(unittest.TestCase):
    """Builder output is fully immutable."""

    def test_result_is_frozen(self):
        ts = datetime(2026, 1, 1)
        m = (
            StrategyManifestBuilder()
            .with_candidate(_make_candidate())
            .with_validation("V", "E")
            .with_observers(("o",))
            .with_interpretation_model("i")
            .with_decision_policy("d")
            .with_risk_policy("r")
            .with_deployment_profile("paper")
            .build(strategy_id="S", manifest_version="1.0.0", provenance_timestamp=ts)
        )
        with self.assertRaises(AttributeError):
            m.strategy_id = "X"  # type: ignore
        with self.assertRaises(AttributeError):
            m.provenance = None  # type: ignore


if __name__ == "__main__":
    unittest.main()
