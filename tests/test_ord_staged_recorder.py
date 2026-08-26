"""Stage-run recorder + reconciliation integration tests (V2.0.1 §10)."""

import json
import subprocess
import sys
import uuid
from pathlib import Path

import psutil
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.staged_execution._stage_recorder import (  # noqa: E402
    StageRunRecorder,
    _INFRA_ARTIFACTS,
)

RECONCILE = ROOT / "scripts/reconcile_execution.py"


def _run_reconciler(directory: Path) -> str:
    return subprocess.run(
        ["python", str(RECONCILE), str(directory)],
        capture_output=True, text=True,
    ).stdout.strip()


@pytest.fixture
def rec(tmp_path):
    d = tmp_path / f"PREFLIGHT_XAUUSD_{uuid.uuid4().hex[:8]}"
    r = StageRunRecorder(
        directory=d, stage_name="STAGE0", protocol_sha="dummy",
        entry_script_path=Path(__file__),
    )
    return r


def test_recorder_writes_five_infra_artifacts(rec):
    rec.start()
    rec.complete()
    for art in _INFRA_ARTIFACTS:
        assert (rec.directory / art).is_file(), art
    j = json.loads((rec.directory / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "COMPLETED"
    m = json.loads((rec.directory / "execution_manifest.json").read_text(encoding="utf-8"))
    assert m["final_state"] == "COMPLETED"
    assert m["scientific_validity"] is False
    assert m["economic_evidence"] is False


def test_recorder_execution_id_equals_dir_name(rec):
    assert rec.execution_id == rec.directory.name


def test_recorder_rejects_existing_dir(rec):
    rec.start()
    with pytest.raises(FileExistsError):
        StageRunRecorder(
            directory=rec.directory, stage_name="STAGE0", protocol_sha="x",
            entry_script_path=Path(__file__),
        ).start()


def test_recorder_mutation_guard_invalidates(rec, tmp_path):
    entry = tmp_path / "entry.py"
    entry.write_text("original\n", encoding="utf-8")
    r = StageRunRecorder(
        directory=tmp_path / "run", stage_name="STAGE0", protocol_sha="x",
        entry_script_path=entry,
    )
    r.start()
    entry.write_text("mutated\n", encoding="utf-8")
    with pytest.raises(RuntimeError):
        r.complete()
    j = json.loads((r.directory / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "INVALIDATED"


def test_reconcile_reconciled_crashed_stage_dir(rec):
    rec.start()  # RUNNING in this live process
    assert rec.state == "RUNNING"
    # Simulate a dead process identity (impossible PID).
    proc = psutil.Process()
    proc_id = {
        "execution_id": rec.directory.name,
        "pid": 999999,
        "process_start_time": proc.create_time(),
        "boot_time": psutil.boot_time(),
    }
    (rec.directory / "process_identity.json").write_text(
        json.dumps(proc_id), encoding="utf-8"
    )
    out = _run_reconciler(rec.directory)
    assert "STALE:" in out
    assert "SUCCESS:" in out
    j = json.loads((rec.directory / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "CRASHED"
    m = json.loads((rec.directory / "execution_manifest.json").read_text(encoding="utf-8"))
    assert m["scientific_validity"] is False
    assert m["scientific_adjudication"] == "NOT_ADJUDICABLE"


def test_reconcile_default_terminal_states(rec):
    rec.start()
    rec.complete()
    out = _run_reconciler(rec.directory)
    assert "TERMINAL:" in out
    j = json.loads((rec.directory / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "COMPLETED"


def test_invalidate_leaves_terminal(rec):
    rec.start()
    rec.interrupt("test interrupt")
    with pytest.raises(RuntimeError):
        rec.complete()
    j = json.loads((rec.directory / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "INTERRUPTED"