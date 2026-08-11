import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Optional

from .errors import DatasetConfigurationError
from .partition import DatasetPartition, PartitionName


def _hash_file(filepath: str) -> str:
    """Compute the SHA-256 hash of a file's contents."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        raise DatasetConfigurationError(f"Failed to hash dataset file {filepath}: {e}")


@dataclass(frozen=True)
class DatasetManifest:
    """
    Deterministic configuration and identity of a historical dataset.
    """
    dataset_id: str
    instrument: str
    timeframe: str
    timezone: str
    schema_version: str
    partitions: List[DatasetPartition]

    def __post_init__(self):
        if not all(isinstance(v, str) and v.strip() for v in (self.dataset_id, self.instrument, self.timeframe, self.timezone, self.schema_version)):
            raise DatasetConfigurationError("All scalar fields in DatasetManifest must be non-empty strings.")
        
        if not self.partitions:
            raise DatasetConfigurationError("DatasetManifest must contain at least one partition.")
            
        # Verify no duplicate partition names
        seen_names = set()
        for partition in self.partitions:
            if partition.partition_name in seen_names:
                raise DatasetConfigurationError(f"Duplicate partition name {partition.partition_name.value} found.")
            seen_names.add(partition.partition_name)
            
        # Sort partitions chronologically by start_timestamp
        sorted_partitions = sorted(self.partitions, key=lambda p: p.start_timestamp)
        
        # Enforce that the provided partitions are already chronologically ordered
        if sorted_partitions != self.partitions:
            raise DatasetConfigurationError("Partitions must be defined in strict chronological order.")
            
        # Enforce no overlaps
        for i in range(len(self.partitions) - 1):
            current = self.partitions[i]
            next_part = self.partitions[i + 1]
            if current.end_timestamp > next_part.start_timestamp:
                raise DatasetConfigurationError(
                    f"Overlapping partitions detected: {current.partition_name.value} ends at {current.end_timestamp}, "
                    f"but {next_part.partition_name.value} starts at {next_part.start_timestamp}."
                )

    def get_partition(self, name: PartitionName) -> DatasetPartition:
        """Retrieve a specific partition by name."""
        for p in self.partitions:
            if p.partition_name == name:
                return p
        raise DatasetConfigurationError(f"Partition {name.value} not found in dataset {self.dataset_id}.")

    @property
    def fingerprint(self) -> str:
        """
        Deterministic cryptographic identity of the dataset contents and configuration.
        """
        manifest_dict = {
            "dataset_id": self.dataset_id,
            "instrument": self.instrument,
            "timeframe": self.timeframe,
            "timezone": self.timezone,
            "schema_version": self.schema_version,
            "partitions": [
                {
                    "partition_name": p.partition_name.value,
                    "start_timestamp": p.start_timestamp.isoformat(),
                    "end_timestamp": p.end_timestamp.isoformat(),
                    "source_uri": p.source_uri
                }
                for p in self.partitions
            ]
        }
        
        canonical_manifest = json.dumps(manifest_dict, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        
        hasher = hashlib.sha256()
        hasher.update(canonical_manifest.encode("utf-8"))
        
        # Hash referenced files in deterministic partition order
        for p in self.partitions:
            file_hash = _hash_file(p.source_uri)
            hasher.update(file_hash.encode("utf-8"))
            
        return f"sha256:{hasher.hexdigest()}"
