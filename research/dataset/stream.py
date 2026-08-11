from typing import Iterable

from boe.deployment.historical_adapter import HistoricalMarketAdapter
from boe.temporal.environment_snapshot import EnvironmentSnapshot

from .manifest import DatasetManifest
from .partition import PartitionName
from .reader import CSVPartitionReader


def create_snapshot_stream(
    manifest: DatasetManifest, 
    partition_name: PartitionName
) -> Iterable[EnvironmentSnapshot]:
    """
    Creates a deterministic, forward-only streaming iterator of EnvironmentSnapshots.
    
    This factory connects the Dataset Foundation to the existing HistoricalMarketAdapter,
    ensuring that raw historical data is parsed, bounded, validated, and translated 
    into immutable snapshots without loading the entire dataset into memory.
    """
    partition = manifest.get_partition(partition_name)
    reader = CSVPartitionReader(partition, manifest.timezone)
    adapter = HistoricalMarketAdapter(
        dataset_id=manifest.dataset_id,
        instrument=manifest.instrument,
        timeframe=manifest.timeframe,
        schema_version=manifest.schema_version
    )
    
    for raw_row in reader.read():
        yield adapter.translate(raw_row)
