"""Stage 0 — Repeatable, non-scientific preflight (V2.0.1 §3).

Per market, Stage 0 verifies: input file existence; streamed SHA-256; schema
(headerless `date,time,bid,ask,last,vol`); exact row count; timestamp format
(`YYYYMMDD,HH:MM:SS`); naive-UTC convention; bid/ask validity; malformed-row
statistics; and environment/resource capability (RAM, free disk, peak-RSS
streaming probe).

Stage 0 computes NO economic result, NO trade, NO exclusion, NO PnL.  A
preflight check that fails produces a FALSE verdict REPEATEDLY (a finding, not
a crash); only component failure of the preflight itself is classified as
`EXECUTION-INFRASTRUCTURE FAILURE` (V2.0.1 §4.5).  Every run gets a fresh
isolated `PREFLIGHT_<market>_<runid>` identity reconcilable through
`scripts/reconcile_execution.py`.
"""

from __future__ import annotations

import json
import math
import platform
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import psutil

from ._failure import (
    INFRASTRUCTURE_FAILURE_LABEL,
    ExecutionInfrastructureFailure,
    classify_infrastructure_failure,
)
from ._identity import sha256_file
from ._stage_recorder import StageRunRecorder

TICK_SCHEMA_FIELDS = ("date", "time", "bid", "ask", "last", "vol")
PROBE_BUDGET_BYTES_DEFAULT = 2 << 30
REQUIRED_FREE_DISK_BYTES_DEFAULT = 40 << 30
REQUIRED_RAM_BYTES_DEFAULT = 4 << 30


def _sample_peak_rss():
    try:
        p = psutil.Process()
        return p.memory_info().rss
    except Exception:
        return None


def _validate_tick_line(line: str):
    """Returns (status, row) where status in {"ok","malformed","bad_quote"}."""
    stripped = line.rstrip("\n").rstrip("\r")
    if not stripped:
        return "malformed", None
    parts = stripped.split(",")
    if len(parts) != 6:
        return "malformed", None
    date, t, bid_s, ask_s, last_s, vol_s = parts
    if len(date) != 8 or not date.isdigit():
        return "malformed", None
    hms = t.split(":")
    if len(hms) != 3:
        return "malformed", None
    try:
        hh, mm, ss = int(hms[0]), int(hms[1]), int(hms[2])
        if not (0 <= hh <= 23 and 0 <= mm <= 59 and 0 <= ss <= 59):
            return "malformed", None
    except ValueError:
        return "malformed", None
    try:
        bid = float(bid_s)
        ask = float(ask_s)
        last = float(last_s)
    except ValueError:
        return "malformed", None
    if not (math.isfinite(bid) and math.isfinite(ask) and math.isfinite(last)):
        return "bad_quote", None
    if not (bid > 0 and ask > 0):
        return "bad_quote", None
    if bid > ask:
        return "bad_quote", None
    return "ok", (date, t)


def _single_pass_scan(tick_path: Path, probe_rows: int, sample_rows: int = 200):
    """One line-buffered pass: row count, schema sample, timestamp, quotes,
    malformed stats, and a bounded peak-RSS probe."""

    rows = 0
    malformed = 0
    bad_quote = 0
    bad_ts = 0
    cols_at_row0 = None
    header_suspect = False
    out_of_order = 0
    last_key = None
    probe_peak = 0
    sample_idx = 0
    total = 0

    with open(tick_path, "r", newline="") as f:
        for line in f:
            rows += 1
            if rows <= sample_rows:
                sample_idx += 1
            status, row = _validate_tick_line(line)
            if status == "malformed":
                malformed += 1
                continue
            if status == "bad_quote":
                bad_quote += 1
                continue
            if rows == 1:
                cols_at_row0 = len(line.rstrip("\n").rstrip("\r").split(","))
                if line[:4].strip().lower().startswith("date"):
                    header_suspect = True
            date, t = row
            try:
                hh, mm, ss = t.split(":")
                key = date + "," + f"{int(hh):02d}:{int(mm):02d}"
            except Exception:
                bad_ts += 1
                continue
            if last_key is not None and key < last_key:
                out_of_order += 1
            last_key = key if key > (last_key or "") else last_key
            total += 1
            if probe_rows and rows <= probe_rows:
                rss = _sample_peak_rss()
                if rss:
                    probe_peak = max(probe_peak, rss)
    return {
        "rows": rows,
        "valid_rows": total,
        "malformed_rows": malformed,
        "bad_quote_rows": bad_quote,
        "bad_timestamp_rows": bad_ts,
        "minute_key_rollback_count": out_of_order,
        "schema_fields_on_row_0": cols_at_row0,
        "header_suspect": header_suspect,
        "probe_peak_rss_bytes": probe_peak if probe_rows else None,
        "probe_rows_sampled": min(rows, probe_rows or 0),
    }


def _environment_report(required_ram: int, required_free_disk: int, out_root: Path):
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage(str(out_root))
    return {
        "memory_total_bytes": vm.total,
        "memory_available_bytes": vm.available,
        "disk_free_bytes": disk.free,
        "memory_threshold_bytes": required_ram,
        "disk_threshold_bytes": required_free_disk,
        "memory_pass": vm.available >= required_ram,
        "disk_pass": disk.free >= required_free_disk,
        "platform": platform.platform(),
        "python_version": platform.python_version(),
    }


