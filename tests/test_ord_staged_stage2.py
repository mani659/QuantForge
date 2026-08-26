"""Stage-2 controlled-execution tests (V2.0.1 §6): exactly-once, fail-closed,
helpers imported (never re-implemented), ledger integrity."""

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
from synth_ord_fixtures import build_fixture  # noqa: E402

ECON_SHA = "8f45d7f82c80b7131c958c158f448520fef6927d49f9eb844fbbd55e35395663"
SCI_SHA = "85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06"
V2_PATH = ROOT / "output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_1_AMENDED.md"
V2_SHA = "1D3EE7A6A9FD747CB57A716B43C5EB80BB7D6016011D2C4DF9F0814CC196968D"
DEFLOCK = ROOT / "output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md"
MISSING_I = "no such v2 file"


@pytest.fixture
def setup(tmp_path):
    data = build_fixture(tmp_path)
    prep_root = tmp_path / "prep"
    run_stage1_prepare(
        out_root=prep_root, repo_root=ROOT, market=data["market"],
        m1_path=data["m1"], tick_path=data["tick"],
        event_table_path=data["events"],
        economic_protocol_sha256=ECON_SHA, scientific_protocol_sha256=SCI_SHA,
    )
    return {
        "market": data["market"],
        "m1_dir": tmp_path,
        "tick_dir": tmp_path,
        "prep_root": prep_root,
        "out_root": tmp_path / "results",
    }


def _execute(s, markets=None):
    return run_stage2_execute(
        out_root=s["out_root"], repo_root=ROOT, prep_root=s["prep_root"],
        markets=markets or [s["market"]],
        m1_dir=s["m1_dir"], tick_dir=s["tick_dir"],
        scientific_protocol_sha256=SCI_SHA, economic_protocol_sha256=ECON_SHA,
        v2_0_1_protocol_path=V2_PATH, v2_0_1_protocol_sha256=V2_SHA,
        definition_lock_path=DEFLOCK,
        entry_script_path=ROOT / "scripts/ord_econ_stage2_execute.py",
    )


