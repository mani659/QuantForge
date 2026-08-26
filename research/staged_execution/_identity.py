"""Staged economic execution — shared identity / hashing primitives.

ANCHORS
-------
* V2.0.1 protocol §4.4 (W4): preparation identity `PREP_<market>_<FULL_SHA256>`
  is a SHA-256 over a canonical, nine-field, byte-stable manifest.
* V2.0.1 protocol §4.3 (W2): market-median fallback universe = complete set of
  eligible per-minute quote aggregates for ALL observed minutes of the market.
* N2 (final re-audit): field 8 "canonical Stage-1 parameter manifest" must be
  enumerated deterministically at implementation time.  It is registered below
  as STAGE1_PARAMETER_KEYS / canonical_stage1_parameters().

Every value in the canonical manifest is reconstructable from the frozen
production inputs alone; no timestamps, machine paths, usernames, or
environment-dependent values are included.  This module is pure infrastructure:
it computes no economics.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import struct
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

STAGE1_SCHEMA_VERSION = "stage1.schema.v1"
PREP_CODE_SCHEMA_VERSION = "stage1.code.v1"
CANONICAL_ENCODING = "utf-8"
_CANONICAL_NEWLINE = "\n"
_CANONICAL_BOM = "\ufeff"


def sha256_file(path) -> str:
    """Streamed SHA-256 (1 MiB chunks) of a file, lower-case hex."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash_value(value: Any) -> str:
    """Canonical lexical normalization of a single field value.

    - SHA-256 digests -> lower-case hex (byte-identical reconstruction
      requires a chosen case; lower-case is chosen and registered here).
    - floats -> repr() (exact round-trip).
    - bools -> true/false.
    - everything else -> str().
    """
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


# ---------------------------------------------------------------------------
# W4 field 8 — canonical Stage-1 parameter manifest (N2 pinning)
# ---------------------------------------------------------------------------
# These are the registered, frozen constants of V1.1.0 §§4-14 (execution-bridge
# and viability-gate facts) plus the deterministic tick-quality rules of the
# execution bridge.  They are the ONLY parameters permitted to influence
# preparation.  No threshold is invented: every value below is already
# registered by the frozen V1.1.0 text implemented in run_ord_econ_v1.py.
# ---------------------------------------------------------------------------

STAGE1_PARAMETER_KEYS: List[str] = [
    "horizon_minutes",            # V1.1.0 §6  — 120 minute literal horizon
    "fallback_minutes",           # V1.1.0 §4  — ±5 minute fallback chain
    "min_sample",                 # V1.1.0 §13 — gate population floor (30)
    "commission_bp",              # V1.1.0 §7  — Model B sensitivity bands
    "slippage_bp",                # V1.1.0 §7  — Model B sensitivity bands
    "tb_offset_seconds",          # V1.1.0 §4  — T_B = anchor + 60 s
    "quote_timezone_utc_naive",   # tick convention: naive UTC
    "projection_timezone",        # OR window projection: America/New_York
    "or_london_minutes",          # London markets 03:00-03:29 ET (30 bars)
    "or_usa_minutes",             # USATECHIDXUSD 09:30-09:59 ET (30 bars)
    "or_min_bars",                # V1.1.0 — ≥30 M1 bars required
    "tick_bid_min",               # tick-quality: bid > 0
    "tick_ask_min",               # tick-quality: ask > 0
    "tick_bid_ask_order",         # tick-quality: bid <= ask
    "tick_finite_required",       # tick-quality: finite
    "range_check_abs_tol",        # V1.1.0 — max(1e-4, 1e-6*|width|)
    "range_check_rel_tol",        # V1.1.0 — 1e-6 relative tolerance
    "dev_oos_day_split",          # V1.1.0 §11 — floor(N/2) dev / rest OOS
]


