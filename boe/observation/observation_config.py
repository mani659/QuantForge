"""Immutable external configuration contract for the Observation Policy."""

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Union

from boe.detector_errors import VersionMismatchError
from .observation_errors import ObservationConfigurationError

SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class ObservationConfig:
    """Immutable external configuration for Observation Policy."""

    schema_version: str
    max_frames: int
    max_duration: float  # seconds or abstract time units

    def __post_init__(self) -> None:
        """Validate config constraints to preserve deterministic behavior."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VersionMismatchError("ObservationConfig schema_version must be semantic versioning.")
        if not isinstance(self.max_frames, int) or isinstance(self.max_frames, bool) or self.max_frames <= 0:
            raise ObservationConfigurationError("max_frames must be a positive integer.")
        if not isinstance(self.max_duration, (int, float)) or isinstance(self.max_duration, bool) or self.max_duration <= 0.0:
            raise ObservationConfigurationError("max_duration must be a positive number.")

    @classmethod
    def from_json(cls, config_path: Union[Path, str]) -> "ObservationConfig":
        """Load immutable configuration from an external JSON file."""
        path = Path(config_path)
        if not path.is_file():
            raise ObservationConfigurationError(f"Observation configuration file not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as error:
            raise ObservationConfigurationError(f"Observation configuration contains invalid JSON: {path}") from error

        required_fields = {"schema_version", "max_frames", "max_duration"}
        missing_fields = required_fields.difference(data)
        if missing_fields:
            raise ObservationConfigurationError(
                f"Observation configuration is missing required fields: {', '.join(sorted(missing_fields))}"
            )
        return cls(
            schema_version=data["schema_version"],
            max_frames=int(data["max_frames"]),
            max_duration=float(data["max_duration"]),
        )
