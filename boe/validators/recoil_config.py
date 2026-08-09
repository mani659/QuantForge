"""Immutable external configuration contract for the Recoil Validator."""

from dataclasses import dataclass
import json
from pathlib import Path
import re

from boe.detector_errors import ConfigurationError, VersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class RecoilConfig:
    """Externally supplied threshold required to classify an observed recoil."""

    schema_version: str
    minimum_recoil_distance: float

    def __post_init__(self) -> None:
        """Validate configuration shape without embedding research parameters."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VersionMismatchError("RecoilConfig schema_version must be semantic versioning.")
        if (
            not isinstance(self.minimum_recoil_distance, (int, float))
            or isinstance(self.minimum_recoil_distance, bool)
            or self.minimum_recoil_distance <= 0
        ):
            raise ConfigurationError("RecoilConfig minimum_recoil_distance must be positive.")

    @classmethod
    def from_json(cls, config_path: Path | str) -> "RecoilConfig":
        """Load immutable recoil configuration from an external JSON document."""
        path = Path(config_path)
        if not path.is_file():
            raise ConfigurationError(f"Recoil configuration was not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        except json.JSONDecodeError as error:
            raise ConfigurationError(f"Recoil configuration contains invalid JSON: {path}") from error
        required_fields = {"schema_version", "minimum_recoil_distance"}
        missing_fields = required_fields.difference(data)
        if missing_fields:
            raise ConfigurationError(
                "Recoil configuration is missing required fields: "
                f"{', '.join(sorted(missing_fields))}"
            )
        return cls(
            schema_version=data["schema_version"],
            minimum_recoil_distance=float(data["minimum_recoil_distance"]),
        )