def canonical_stage1_parameters(**overrides: Any) -> str:
    """Canonical, single-line, byte-stable serialization of the Stage-1
    parameter manifest (W4 field 8 value).  Fixed key order; every value is
    lexically normalized; list/tuple values are comma-joined primitives."""
    params: Dict[str, Any] = {
        "horizon_minutes": 120,
        "fallback_minutes": 5,
        "min_sample": 30,
        "commission_bp": [0.0, 2.0, 5.0, 10.0],
        "slippage_bp": [0.0, 2.0, 5.0],
        "tb_offset_seconds": 60,
        "quote_timezone_utc_naive": "UTC",
        "projection_timezone": "America/New_York",
        "or_london_minutes": (3, 0, 3, 29),
        "or_usa_minutes": (9, 30, 9, 59),
        "or_min_bars": 30,
        "tick_bid_min": 0.0,
        "tick_ask_min": 0.0,
        "tick_bid_ask_order": "bid_less_equal_ask",
        "tick_finite_required": True,
        "range_check_abs_tol": 1.0e-4,
        "range_check_rel_tol": 1.0e-6,
        "dev_oos_day_split": "floor_half",
    }
    params.update(overrides)
    parts = []
    for key in STAGE1_PARAMETER_KEYS:
        value = params[key]
        if isinstance(value, (list, tuple)):
            value = ",".join(canonical_hash_value(v) for v in value)
        parts.append(key + "=" + canonical_hash_value(value))
    return ";".join(parts)


# ---------------------------------------------------------------------------
# W4 §4.4.2 canonical nine-field input manifest
# ---------------------------------------------------------------------------

CANONICAL_MANIFEST_FIELDS: List[Tuple[str, str]] = [
    ("market", "market"),                                    # 1
    ("schema.version.stage1", "schema.stage1"),              # 2
    ("protocol.economic.sha256", "protocol.economic"),       # 3
    ("protocol.scientific.sha256", "protocol.scientific"),   # 4
    ("source.m1.sha256", "source.m1"),                       # 5
    ("source.tick.sha256", "source.tick"),                   # 6
    ("implementation.preparation.sha256", "implementation.prep"),  # 7
    ("parameters.stage1.manifest", "parameters.stage1"),     # 8
    ("code.schema.prep", "code.schema"),                     # 9
]


def build_canonical_manifest(
    market: str,
    economic_protocol_sha256: str,
    scientific_protocol_sha256: str,
    source_m1_sha256: str,
    source_tick_sha256: str,
    preparation_implementation_sha256: str,
    stage1_parameter_manifest: str | None = None,
    schema_stage1: str = STAGE1_SCHEMA_VERSION,
    code_schema_prep: str = PREP_CODE_SCHEMA_VERSION,
) -> bytes:
    """Serializes the canonical nine-field manifest for one market.

    Byte-stable `key=value\\n` lines, UTF-8 no BOM, fixed field order, single
    trailing newline after the last field, no timestamps/paths/usernames/env.
    """
    param_manifest = stage1_parameter_manifest or canonical_stage1_parameters()
    values = {
        "market": canonical_hash_value(market),
        "schema.stage1": canonical_hash_value(schema_stage1),
        "protocol.economic": canonical_hash_value(economic_protocol_sha256),
        "protocol.scientific": canonical_hash_value(scientific_protocol_sha256),
        "source.m1": canonical_hash_value(source_m1_sha256),
        "source.tick": canonical_hash_value(source_tick_sha256),
        "implementation.prep": canonical_hash_value(preparation_implementation_sha256),
        "parameters.stage1": param_manifest,
        "code.schema": canonical_hash_value(code_schema_prep),
    }
    lines = [key + "=" + values[lookup] for key, lookup in CANONICAL_MANIFEST_FIELDS]
    text = _CANONICAL_NEWLINE.join(lines) + _CANONICAL_NEWLINE
    if _CANONICAL_BOM in text:
        raise ValueError("Refusing to serialize BOM into canonical manifest.")
    return text.encode(CANONICAL_ENCODING)


