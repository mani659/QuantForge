"""Canonical Tick Data Canonicalizer — V1.

Transforms raw MT5 tick CSVs into a governed Parquet representation
suitable for quote-level microstructure research.

Governing specification: QUANTFORGE_CANONICAL_TICK_DATA_SPECIFICATION_V1
"""

from __future__ import annotations

import hashlib
import json
import struct
import sys
import time
from pathlib import Path
from typing import Optional

import pyarrow as pa
import pyarrow.parquet as pq


SCHEMA = pa.schema([
    ("source_row_ordinal", pa.int64()),
    ("date", pa.string()),
    ("time", pa.string()),
    ("bid", pa.float64()),
    ("ask", pa.float64()),
    ("last", pa.float64()),
    ("vol", pa.float64()),
    ("mid", pa.float64()),
    ("spread", pa.float64()),
])

SOURCE_COLUMNS = ["date", "time", "bid", "ask", "last", "vol"]
NUMERIC_COLUMNS = ["bid", "ask", "last", "vol"]

CHUNK_SIZE = 200_000


class CanonicalTickCanonicalizer:
    """Streaming, bounded-memory canonicalizer for MT5 tick CSVs.

    Produces deterministic Parquet partitions with provenance manifest.
    """

    def __init__(
        self,
        output_dir: Path,
        symbol: str,
        chunk_size: int = CHUNK_SIZE,
        compression: str = "snappy",
    ) -> None:
        self.output_dir = Path(output_dir)
        self.symbol = symbol
        self.chunk_size = chunk_size
        self.compression = compression

        self.current_partition: Optional[str] = None
        self.writer: Optional[pq.ParquetWriter] = None

        self.total_rows = 0
        self.rejected_rows = 0
        self.duplicate_timestamp_rows = 0
        self.bid_ask_inverted_rows = 0
        self.zero_price_rows = 0
        self.negative_price_rows = 0
        self.null_last_rows = 0

        self.partition_inventory: list[str] = []
        self.partition_row_counts: dict[str, int] = {}

        self._reset_buffer()
        self._reset_hashers()

        self._first_timestamp: Optional[str] = None
        self._last_timestamp: Optional[str] = None
        self._prev_timestamp: Optional[str] = None

    def _reset_buffer(self) -> None:
        self._buffer: dict[str, list] = {k: [] for k in SCHEMA.names}
        self._buffer_count = 0

    def _reset_hashers(self) -> None:
        self._hashers = {name: hashlib.sha256() for name in SOURCE_COLUMNS}

    def _hash_numeric(self, name: str, val: float) -> None:
        self._hashers[name].update(struct.pack("<d", val))

    def _hash_string(self, name: str, val: str) -> None:
        encoded = val.encode("utf-8")
        self._hashers[name].update(struct.pack("<I", len(encoded)) + encoded)

    def _flush_buffer(self) -> None:
        if self._buffer_count == 0:
            return
        table = pa.table(self._buffer, schema=SCHEMA)
        self.writer.write_table(table)
        self._reset_buffer()

    def _close_writer(self) -> None:
        self._flush_buffer()
        if self.writer is not None:
            self.writer.close()
            self.writer = None

    def _open_partition(self, yyyymm: str) -> None:
        self._close_writer()
        self.current_partition = yyyymm
        part_dir = self.output_dir / self.symbol
        part_dir.mkdir(parents=True, exist_ok=True)
        part_path = part_dir / f"{yyyymm}.parquet"
        self.writer = pq.ParquetWriter(
            part_path, self.SCHEMA, compression=self.compression
        )
        self.partition_inventory.append(f"{yyyymm}.parquet")
        self.partition_row_counts[yyyymm] = 0

    @property
    def SCHEMA(self) -> pa.schema:
        return SCHEMA

    def process_file(self, input_csv: Path) -> dict:
        """Process a raw tick CSV into canonical Parquet partitions."""
        input_csv = Path(input_csv).resolve()
        if not input_csv.exists():
            raise FileNotFoundError(f"Source CSV not found: {input_csv}")

        source_sha = self._compute_file_sha256(input_csv)
        start_time = time.time()

        with open(input_csv, "rb") as f:
            for line_bytes in f:
                line = line_bytes.decode("utf-8").strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 6:
                    self.rejected_rows += 1
                    continue

                date_str, time_str = parts[0], parts[1]
                bid_str, ask_str, last_str, vol_str = (
                    parts[2], parts[3], parts[4], parts[5]
                )

                try:
                    bid_val = float(bid_str)
                    ask_val = float(ask_str)
                    vol_val = float(vol_str)
                    last_val = float(last_str) if last_str.strip() else None
                except ValueError:
                    self.rejected_rows += 1
                    continue

                if bid_val < 0 or ask_val < 0:
                    self.negative_price_rows += 1
                    self.rejected_rows += 1
                    continue

                if bid_val == 0 or ask_val == 0:
                    self.zero_price_rows += 1
                    self.rejected_rows += 1
                    continue

                if ask_val < bid_val:
                    self.bid_ask_inverted_rows += 1
                    self.rejected_rows += 1
                    continue

                if last_val is None:
                    self.null_last_rows += 1

                ts_key = f"{date_str} {time_str}"
                if self._prev_timestamp is not None and ts_key < self._prev_timestamp:
                    self.rejected_rows += 1
                    continue
                if ts_key == self._prev_timestamp:
                    self.duplicate_timestamp_rows += 1
                self._prev_timestamp = ts_key

                if self._first_timestamp is None:
                    self._first_timestamp = ts_key
                self._last_timestamp = ts_key

                yyyymm = date_str[:6]
                if len(yyyymm) != 6 or not yyyymm.isdigit():
                    self.rejected_rows += 1
                    continue

                if self.current_partition != yyyymm:
                    self._open_partition(yyyymm)

                mid_val = (bid_val + ask_val) / 2.0
                spread_val = ask_val - bid_val

                ordinal = self.total_rows
                self._buffer["source_row_ordinal"].append(ordinal)
                self._buffer["date"].append(date_str)
                self._buffer["time"].append(time_str)
                self._buffer["bid"].append(bid_val)
                self._buffer["ask"].append(ask_val)
                self._buffer["last"].append(last_val)
                self._buffer["vol"].append(vol_val)
                self._buffer["mid"].append(mid_val)
                self._buffer["spread"].append(spread_val)

                self._hash_string("date", date_str)
                self._hash_string("time", time_str)
                self._hash_numeric("bid", bid_val)
                self._hash_numeric("ask", ask_val)
                self._hash_numeric("last", last_val if last_val is not None else 0.0)
                self._hash_numeric("vol", vol_val)

                self.total_rows += 1
                self._buffer_count += 1
                self.partition_row_counts[yyyymm] += 1

                if self._buffer_count >= self.chunk_size:
                    self._flush_buffer()

        self._close_writer()

        elapsed = time.time() - start_time
        manifest = self._build_manifest(
            source_csv=input_csv,
            source_sha=source_sha,
            elapsed_seconds=elapsed,
        )

        manifest_path = self.output_dir / self.symbol / "manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest

    def _build_manifest(
        self,
        source_csv: Path,
        source_sha: str,
        elapsed_seconds: float,
    ) -> dict:
        column_hashes = {}
        for name in SOURCE_COLUMNS:
            column_hashes[name] = self._hashers[name].hexdigest()

        spec_path = (
            Path(__file__).resolve().parents[2]
            / "output"
            / "research_discovery"
            / "QUANTFORGE_CANONICAL_TICK_DATA_SPECIFICATION_V1.md"
        )
        spec_sha = "SPEC_NOT_FOUND"
        if spec_path.exists():
            with open(spec_path, "rb") as f:
                spec_sha = hashlib.sha256(f.read()).hexdigest()

        impl_path = Path(__file__).resolve()
        with open(impl_path, "rb") as f:
            impl_sha = hashlib.sha256(f.read()).hexdigest()

        return {
            "symbol": self.symbol,
            "schema_version": "V1",
            "source_file": str(source_csv.name),
            "source_sha256": source_sha,
            "specification_sha256": spec_sha,
            "implementation_sha256": impl_sha,
            "total_rows": self.total_rows,
            "rejected_rows": self.rejected_rows,
            "duplicate_timestamp_rows": self.duplicate_timestamp_rows,
            "bid_ask_inverted_rows": self.bid_ask_inverted_rows,
            "negative_price_rows": self.negative_price_rows,
            "zero_price_rows": self.zero_price_rows,
            "null_last_rows": self.null_last_rows,
            "first_timestamp": self._first_timestamp,
            "last_timestamp": self._last_timestamp,
            "partitions": self.partition_inventory,
            "partition_row_counts": self.partition_row_counts,
            "column_hashes": column_hashes,
            "compression": self.compression,
            "elapsed_seconds": round(elapsed_seconds, 2),
        }

    @staticmethod
    def _compute_file_sha256(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Canonical Tick Data Canonicalizer V1"
    )
    parser.add_argument("input_csv", help="Path to raw tick CSV")
    parser.add_argument("output_dir", help="Output directory for Parquet")
    parser.add_argument("symbol", help="Symbol name (e.g., USATECHIDXUSD)")
    parser.add_argument(
        "--compression", default="snappy", help="Parquet compression"
    )
    parser.add_argument(
        "--chunk-size", type=int, default=CHUNK_SIZE, help="Rows per chunk"
    )
    args = parser.parse_args()

    canonicalizer = CanonicalTickCanonicalizer(
        output_dir=Path(args.output_dir),
        symbol=args.symbol,
        chunk_size=args.chunk_size,
        compression=args.compression,
    )
    manifest = canonicalizer.process_file(Path(args.input_csv))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
