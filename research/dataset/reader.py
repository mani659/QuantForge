import csv
import math
import zoneinfo
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Iterable, Mapping

from .errors import DatasetReaderError
from .partition import DatasetPartition


class PartitionReaderContract(ABC):
    """Abstraction for reading raw historical data from a partition."""
    @abstractmethod
    def read(self) -> Iterable[Mapping[str, Any]]:
        pass


class CSVPartitionReader(PartitionReaderContract):
    """
    Streaming CSV reader that ensures deterministic memory usage O(1)
    and strictly enforces partition boundaries, data types, and required schema.
    """
    def __init__(self, partition: DatasetPartition, timezone_str: str):
        self.partition = partition
        try:
            self.tz = zoneinfo.ZoneInfo(timezone_str)
        except Exception as e:
            raise DatasetReaderError(f"Invalid timezone {timezone_str}: {e}")

    def read(self) -> Iterable[Mapping[str, Any]]:
        required_fields = {"timestamp", "open", "high", "low", "close", "volume"}
        
        try:
            with open(self.partition.source_uri, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                
                # Verify required columns exist
                if not reader.fieldnames or not required_fields.issubset(set(reader.fieldnames)):
                    missing = required_fields - set(reader.fieldnames or [])
                    raise DatasetReaderError(f"Missing required columns in CSV: {missing}")
                
                for row_idx, row in enumerate(reader, start=1):
                    # Fail fast if required fields are empty
                    if not all(row.get(f) for f in required_fields):
                        raise DatasetReaderError(f"Row {row_idx}: Missing data in required fields {required_fields}.")
                        
                    # Parse timestamp (expected strictly as ISO format in naive time)
                    ts_str = row["timestamp"]
                    try:
                        dt_naive = datetime.fromisoformat(ts_str)
                    except ValueError as e:
                        raise DatasetReaderError(f"Row {row_idx}: Invalid timestamp format '{ts_str}'. Expected ISO 8601: {e}")
                        
                    if dt_naive.tzinfo is not None:
                        raise DatasetReaderError(f"Row {row_idx}: Source timestamp '{ts_str}' should be timezone-naive.")
                        
                    # Attach timezone and normalize to UTC
                    dt_aware = dt_naive.replace(tzinfo=self.tz)
                    dt_utc = dt_aware.astimezone(zoneinfo.ZoneInfo("UTC"))
                    
                    # Apply scientific boundary: [start, end)
                    if dt_utc < self.partition.start_timestamp:
                        continue
                    if dt_utc >= self.partition.end_timestamp:
                        continue
                        
                    # Parse OHLCV explicitly to ensure numerical validity
                    parsed_row: dict[str, Any] = {"timestamp": dt_utc}
                    for field in ["open", "high", "low", "close", "volume"]:
                        try:
                            val = float(row[field])
                            if math.isnan(val) or math.isinf(val):
                                raise DatasetReaderError(f"Row {row_idx}: NaN or Inf detected in field '{field}'.")
                            parsed_row[field] = val
                        except ValueError:
                            raise DatasetReaderError(f"Row {row_idx}: Invalid numeric value '{row[field]}' in field '{field}'.")
                            
                    # Preserve any arbitrary extra columns as strings
                    for k, v in row.items():
                        if k not in required_fields:
                            parsed_row[k] = v
                            
                    yield parsed_row
                    
        except FileNotFoundError:
            raise FileNotFoundError(f"Partition source file not found: {self.partition.source_uri}")
