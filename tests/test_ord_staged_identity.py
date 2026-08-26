"""Identity / hashing / bounded external-statistics tests (V2.0.1 §4.4, W4)."""

import os
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.staged_execution._identity import (  # noqa: E402
    MINUTE_RECORD_FORMAT,
    MinuteIndex,
    STAGE1_PARAMETER_KEYS,
    build_canonical_manifest,
    canonical_stage1_parameters,
    external_median,
    external_percentile,
    prep_hash_of,
    prep_identity,
    preparation_implementation_sha256,
    sha256_bytes,
    sha256_file,
    write_minute_index,
)

ECON_SHA = "8f45d7f82c80b7131c958c158f448520fef6927d49f9eb844fbbd55e35395663"
SCI_SHA = "85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06"
IMPL_SHA = "ab" * 32


def _manifest_bytes(market: str = "XAUUSD") -> bytes:
    return build_canonical_manifest(
        market=market,
        economic_protocol_sha256=ECON_SHA,
        scientific_protocol_sha256=SCI_SHA,
        source_m1_sha256="11" * 32,
        source_tick_sha256="22" * 32,
        preparation_implementation_sha256=IMPL_SHA,
    )


def test_canonical_manifest_byte_stable():
    a = _manifest_bytes()
    b = _manifest_bytes()
    assert a == b
    assert a.endswith(b"\n")
    assert a.count(b"\n") == 9
    assert b"\ufeff" not in a
    assert b"timestamp" not in a.lower() and b"path" not in a.lower()


def test_canonical_manifest_field_order():
    text = _manifest_bytes().decode("utf-8")
    lines = text.splitlines()
    assert len(lines) == 9
    assert lines[0].startswith("market=")
    assert lines[1].startswith("schema.version.stage1=")
    assert lines[2].startswith("protocol.economic.sha256=")
    assert lines[3].startswith("protocol.scientific.sha256=")
    assert lines[4].startswith("source.m1.sha256=")
    assert lines[5].startswith("source.tick.sha256=")
    assert lines[6].startswith("implementation.preparation.sha256=")
    assert lines[7].startswith("parameters.stage1.manifest=")
    assert lines[8].startswith("code.schema.prep=")


def test_canonical_manifest_digest_case_lower_hex():
    text = _manifest_bytes().decode("utf-8")
    for line in text.splitlines():
        if line.startswith(("protocol.", "source.", "implementation.prep")):
            value = line.split("=", 1)[1]
            assert value == value.lower()


def test_prep_identity_format():
    ident = prep_identity("xauusd", _manifest_bytes())
    assert ident.startswith("PREP_XAUUSD_")
    digest = ident.split("_")[-1]
    assert len(digest) == 64
    assert digest == digest.upper()
    assert prep_hash_of("xauusd", _manifest_bytes()) == digest


def test_identity_changes_with_market():
    a = prep_identity("XAUUSD", _manifest_bytes("XAUUSD"))
    b = prep_identity("XAGUSD", _manifest_bytes("XAGUSD"))
    assert a != b


def test_identity_rejects_bom():
    with pytest.raises(ValueError):
        build_canonical_manifest(
            market="XAUUSD",
            economic_protocol_sha256=ECON_SHA,
            scientific_protocol_sha256=SCI_SHA,
            source_m1_sha256="11" * 32,
            source_tick_sha256="22" * 32,
            preparation_implementation_sha256=IMPL_SHA,
            stage1_parameter_manifest="k=v;\ufeffk2=v2",
        )


def test_stage1_parameter_manifest_registered_values():
    s = canonical_stage1_parameters()
    assert "horizon_minutes=120" in s
    assert "fallback_minutes=5" in s
    assert "min_sample=30" in s
    assert "commission_bp=0.0,2.0,5.0,10.0" in s
    assert "slippage_bp=0.0,2.0,5.0" in s
    assert "tb_offset_seconds=60" in s
    assert "dev_oos_day_split=floor_half" in s
    keys = [part.split("=")[0] for part in s.split(";")]
    assert keys == STAGE1_PARAMETER_KEYS


def test_external_median_matches_numpy():
    rng = np.random.default_rng(7)
    for n in (1, 2, 3, 10, 11, 999):
        vals = rng.normal(size=n).tolist()
        assert external_median(vals) == float(np.median(vals))


def test_external_median_even_average_of_middle():
    assert external_median([1.0, 2.0]) == 1.5
    assert external_median([5.0, 1.0, 3.0, 2.0, 9.0, 4.0]) == float(np.median([5, 1, 3, 2, 9, 4]))


def test_external_median_repeated_values():
    vals = [7.0] * 1000 + [3.0] * 1000
    assert external_median(vals) == 5.0  # 3.0 x1000 then 7.0 x1000 -> mid average


def test_external_median_empty_raises():
    with pytest.raises(ValueError):
        external_median([])


def test_external_percentile_matches_numpy():
    rng = np.random.default_rng(11)
    vals = rng.normal(size=1000).tolist()
    for pct in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0):
        assert external_percentile(vals, pct) == pytest.approx(
            float(np.percentile(vals, pct * 100))
        )


def test_median_is_constant_memory(tmp_path):
    # 200k values, small buckets; verify exactness, not RAM blowup.
    rng = np.random.default_rng(3)
    vals = rng.normal(size=200_000).tolist()
    assert external_median(vals) == pytest.approx(float(np.median(vals)), rel=1e-12)


def test_write_minute_index_and_lookup(tmp_path):
    idx_path = tmp_path / "minute_index.bin"
    rows = [(1000 + i, float(i), float(i) + 0.1, 1) for i in range(50)]
    write_minute_index(idx_path, rows)
    idx = MinuteIndex(idx_path)
    assert len(idx) == 50
    assert idx.get(1000) == (0.0, 0.1, 1)
    assert idx.get(1049) == (49.0, 49.1, 1)
    assert idx.get(1050) is None
    assert idx.contains(1030)
    assert not idx.contains(999)


def test_minute_index_median_of_column(tmp_path):
    idx_path = tmp_path / "minute_index.bin"
    rows = [(1000 + i, float(i), float(2 * i), 1) for i in range(100)]
    write_minute_index(idx_path, rows)
    idx = MinuteIndex(idx_path)
    assert idx.median_of_column("bid") == float(np.median(list(range(100))))
    assert idx.median_of_column("ask") == float(np.median([2 * i for i in range(100)]))


def test_minute_index_corruption_returns_none(tmp_path):
    idx_path = tmp_path / "minute_index.bin"
    write_minute_index(idx_path, [(1000, 1.0, 1.1, 1)])
    assert len(MinuteIndex(idx_path)) == 1
    idx_path.write_bytes(b"\x00" * 4)  # size no longer a record multiple
    assert len(MinuteIndex(idx_path)) == 0
    assert MinuteIndex(idx_path).get(1000) is None


def test_sha256_bytes_known_vector():
    assert sha256_bytes(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_sha256_file_match(tmp_path):
    p = tmp_path / "f.txt"
    p.write_bytes(b"hello")
    assert sha256_file(p) == sha256_bytes(b"hello")


def test_preparation_implementation_sha256_deterministic():
    assert preparation_implementation_sha256(ROOT) == preparation_implementation_sha256(ROOT)
    assert len(preparation_implementation_sha256(ROOT)) == 64


def test_preparation_implementation_sha256_missing_file():
    with pytest.raises(FileNotFoundError):
        preparation_implementation_sha256(ROOT / "does_not_exist_xyz")


def test_record_size_exact():
    import struct
    assert struct.calcsize(MINUTE_RECORD_FORMAT) == 28  # <QddI = 8+8+8+4