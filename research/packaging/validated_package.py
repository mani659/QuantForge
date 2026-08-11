from dataclasses import dataclass, replace
import json
import hashlib
from typing import Any

from research.lifecycle.strategy_manifest import StrategyManifest
from research.engine.configuration import ExperimentConfiguration
from research.analytics.verdict import ScientificVerdict


class _ImmutableDict(dict):
    def __setitem__(self, key, value):
        raise TypeError("ValidatedStrategyPackage contents are immutable")
    def __delitem__(self, key):
        raise TypeError("ValidatedStrategyPackage contents are immutable")
    def clear(self):
        raise TypeError("ValidatedStrategyPackage contents are immutable")
    def pop(self, k, d=None):
        raise TypeError("ValidatedStrategyPackage contents are immutable")
    def popitem(self):
        raise TypeError("ValidatedStrategyPackage contents are immutable")
    def setdefault(self, k, d=None):
        raise TypeError("ValidatedStrategyPackage contents are immutable")
    def update(self, *args, **kwargs):
        raise TypeError("ValidatedStrategyPackage contents are immutable")


def _deep_freeze(obj: Any) -> Any:
    if isinstance(obj, dict):
        return _ImmutableDict({k: _deep_freeze(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return tuple(_deep_freeze(v) for v in obj)
    return obj


@dataclass(frozen=True)
class ValidatedStrategyPackage:
    """
    Immutable deployment package bridging a scientifically accepted research outcome 
    to a deployment-ready operational manifest.
    """
    strategy_manifest: StrategyManifest
    configuration: ExperimentConfiguration
    scientific_verdict: ScientificVerdict
    package_fingerprint: str

    def __post_init__(self):
        # Prevent shallow mutation by deep-freezing the configuration
        frozen_params = _deep_freeze(self.configuration.strategy_parameters)
        frozen_costs = _deep_freeze(self.configuration.transaction_costs)
        
        frozen_config = replace(
            self.configuration,
            strategy_parameters=frozen_params,
            transaction_costs=frozen_costs
        )
        object.__setattr__(self, 'configuration', frozen_config)

    def verify_fingerprint(self) -> bool:
        """
        Deterministically verifies the package content against the fingerprint.
        """
        expected = self.compute_canonical_fingerprint(
            self.strategy_manifest,
            self.configuration,
            self.scientific_verdict
        )
        return expected == self.package_fingerprint

    @staticmethod
    def compute_canonical_fingerprint(
        manifest: StrategyManifest, 
        config: ExperimentConfiguration, 
        verdict: ScientificVerdict
    ) -> str:
        """
        Creates a deterministic SHA-256 fingerprint from the core identities.
        """
        manifest_canonical = {
            "strategy_id": manifest.strategy_id,
            "manifest_version": manifest.manifest_version,
            "observer_ids": list(manifest.observer_ids),
            "decision_policy_id": manifest.decision_policy_id,
            "risk_policy_id": manifest.risk_policy_id,
            "deployment_profile": manifest.deployment_profile,
            "provenance": {
                "research_candidate_id": manifest.provenance.research_candidate_id,
                "validation_id": manifest.provenance.validation_id,
                "experiment_id": manifest.provenance.experiment_id,
                "strategy_manifest_id": manifest.provenance.strategy_manifest_id,
            }
        }
        
        from research.orchestration.matrix import generate_experiment_id
        config_id = generate_experiment_id(config)
        
        verdict_canonical = {
            "hypothesis_id": verdict.hypothesis_id,
            "validation_experiment_id": verdict.validation_experiment_id,
            "dataset_fingerprint": verdict.dataset_fingerprint,
            "verdict": verdict.verdict.value,
        }
        
        payload = {
            "manifest": manifest_canonical,
            "configuration_identity": config_id,
            "verdict": verdict_canonical
        }
        
        payload_json = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