def test_stage2_exactly_once_fresh_identity(setup):
    r1 = _execute(setup)
    global_dir = Path(r1["execution_dir"])
    assert global_dir.is_dir()
    assert global_dir.name.startswith("EXECUTION_")
    j = json.loads((global_dir / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "COMPLETED"

    r2 = _execute(setup)
    assert r2["execution_id"] != r1["execution_id"]
    assert Path(r2["execution_dir"]) != global_dir
    j2 = json.loads((Path(r2["execution_dir"]) / "execution_journal.json").read_text(encoding="utf-8"))
    assert j2["state"] == "COMPLETED"
    # First never resumed / overwritten.
    assert (global_dir / "execution_journal.json").is_file()


def test_stage2_required_artifacts(setup):
    r = _execute(setup)
    d = Path(r["execution_dir"])
    base = ["trade_ledger.csv", "statistics.json", "market_summary.csv",
            "yearly_summary.csv", "development_oos_summary.csv",
            "cost_model_outputs.json", "execution_metadata.json",
            "peak_resource.json", "ECONOMIC_TRANSLATION_REPORT_V1.md"]
    for art in base + [f"trade_ledger_{setup['market']}.csv"]:
        assert (d / art).is_file(), art
    assert (d / "execution_manifest.json").is_file()
    em = json.loads((d / "execution_manifest.json").read_text(encoding="utf-8"))
    assert em["final_state"] == "COMPLETED"
    assert em["missing_artifacts"] == []


def test_stage2_ledger_content(setup):
    r = _execute(setup)
    d = Path(r["execution_dir"])
    import pandas as pd
    led = pd.read_csv(d / "trade_ledger.csv")
    assert len(led) == 5  # 2 traded + 3 excluded
    traded = led[led["exit_reason"].isin(
        ["HORIZON", "STRUCTURAL_INVALIDATION"])]
    assert len(traded) == 2
    horizon = traded[traded["exit_reason"] == "HORIZON"].iloc[0]
    assert horizon["net_bp"] == pytest.approx((120.0 - 120.1) / 120.1 * 1.0e4)
    assert horizon["holding_duration_min"] == pytest.approx(120.0)
    stop = traded[traded["exit_reason"] == "STRUCTURAL_INVALIDATION"].iloc[0]
    assert stop["net_bp"] == pytest.approx((200.5 - 203.1) / 203.1 * 1.0e4)
    assert stop["holding_duration_min"] == pytest.approx(1.0)
    excluded = led[led["exit_reason"].str.startswith("EXCLUDED_")]
    assert len(excluded) == 3


def test_stage2_prep_mutation_fails_closed_before_economics(setup):
    _execute(setup)
    prep_dir = next(setup["prep_root"].iterdir())
    (prep_dir / "event_paths.csv").write_text("corrupted\n", encoding="utf-8")
    before = {
        p.name for p in setup["out_root"].glob("ORD_ECONOMIC/V1.1.0/EXECUTION_*")
    } if any(setup["out_root"].glob("ORD_ECONOMIC/V1.1.0/EXECUTION_*")) else set()
    with pytest.raises(ExecutionInfrastructureFailure) as ei:
        _execute(setup)
    assert "EXECUTION-INFRASTRUCTURE FAILURE" in str(ei.value)
    after = {
        p.name for p in setup["out_root"].glob("ORD_ECONOMIC/V1.1.0/EXECUTION_*")
    } if any(setup["out_root"].glob("ORD_ECONOMIC/V1.1.0/EXECUTION_*")) else set()
    assert after == before  # no new economic execution directory materialized


def test_stage2_missing_source_fails_closed(setup):
    wrong_tick = setup["tick_dir"] / "XAGUSD_mt5_ticks.csv"
    assert not wrong_tick.exists()
    with pytest.raises(ExecutionInfrastructureFailure) as ei:
        run_stage2_execute(
            out_root=setup["out_root"], repo_root=ROOT, prep_root=setup["prep_root"],
            markets=["XAGUSD"], m1_dir=setup["m1_dir"], tick_dir=setup["tick_dir"],
            scientific_protocol_sha256=SCI_SHA, economic_protocol_sha256=ECON_SHA,
            v2_0_1_protocol_path=V2_PATH, v2_0_1_protocol_sha256=V2_SHA,
            definition_lock_path=DEFLOCK,
            entry_script_path=ROOT / "scripts/ord_econ_stage2_execute.py",
        )
    assert "EXECUTION-INFRASTRUCTURE FAILURE" in str(ei.value)


def test_stage2_helpers_are_imported_not_reimplemented():
    import research.staged_execution.stage2 as s2
    import scripts.run_ord_econ_v1 as v1
    for name in ("COMMISSION_BANDS", "SLIPPAGE_BANDS", "LEDGER_COLUMNS",
                 "PeakSampler", "classify", "market_metrics", "profit_factor",
                 "split_dev_oos", "year_concentration"):
        assert hasattr(v1, name)
    h = s2._import_v11_helpers()
    assert h["commission_bands"] == v1.COMMISSION_BANDS
    assert h["market_metrics"] is v1.market_metrics
    assert h["classify"] is v1.classify


def test_stage2_statistics_excluded_counts(setup):
    r = _execute(setup)
    d = Path(r["execution_dir"])
    s = json.loads((d / "statistics.json").read_text(encoding="utf-8"))
    m = s["markets"][setup["market"]]
    exc = m["excluded"]
    assert exc.get("EXCLUDED_RANGE_MISMATCH") == 1
    assert exc.get("EXCLUDED_RANGE_RECONSTRUCTION") == 1
    assert exc.get("EXCLUDED_HORIZON_INCOMPLETE") == 1
    assert exc.get("HORIZON") == 1
    assert exc.get("STRUCTURAL_INVALIDATION") == 1
    assert m["trade_count"] == 2


def test_stage2_development_oos_split(setup):
    r = _execute(setup)
    d = Path(r["execution_dir"])
    import pandas as pd
    doo = pd.read_csv(d / "development_oos_summary.csv")
    row = doo.iloc[0]
    assert row["n_event_days"] == 4
    assert row["dev_day_count"] == 2
    assert row["dev_trades"] == 2
    assert row["oos_trades"] == 0