def prep_identity(market: str, canonical_bytes: bytes) -> str:
    """Full preparation identity `PREP_<market>_<64-char upper hex>` (W4 §4.4.4)."""
    digest = hashlib.sha256(canonical_bytes).hexdigest().upper()
    return f"PREP_{canonical_hash_value(market).upper()}_{digest}"


def prep_hash_of(market: str, canonical_bytes: bytes) -> str:
    return prep_identity(market, canonical_bytes).split("_")[-1]


# ---------------------------------------------------------------------------
# Preparation-implementation hash (canonical field 7)
# ---------------------------------------------------------------------------

_PREP_SOURCE_FILES: List[str] = [
    "research/staged_execution/_identity.py",
    "research/staged_execution/_failure.py",
    "research/staged_execution/_stage_recorder.py",
    "research/staged_execution/stage1.py",
    "scripts/ord_econ_stage1_prepare.py",
]


def preparation_implementation_sha256(repo_root: Path) -> str:
    """Deterministic SHA-256 of the preparation-implementation source set.

    Hash = SHA-256 over concatenated `relpath\\0 sha256-hex\\n` entries in the
    fixed registered order.  Any change to the preparation implementation
    changes the hash and therefore the preparation identity (W4 field 7).
    """
    h = hashlib.sha256()
    for rel in _PREP_SOURCE_FILES:
        p = repo_root / rel
        if not p.is_file():
            raise FileNotFoundError(
                f"Preparation implementation file missing: {p} "
                f"(canonical field 7 requires every frozen source file)"
            )
        h.update(rel.encode(CANONICAL_ENCODING))
        h.update(b"\x00")
        h.update(sha256_file(p).encode(CANONICAL_ENCODING))
        h.update(b"\n")
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Fixed-width minute index + bounded-memory EXACT median
# ---------------------------------------------------------------------------
# The market-median fallback (W2) is the median over ALL eligible observed
# minutes.  To honor W1 (no O(number_of_minutes) table resident in Stage 1) we
# never load the column; we run a chunked external quickselect over the
# fixed-width minute-index file, reading bounded slices at a time.  The result
# matches numpy's median semantics (average of the two middle values when the
# population is even).
# ---------------------------------------------------------------------------

MINUTE_RECORD_FORMAT = "<QddI"  # epoch_min (u64), bid (f64), ask (f64), nticks (u32)
MINUTE_RECORD_SIZE = struct.calcsize(MINUTE_RECORD_FORMAT)
_CHUNK_RECS = 1 << 17  # 131072 records/values per internal buffer (~3 MiB)
_FLOAT_FILE_EXT = ".f64"


class _BufferedFloatWriter:
    """Bounded-RAM writer that flushes in CHUNK-sized batches (deterministic)."""

    def __init__(self, path: Path):
        self.path = path
        self._f = open(path, "wb")
        self._buf = bytearray(_CHUNK_RECS * 8)
        self._n = 0

    def write(self, value: float) -> None:
        struct.pack_into("<d", self._buf, self._n * 8, float(value))
        self._n += 1
        if self._n == _CHUNK_RECS:
            self._flush()

    def _flush(self) -> None:
        if self._n:
            self._f.write(memoryview(self._buf)[: self._n * 8])
            self._n = 0

    def close(self) -> None:
        self._flush()
        self._f.close()


def write_minute_index(path: Path, rows: Iterable[Tuple[int, float, float, int]]) -> None:
    """Appends fixed-width minute-index records: (epoch_min, bid, ask, nticks).

    Rows MUST arrive in strictly ascending epoch_min order (a chronological
    tick stream guarantees this).  Records are buffered in bounded batches; the
    caller never retains the table.
    """
    buf = bytearray(_CHUNK_RECS * MINUTE_RECORD_SIZE)
    n = 0
    with open(path, "ab") as f:
        for epoch_min, bid, ask, nticks in rows:
            struct.pack_into(MINUTE_RECORD_FORMAT, buf, n * MINUTE_RECORD_SIZE,
                             int(epoch_min), float(bid), float(ask), int(nticks))
            n += 1
            if n == _CHUNK_RECS:
                f.write(memoryview(buf)[: n * MINUTE_RECORD_SIZE])
                n = 0
        if n:
            f.write(memoryview(buf)[: n * MINUTE_RECORD_SIZE])


