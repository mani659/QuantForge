"""Tests for the Canonical Tick Data Canonicalizer V1."""

import json
import shutil
from pathlib import Path

import pyarrow.parquet as pq
import pytest

from scripts.data.tick_canonicalizer import CanonicalTickCanonicalizer, SCHEMA


@pytest.fixture
def tmp_out(tmp_path):
    d = tmp_path / "canonical_output"
    d.mkdir()
    yield d
    if d.exists():
        shutil.rmtree(d)


def _write_csv(path: Path, rows: list[list[str]]) -> None:
    with open(path, "w") as f:
        for r in rows:
            f.write(",".join(r) + "\n")


class TestSchema:
    def test_schema_has_all_fields(self):
        names = SCHEMA.names
        assert "source_row_ordinal" in names
        assert "date" in names
        assert "time" in names
        assert "bid" in names
        assert "ask" in names
        assert "last" in names
        assert "vol" in names
        assert "mid" in names
        assert "spread" in names

    def test_schema_count(self):
        assert len(SCHEMA) == 9


class TestBasicConversion:
    def test_single_row(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [["20210101", "09:30:00", "1.1000", "1.1005", "1.1002", "10"]])

        c = CanonicalTickCanonicalizer(tmp_out, "TEST")
        m = c.process_file(csv)

        assert m["total_rows"] == 1
        assert m["rejected_rows"] == 0
        part = tmp_out / "TEST" / "202101.parquet"
        assert part.exists()

        t = pq.read_table(part)
        assert t.num_rows == 1
        assert t.column("bid").to_pylist()[0] == 1.1
        assert t.column("ask").to_pylist()[0] == 1.1005
        assert t.column("mid").to_pylist()[0] == pytest.approx(1.10025)
        assert t.column("spread").to_pylist()[0] == pytest.approx(0.0005)
        assert t.column("source_row_ordinal").to_pylist()[0] == 0

    def test_multi_partition(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210115", "10:00:00", "100.0", "100.5", "100.2", "1"],
            ["20210215", "10:00:00", "200.0", "200.5", "200.2", "2"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "MULTI")
        m = c.process_file(csv)

        assert m["total_rows"] == 2
        assert len(m["partitions"]) == 2
        assert "202101.parquet" in m["partitions"]
        assert "202102.parquet" in m["partitions"]
        assert m["partition_row_counts"]["202101"] == 1
        assert m["partition_row_counts"]["202102"] == 1


class TestDuplicates:
    def test_duplicate_timestamps_preserved(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "1.0", "1.1", "1.05", "1"],
            ["20210101", "09:30:00", "1.01", "1.11", "1.06", "2"],
            ["20210101", "09:30:00", "1.02", "1.12", "1.07", "3"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "DUP")
        m = c.process_file(csv)

        assert m["total_rows"] == 3
        assert m["duplicate_timestamp_rows"] == 2

        t = pq.read_table(tmp_out / "DUP" / "202101.parquet")
        assert t.num_rows == 3
        bids = t.column("bid").to_pylist()
        assert bids == [1.0, 1.01, 1.02]


class TestQualityGates:
    def test_ask_less_than_bid_rejected(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "1.1", "1.0", "1.05", "1"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "INV")
        m = c.process_file(csv)

        assert m["total_rows"] == 0
        assert m["bid_ask_inverted_rows"] == 1

    def test_zero_price_rejected(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "0.0", "1.0", "0.5", "1"],
            ["20210101", "09:30:01", "1.0", "0.0", "0.5", "1"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "ZERO")
        m = c.process_file(csv)

        assert m["total_rows"] == 0
        assert m["zero_price_rows"] == 2

    def test_negative_price_rejected(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "-1.0", "1.0", "0.0", "1"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "NEG")
        m = c.process_file(csv)

        assert m["total_rows"] == 0
        assert m["negative_price_rows"] == 1

    def test_malformed_row_rejected(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "not_a_number", "1.0", "0.5", "1"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "MAL")
        m = c.process_file(csv)

        assert m["total_rows"] == 0
        assert m["rejected_rows"] == 1

    def test_wrong_column_count_rejected(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "1.0"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "COL")
        m = c.process_file(csv)

        assert m["total_rows"] == 0
        assert m["rejected_rows"] == 1


class TestNullableLast:
    def test_null_last_preserved(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "1.0", "1.1", "", "1"],
            ["20210101", "09:30:01", "1.0", "1.1", "1.05", "1"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "NULL")
        m = c.process_file(csv)

        t = pq.read_table(tmp_out / "NULL" / "202101.parquet")
        lasts = t.column("last").to_pylist()
        assert lasts[0] is None
        assert lasts[1] == 1.05
        assert m["null_last_rows"] == 1


class TestProvenance:
    def test_manifest_has_required_fields(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [["20210101", "09:30:00", "1.0", "1.1", "1.05", "1"]])

        c = CanonicalTickCanonicalizer(tmp_out, "PROV")
        m = c.process_file(csv)

        assert "symbol" in m
        assert "schema_version" in m
        assert "source_sha256" in m
        assert "specification_sha256" in m
        assert "implementation_sha256" in m
        assert "total_rows" in m
        assert "rejected_rows" in m
        assert "partitions" in m
        assert "column_hashes" in m
        assert m["symbol"] == "PROV"
        assert m["schema_version"] == "V1"

    def test_manifest_persisted_to_disk(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [["20210101", "09:30:00", "1.0", "1.1", "1.05", "1"]])

        c = CanonicalTickCanonicalizer(tmp_out, "DISK")
        c.process_file(csv)

        manifest_path = tmp_out / "DISK" / "manifest.json"
        assert manifest_path.exists()
        with open(manifest_path) as f:
            m = json.load(f)
        assert m["total_rows"] == 1


class TestReproducibility:
    def test_deterministic_column_hashes(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210101", "09:30:00", "1.0", "1.1", "1.05", "1"],
            ["20210101", "09:30:01", "1.01", "1.11", "1.06", "2"],
        ])

        out1 = tmp_out / "run1"
        c1 = CanonicalTickCanonicalizer(out1, "REPR")
        m1 = c1.process_file(csv)

        out2 = tmp_out / "run2"
        c2 = CanonicalTickCanonicalizer(out2, "REPR", compression="none")
        m2 = c2.process_file(csv)

        assert m1["column_hashes"] == m2["column_hashes"]
        assert m1["total_rows"] == m2["total_rows"]


class TestChunkedProcessing:
    def test_large_file_chunked(self, tmp_out):
        csv = tmp_out / "big.csv"
        with open(csv, "w") as f:
            for i in range(500_000):
                f.write(f"20210101,09:30:00,{1.0 + i * 0.000001},{1.1 + i * 0.000001},1.05,1\n")

        c = CanonicalTickCanonicalizer(tmp_out, "CHUNK", chunk_size=100_000)
        m = c.process_file(csv)

        assert m["total_rows"] == 500_000
        assert m["rejected_rows"] == 0
        t = pq.read_table(tmp_out / "CHUNK" / "202101.parquet")
        assert t.num_rows == 500_000


class TestOutofOrder:
    def test_out_of_order_rejected(self, tmp_out):
        csv = tmp_out / "ticks.csv"
        _write_csv(csv, [
            ["20210102", "09:30:00", "1.0", "1.1", "1.05", "1"],
            ["20210101", "09:30:00", "1.0", "1.1", "1.05", "1"],
        ])

        c = CanonicalTickCanonicalizer(tmp_out, "OOO")
        m = c.process_file(csv)

        assert m["total_rows"] == 1
        assert m["rejected_rows"] == 1
