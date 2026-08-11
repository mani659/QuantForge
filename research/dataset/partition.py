from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from .errors import DatasetConfigurationError


class PartitionName(Enum):
    TRAIN = "TRAIN"
    VALIDATION = "VALIDATION"
    TEST = "TEST"


@dataclass(frozen=True)
class DatasetPartition:
    """
    Explicit boundary definition for a historical dataset partition.
    Represents [start_timestamp, end_timestamp).
    """
    partition_name: PartitionName
    start_timestamp: datetime
    end_timestamp: datetime
    source_uri: str

    def __post_init__(self):
        if not isinstance(self.partition_name, PartitionName):
            raise DatasetConfigurationError("partition_name must be a PartitionName enum.")
        
        if not isinstance(self.start_timestamp, datetime) or not isinstance(self.end_timestamp, datetime):
            raise DatasetConfigurationError("start_timestamp and end_timestamp must be datetime objects.")
        
        if self.start_timestamp.tzinfo is None or self.end_timestamp.tzinfo is None:
            raise DatasetConfigurationError("Timestamps must be timezone-aware.")
            
        if self.start_timestamp >= self.end_timestamp:
            raise DatasetConfigurationError(f"start_timestamp ({self.start_timestamp}) must be strictly before end_timestamp ({self.end_timestamp}).")
        
        if not isinstance(self.source_uri, str) or not self.source_uri.strip():
            raise DatasetConfigurationError("source_uri must be a non-empty string.")

    def contains(self, timestamp: datetime) -> bool:
        """
        Check if a timestamp falls within this partition's [start, end) bounds.
        """
        if timestamp.tzinfo is None:
            raise DatasetConfigurationError("Cannot check bounds for a timezone-naive timestamp.")
        return self.start_timestamp <= timestamp < self.end_timestamp