class MinuteIndex:
    """Read-only bounded-memory minute index.

    Presence / value lookup by binary search (single fixed-width record reads);
    median-of-column via an external, memory-capped quickselect.
    """

    def __init__(self, path: Path):
        self.path = Path(path)

    def __len__(self) -> int:
        return os.path.getsize(self.path) // MINUTE_RECORD_SIZE

    def _read_record(self, i: int):
        with open(self.path, "rb") as f:
            f.seek(i * MINUTE_RECORD_SIZE)
            raw = f.read(MINUTE_RECORD_SIZE)
        if len(raw) != MINUTE_RECORD_SIZE:
            raise ValueError(f"Corrupted minute index record at index {i}")
        return struct.unpack(MINUTE_RECORD_FORMAT, raw)

    def contains(self, epoch_min: int) -> bool:
        return self.get(epoch_min) is not None

    def get(self, epoch_min: int):
        """Returns (bid, ask, nticks) for the minute or None."""
        lo, hi = 0, len(self) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            rec = self._read_record(mid)
            cur = rec[0]
            if cur == epoch_min:
                return (float(rec[1]), float(rec[2]), int(rec[3]))
            if cur < epoch_min:
                lo = mid + 1
            else:
                hi = mid - 1
        return None

    def column_values(self, key: str) -> Iterable[float]:
        """Chunked stream of a float64 column (offset 8 = bid, 16 = ask)."""
        offset = 8 if key == "bid" else 16
        total = len(self)
        with open(self.path, "rb") as f:
            pos = 0
            while pos < total:
                take = min(_CHUNK_RECS, total - pos)
                f.seek(pos * MINUTE_RECORD_SIZE)
                data = f.read(take * MINUTE_RECORD_SIZE)
                if len(data) != take * MINUTE_RECORD_SIZE:
                    data = data + b"\x00" * (take * MINUTE_RECORD_SIZE - len(data))
                for i in range(take):
                    yield struct.unpack_from(MINUTE_RECORD_FORMAT, data,
                                             i * MINUTE_RECORD_SIZE)[1 if offset == 8 else 2]
                pos += take

    def median_of_column(self, key: str) -> float:
        """Exact median of the column (avg of middle two when even)."""
        return external_median(self.column_values(key))


# ---------------------------------------------------------------------------
# External exact median (bounded RAM, deterministic)
# ---------------------------------------------------------------------------

def _read_value_at(path: Path, idx: int) -> float:
    with open(path, "rb") as f:
        f.seek(idx * 8)
        raw = f.read(8)
    if len(raw) != 8:
        raise ValueError(f"Corrupted float file {path} at index {idx}")
    return struct.unpack("<d", raw)[0]


def _partition_range(src: Path, hi: int, pivot: float, out_dir: Path):
    """Partitions values[0:hi) of `src` into bounded lt/eq/gt files.

    Files are written into the dedicated per-call `out_dir` so recursion
    never truncates the file it is reading.  Returns (n_lt, n_eq).
    """
    lt = _BufferedFloatWriter(out_dir / ("lt" + _FLOAT_FILE_EXT))
    eq = _BufferedFloatWriter(out_dir / ("eq" + _FLOAT_FILE_EXT))
    gt = _BufferedFloatWriter(out_dir / ("gt" + _FLOAT_FILE_EXT))
    n_lt = n_eq = 0
    buf = bytearray(_CHUNK_RECS * 8)
    with open(src, "rb") as f:
        pos = 0
        while pos < hi:
            take = min(_CHUNK_RECS, hi - pos)
            f.seek(pos * 8)
            data = f.read(take * 8)
            if len(data) != take * 8:
                data = data + b"\x00" * (take * 8 - len(data))
            for i in range(take):
                v = struct.unpack_from("<d", data, i * 8)[0]
                if v < pivot:
                    lt.write(v)
                    n_lt += 1
                elif v == pivot:
                    eq.write(v)
                    n_eq += 1
                else:
                    gt.write(v)
            pos += take
    lt.close()
    eq.close()
    gt.close()
    return n_lt, n_eq