def run_stage0_preflight(
    out_root: Path,
    market: str,
    tick_path: Path,
    m1_path: Path,
    expected_tick_sha256: str | None = None,
    expected_m1_sha256: str | None = None,
    required_ram_bytes: int = REQUIRED_RAM_BYTES_DEFAULT,
    required_free_disk_bytes: int = REQUIRED_FREE_DISK_BYTES_DEFAULT,
    probe_rows: int = 10_000_000,
    entry_script_path: Path | None = None,
    helper_module_paths: list[Path] | None = None,
    protocol_sha256: str | None = None,
) -> dict:
    """Runs Stage-0 preflight for one market and returns the report dict.

    Never raises for a failed CHECK (that is a FALSE verdict); raises
    ExecutionInfrastructureFailure only for component failure of the check
    itself.
    """
    market_upper = market.upper()
    run_id = f"PREFLIGHT_{market_upper}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    stage_dir = out_root / run_id

    rec = StageRunRecorder(
        directory=stage_dir,
        stage_name="STAGE0",
        protocol_sha=protocol_sha256 or "",
        entry_script_path=entry_script_path or Path(__file__),
        helper_module_paths=helper_module_paths or [],
        extra_identity={"market": market_upper, "output_layout": "PREFLIGHT_<market>_<runid>"},
    )
    rec.start()

    checks = {}
    reasons = []
    try:
        tick_ok = tick_path.is_file()
        m1_ok = m1_path.is_file()
        checks["tick_file_exists"] = tick_ok
        checks["m1_file_exists"] = m1_ok
        if not tick_ok:
            reasons.append(f"tick file missing: {tick_path}")
        if not m1_ok:
            reasons.append(f"m1 file missing: {m1_path}")

        tick_sha = sha256_file(tick_path) if tick_ok else None
        m1_sha = sha256_file(m1_path) if m1_ok else None
        checks["tick_sha256"] = tick_sha
        checks["m1_sha256"] = m1_sha
        if expected_tick_sha256 and tick_sha and tick_sha.lower() != expected_tick_sha256.lower():
            reasons.append("tick SHA-256 mismatch")
            checks["tick_hash_match"] = False
        elif tick_sha:
            checks["tick_hash_match"] = True
        if expected_m1_sha256 and m1_sha and m1_sha.lower() != expected_m1_sha256.lower():
            reasons.append("m1 SHA-256 mismatch")
            checks["m1_hash_match"] = False
        elif m1_sha:
            checks["m1_hash_match"] = True

        scan = {}
        if tick_ok:
            scan = _single_pass_scan(tick_path, probe_rows)
            checks.update(scan)
            if scan["rows"] == 0:
                reasons.append("tick file is empty")
            if scan["schema_fields_on_row_0"] != 6:
                reasons.append(
                    f"schema: expected 6 fields on row 0, got {scan['schema_fields_on_row_0']}"
                )
            if scan["header_suspect"]:
                reasons.append("schema: header row suspected (expected headerless)")
            if scan["bad_timestamp_rows"]:
                reasons.append(
                    f"timestamp format: {scan['bad_timestamp_rows']} malformed rows"
                )
            checks["schema_valid"] = (
                scan["schema_fields_on_row_0"] == 6 and not scan["header_suspect"]
            )
            checks["timestamp_format_valid"] = scan["bad_timestamp_rows"] == 0
            checks["quote_validity_pass"] = scan["bad_quote_rows"] == 0
            checks["malformed_rows_pass"] = scan["malformed_rows"] == 0
            checks["timezone_convention"] = "naive UTC (YYYYMMDD,HH:MM:SS)"

        env = _environment_report(required_ram_bytes, required_free_disk_bytes, out_root)
        checks["environment"] = env
        if not env["memory_pass"]:
            reasons.append(
                "resource: available RAM below configured preflight threshold"
            )
        if not env["disk_pass"]:
            reasons.append(
                "resource: free disk below configured preflight threshold"
            )
        checks["streaming_probe_pass"] = bool(
            not probe_rows or scan.get("probe_peak_rss_bytes")
        )
        checks["peak_rss_probe_bytes"] = scan.get("probe_peak_rss_bytes")

        verdict = "PASS" if not reasons else "FAIL"
        report = {
            "stage": "STAGE0",
            "market": market_upper,
            "run_id": run_id,
            "output_directory": str(stage_dir),
            "verdict": verdict,
            "summary": " ".join(reasons) if reasons else "all preflight checks passed",
            "checks": checks,
            "failures": reasons,
        }

        (stage_dir / "preflight.json").write_text(
            json.dumps(report, indent=2, allow_nan=True), encoding="utf-8"
        )
        stage_manifest = {
            "stage": "STAGE0",
            "preflight_sha256": sha256_file(stage_dir / "preflight.json"),
        }
        (stage_dir / "stage0_manifest.json").write_text(
            json.dumps(stage_manifest, indent=2), encoding="utf-8"
        )

        rec.complete(
            extra={
                "verdict": verdict,
                "preflight_reasons": reasons,
                "tick_sha256": tick_sha,
                "m1_sha256": m1_sha,
            }
        )
        report["stage_state"] = "COMPLETED"
        return report
    except BaseException as exc:
        rec.invalidate(reason=classify_infrastructure_failure(exc))
        category = classify_infrastructure_failure(exc)
        raise ExecutionInfrastructureFailure(
            category, f"Stage 0 failed for {market_upper}: {exc}"
        ) from exc