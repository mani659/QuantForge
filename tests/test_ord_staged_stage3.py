"""Stage-3 read-only verification tests (V2.0.1 §7)."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.staged_execution._failure import ExecutionInfrastructureFailure  # noqa: E402
from research.staged_execution.stage1 import run_stage1_prepare  # noqa: E402
from research.staged_execution.stage2 import run_stage2_execute  # noqa: E402
from research.staged_execution.stage3 import run_stage3_verify  # noqa: E402
from synth_ord_fixtures import build_fixture  # noqa: E402

ECON_SHA = "8f45d7f82c80b7131c958c158f448520fef6927d49f9eb844fbbd55e35395663"
SCI_SHA = "85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06"
V2_PATH = ROOT / "output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_1_AMENDED.md"
V2_SHA = "1D3EE7A6A9FD747CB57A716B43C5EB80BB7D6016011D2C4DF9F0814CC196968D"
DEFLOCK = ROOT / "output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md"


@pytest.fixture
def chain(tmp_path):
    data = build_fixture(tmp_path)
    prep_root = tmp_path / "prep"
    run_stage1_prepare(
        out_root=prep_root, repo_root=ROOT, market=data["market"],
        m1_path=data["m1"], tick_path=data["tick"],
        event_table_path=data["events"],
        economic_protocol_sha256=ECON_SHA, scientific_protocol_sha256=SCI_SHA,
    )
    ex = run_stage2_execute(
        out_root=tmp_path / "results", repo_root=ROOT, prep_root=prep_root,
        markets=[data["market"]], m1_dir=tmp_path, tick_dir=tmp_path,
        scientific_protocol_sha256=SCI_SHA, economic_protocol_sha256=ECON_SHA,
        v2_0_1_protocol_path=V2_PATH, v2_0_1_protocol_sha256=V2_SHA,
        definition_lock_path=DEFLOCK,
        entry_script_path=ROOT / "scripts/ord_econ_stage2_execute.py",
    )
    return {
        "market": data["market"],
        "execution_dir": Path(ex["execution_dir"]),
        "prep_root": prep_root,
        "m1_dir": tmp_path,
        "tick_dir": tmp_path,
    }


def _verify(chain, force_rerun=False):
    return run_stage3_verify(
        execution_dir=chain["execution_dir"], prep_root=chain["prep_root"],
        markets=[chain["market"]], m1_dir=chain["m1_dir"],
        tick_dir=chain["tick_dir"], repo_root=ROOT,
        economic_protocol_sha256=ECON_SHA, scientific_protocol_sha256=SCI_SHA,
        v2_0_1_protocol_path=V2_PATH, v2_0_1_protocol_sha256=V2_SHA,
        definition_lock_path=DEFLOCK,
        entry_script_path=ROOT / "scripts/ord_econ_stage3_verify.py",
        force_rerun=force_rerun,
    )


def test_stage3_passes_on_pristine_chain(chain):
    report = _verify(chain)
    assert report["verdict"] == "PASS"
    assert report["checks_total"] == report["checks_passed"]
    vdir = chain["execution_dir"].parent / f"VERIFICATION_{chain['execution_dir'].name}"
    assert (vdir / "verification_report.json").is_file()
    assert (vdir / "verification_summary.md").is_file()
    j = json.loads((vdir / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "COMPLETED"
    # Stage 3 is read-only with respect to economic artifacts.
    from research.staged_execution._identity import sha256_file
    ledger_hash_before = sha256_file(chain["execution_dir"] / "trade_ledger.csv")
    _verify(chain, force_rerun=True)
    assert sha256_file(chain["execution_dir"] / "trade_ledger.csv") == ledger_hash_before


def test_stage3_not_restartable_without_force(chain):
    _verify(chain)
    with pytest.raises(ExecutionInfrastructureFailure):
        _verify(chain)


def test_stage3_fails_on_tampered_ledger(chain):
    import pandas as pd
    led = chain["execution_dir"] / f"trade_ledger_{chain['market']}.csv"
    df = pd.read_csv(led)
    # Corrupt every persisted net_bp so reproduction-from-frozen-inputs
    # (and cumulative/yearly/gates) diverges from the recorded values.
    df.loc[df["exit_reason"] == "HORIZON", "net_bp"] = -999.0
    df.to_csv(led, index=False)
    report = _verify(chain)
    assert report["verdict"] == "FAIL"
    names = {c["check"] for c in report["checks"]}
    assert any("net_reproduced" in n for n in names)


def test_stage3_fails_on_missing_artifact(chain):
    (chain["execution_dir"] / "yearly_summary.csv").unlink()
    report = _verify(chain)
    assert report["verdict"] == "FAIL"
    names = {c["check"] for c in report["checks"]}
    assert "required_artifacts_complete" in names


def test_stage3_fails_on_missing_market_ledger(chain):
    (chain["execution_dir"] / f"trade_ledger_{chain['market']}.csv").unlink()
    report = _verify(chain)
    assert report["verdict"] == "FAIL"
    names = {c["check"] for c in report["checks"]}
    assert any(n.endswith("market_ledger_present") for n in names)


def test_stage3_fails_on_non_completed_journal(chain):
    jpath = chain["execution_dir"] / "execution_journal.json"
    j = json.loads(jpath.read_text(encoding="utf-8"))
    j["state"] = "INVALIDATED"
    jpath.write_text(json.dumps(j), encoding="utf-8")
    report = _verify(chain)
    assert report["verdict"] == "FAIL"
    names = {c["check"] for c in report["checks"]}
    assert "stage2_journal_completed" in names