def _kth_value(path: Path, n: int, k: int, tmpdir: Path) -> float:
    """Deterministic bounded-RAM quickselect over values[0:n) of a float file."""
    if n == 1:
        return _read_value_at(path, 0)
    limit = 0
    while True:
        out_dir = tmpdir / f"k{limit}_{id(path) & 0xFFFF}"
        limit += 1
        if not out_dir.exists():
            break
    out_dir.mkdir()
    pivot = _read_value_at(path, n // 2)
    n_lt, n_eq = _partition_range(path, n, pivot, out_dir)
    try:
        if k < n_lt:
            return _kth_value(out_dir / ("lt" + _FLOAT_FILE_EXT), n_lt, k, tmpdir)
        if k < n_lt + n_eq:
            return pivot
        return _kth_value(
            out_dir / ("gt" + _FLOAT_FILE_EXT),
            n - n_lt - n_eq,
            k - n_lt - n_eq,
            tmpdir,
        )
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


def external_median(values: Iterable[float]) -> float:
    """Exact median of an arbitrary-length iterable of floats with bounded RAM.

    Values are materialized once to a temp float64 file (buffered, bounded),
    then the median is computed by deterministic external quickselect, matching
    numpy's median semantics (average of the two middle values when even).
    """
    tmpdir_root = Path(tempfile.mkdtemp(prefix="ord_median_"))
    try:
        values_file = tmpdir_root / ("values" + _FLOAT_FILE_EXT)
        writer = _BufferedFloatWriter(values_file)
        count = 0
        for v in values:
            writer.write(float(v))
            count += 1
        writer.close()
        if count == 0:
            raise ValueError("Cannot compute a median of zero values.")
        if count % 2 == 1:
            return _kth_value(values_file, count, count // 2, tmpdir_root)
        lower = _kth_value(values_file, count, count // 2 - 1, tmpdir_root)
        upper = _kth_value(values_file, count, count // 2, tmpdir_root)
        return (lower + upper) / 2.0
    finally:
        shutil.rmtree(tmpdir_root, ignore_errors=True)


def external_percentile(values: Iterable[float], pct: float) -> float:
    """Exact percentile of an arbitrary-length iterable of floats (bounded RAM).

    Mirrors numpy's linear-interpolation percentile convention on the order
    statistics: rank = (n-1)*pct; result = v[lo] + (v[lo+1] - v[lo]) * frac.
    """
    tmpdir_root = Path(tempfile.mkdtemp(prefix="ord_pct_"))
    try:
        values_file = tmpdir_root / ("values" + _FLOAT_FILE_EXT)
        writer = _BufferedFloatWriter(values_file)
        count = 0
        for v in values:
            writer.write(float(v))
            count += 1
        writer.close()
        if count == 0:
            raise ValueError("Cannot compute a percentile of zero values.")
        rank = (count - 1) * pct
        lo = int(rank // 1)
        frac = rank - lo
        lower = _kth_value(values_file, count, lo, tmpdir_root)
        if frac == 0 or lo == count - 1:
            return lower
        upper = _kth_value(values_file, count, lo + 1, tmpdir_root)
        return lower + (upper - lower) * frac
    finally:
        shutil.rmtree(tmpdir_root, ignore_errors=True)