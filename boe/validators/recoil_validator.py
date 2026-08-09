"""Research-derived Recoil Validator using only stable candidate and context contracts."""

from pathlib import Path
from typing import Mapping

from boe.candidate import Candidate

from .recoil_config import RecoilConfig
from .validation_context import ValidationContext
from .validation_result import ValidationResult
from .validator_contract import BehaviorValidatorContract
from .validator_errors import ValidationContextError


class RecoilValidator(BehaviorValidatorContract):
    """Classifies whether supplied market context shows configured-direction recoil.

    Context data must contain only raw contextual fields used by this validator:
    ``reference_value``, ``current_value``, and ``expected_recoil_direction``.
    These values remain validator input; its public result exposes only abstract
    recoil evidence labels.
    """

    VALIDATOR_ID = "recoil_validator"
    VALIDATOR_NAME = "Recoil Validator"
    VALIDATOR_VERSION = "1.0.0"

    def __init__(self, config: RecoilConfig) -> None:
        if not isinstance(config, RecoilConfig):
            raise ValidationContextError("RecoilValidator requires a RecoilConfig.")
        self._config = config

    @classmethod
    def from_config_file(cls, config_path: Path | str) -> "RecoilValidator":
        """Create a validator from externally maintained recoil configuration."""
        return cls(RecoilConfig.from_json(config_path))

    @property
    def validator_id(self) -> str:
        """Return the stable recoil validator identifier."""
        return self.VALIDATOR_ID

    @property
    def validator_name(self) -> str:
        """Return the stable recoil validator name."""
        return self.VALIDATOR_NAME

    @property
    def validator_version(self) -> str:
        """Return the semantic version of this validator implementation."""
        return self.VALIDATOR_VERSION

    def validate(self, candidate: Candidate, context: ValidationContext) -> ValidationResult:
        """Return abstract evidence for whether configured-direction recoil occurred."""
        if not isinstance(candidate, Candidate):
            raise ValidationContextError("RecoilValidator candidate must be a Candidate.")
        if not isinstance(context, ValidationContext):
            raise ValidationContextError("RecoilValidator context must be a ValidationContext.")
        if context.candidate_id != candidate.candidate_id:
            raise ValidationContextError("ValidationContext candidate_id must match the Candidate.")

        reference_value, current_value, direction = self._extract_context(context.context_data)
        observed_distance = (
            current_value - reference_value
            if direction == "UP"
            else reference_value - current_value
        )
        passed = observed_distance >= self._config.minimum_recoil_distance
        return ValidationResult(
            schema_version="1.0.0",
            candidate_id=candidate.candidate_id,
            validator_id=self.validator_id,
            validator_version=self.validator_version,
            passed=passed,
            confidence=1.0 if passed else 0.0,
            evidence=("RECOIL_OBSERVED" if passed else "RECOIL_NOT_OBSERVED",),
            timestamp=context.observed_at,
        )

    @staticmethod
    def _extract_context(context_data: Mapping[str, object]) -> tuple[float, float, str]:
        """Validate the minimal raw market context required for recoil observation."""
        required_fields = {"reference_value", "current_value", "expected_recoil_direction"}
        missing_fields = required_fields.difference(context_data)
        if missing_fields:
            raise ValidationContextError(
                "Recoil validation context is missing required fields: "
                f"{', '.join(sorted(missing_fields))}"
            )
        reference_value = context_data["reference_value"]
        current_value = context_data["current_value"]
        direction = context_data["expected_recoil_direction"]
        if (
            not isinstance(reference_value, (int, float))
            or isinstance(reference_value, bool)
            or not isinstance(current_value, (int, float))
            or isinstance(current_value, bool)
        ):
            raise ValidationContextError("Recoil validation values must be numeric.")
        if direction not in {"UP", "DOWN"}:
            raise ValidationContextError("Recoil validation direction must be UP or DOWN.")
        return float(reference_value), float(current_value), direction
