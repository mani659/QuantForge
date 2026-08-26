"""Stage-0 preflight tests (V2.0.1 §3): PASS/FAIL as findings, not crashes."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.staged_execution._failure import ExecutionInfrastructureFailure  # noqa: E402
from research.staged_execution.stage0 import run_stage0_preflight  # noqa: E402


def _write_tick(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _good_lines() -> list[str]:
    return [
        "20240610,07:00:00,100.0,100.1,100.05,1",
        "20240610,07:01:00,100.2,100.3,100.25,1",
        "20240610,07:02:00,100.4,100.5,100.45,1",
    ]


@pytest.fixture
def env(tmp_path):
    out = tmp_path / "out"
    m1 = tmp_path / "M1.csv"
    m1.write_text("timestamp,open,high,low,close,volume\n2024-06-10 07:00:00,1,1,1,1,1\n")
    return {"out": out, "m1": m1}


def test_stage0_pass(env):
    tick = env["out"].parent / "tick.csv"
    _write_tick(tick, _good_lines())
    report = run_stage0_preflight(
        out_root=env["out"], market="XAUUSD",
        tick_path=tick, m1_path=env["m1"],
        required_ram_bytes=0, required_free_disk_bytes=0, probe_rows=0,
        protocol_sha256="dummy",
    )
    assert report["verdict"] == "PASS"
    assert report["stage"] == "STAGE0"
    assert report["stage_state"] == "COMPLETED"
    assert report["checks"]["schema_valid"] is True
    assert report["checks"]["tick_hash_match"] is True
    assert report["checks"]["quote_validity_pass"] is True
    stage_dir = Path(report["output_directory"])
    assert (stage_dir / "preflight.json").is_file()
    assert (stage_dir / "stage0_manifest.json").is_file()
    assert (stage_dir / "execution_journal.json").is_file()
    j = json.loads((stage_dir / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "COMPLETED"


def test_stage0_pass_repeatable_fresh_identity(env):
    tick = env["out"].parent / "tick.csv"
    _write_tick(tick, _good_lines())
    r1 = run_stage0_preflight(out_root=env["out"], market="XAUUSD", tick_path=tick,
                              m1_path=env["m1"], required_ram_bytes=0,
                              required_free_disk_bytes=0, probe_rows=0)
    r2 = run_stage0_preflight(out_root=env["out"], market="XAUUSD", tick_path=tick,
                              m1_path=env["m1"], required_ram_bytes=0,
                              required_free_disk_bytes=0, probe_rows=0)
    assert r1["verdict"] == r2["verdict"] == "PASS"
    assert r1["run_id"] != r2["run_id"]


def test_stage0_missing_files_is_finding_not_crash(env):
    missing = env["out"].parent / "missing.csv"
    report = run_stage0_preflight(out_root=env["out"], market="XAUUSD",
                                  tick_path=missing, m1_path=missing,
                                  required_ram_bytes=0, required_free_disk_bytes=0,
                                  probe_rows=0)
    assert report["verdict"] == "FAIL"
    assert report["stage_state"] == "COMPLETED"
    assert report["checks"]["tick_file_exists"] is False
    assert report["checks"]["m1_file_exists"] is False


def test_stage0_bad_schema_fail(env):
    tick = env["out"].parent / "tick.csv"
    _write_tick(tick, ["20240610,07:00:00,100.0,100.1,100.05"])  # 5 fields
    report = run_stage0_preflight(out_root=env["out"], market="XAUUSD",
                                  tick_path=tick, m1_path=env["m1"],
                                  required_ram_bytes=0, required_free_disk_bytes=0,
                                  probe_rows=0)
    assert report["verdict"] == "FAIL"
    assert report["checks"]["schema_valid"] is False


def test_stage0_bad_quote_fail(env):
    tick = env["out"].parent / "tick.csv"
    _write_tick(tick, ["20240610,07:00:00,100.5,100.1,100.3,1"])  # bid > ask
    report = run_stage0_preflight(out_root=env["out"], market="XAUUSD",
                                  tick_path=tick, m1_path=env["m1"],
                                  required_ram_bytes=0, required_free_disk_bytes=0,
                                  probe_rows=0)
    assert report["verdict"] == "FAIL"
    assert report["checks"]["quote_validity_pass"] is False


def test_stage0_expected_hash_mismatch_fail(env):
    tick = env["out"].parent / "tick.csv"
    _write_tick(tick, _good_lines())
    report = run_stage0_preflight(out_root=env["out"], market="XAUUSD",
                                  tick_path=tick, m1_path=env["m1"],
                                  expected_tick_sha256="0" * 64,
                                  required_ram_bytes=0, required_free_disk_bytes=0,
                                  probe_rows=0)
    assert report["verdict"] == "FAIL"
    assert report["checks"]["tick_hash_match"] is False


def test_stage0_component_failure_is_infra_failure(env, monkeypatch):
    tick = env["out"].parent / "tick.csv"
    _write_tick(tick, _good_lines())

    def boom(*a, **k):
        raise RuntimeError("scan exploded")

    monkeypatch.setattr("research.staged_execution.stage0._single_pass_scan", boom)
    with pytest.raises(ExecutionInfrastructureFailure) as ei:
        run_stage0_preflight(out_root=env["out"], market="XAUUSD",
                             tick_path=tick, m1_path=env["m1"],
                             required_ram_bytes=0, required_free_disk_bytes=0,
                             probe_rows=0)
    assert "EXECUTION-INFRASTRUCTURE FAILURE" in str(ei.value)
    assert "INFRASTRUCTURE_EXCEPTION" in str(ei.value)