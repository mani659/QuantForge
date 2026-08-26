"""Stage-1 frozen preparation tests (V2.0.1 §4, W1/W2/W4)."""

import gzip
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.staged_execution._failure import ExecutionInfrastructureFailure  # noqa: E402
from research.staged_execution.stage1 import is_valid_prep, run_stage1_prepare  # noqa: E402
from synth_ord_fixtures import build_fixture  # noqa: E402

ECON_SHA = "8f45d7f82c80b7131c958c158f448520fef6927d49f9eb844fbbd55e35395663"
SCI_SHA = "85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06"
MARKETS = ["XAUUSD"]


@pytest.fixture
def fixture(tmp_path):
    data = build_fixture(tmp_path)
    out_root = tmp_path / "prep"
    return {**data, "out_root": out_root, "repo_root": ROOT}


def _prepare(fx, force_rebuild=False):
    return run_stage1_prepare(
        out_root=fx["out_root"], repo_root=fx["repo_root"], market=fx["market"],
        m1_path=fx["m1"], tick_path=fx["tick"], event_table_path=fx["events"],
        economic_protocol_sha256=ECON_SHA, scientific_protocol_sha256=SCI_SHA,
        force_rebuild=force_rebuild,
    )


def test_stage1_builds_immutable_prep(fixture):
    res = _prepare(fixture)
    assert res["mode"] == "built"
    assert res["preparation_identity"].startswith("PREP_XAUUSD_")
    assert len(res["preparation_hash"]) == 64
    prep = Path(res["prep_dir"])
    assert prep.exists()
    assert prep.name == res["preparation_identity"]
    for art in ("prep_manifest.json", "minute_quotes.csv.gz", "event_inputs.csv",
                "event_paths.csv", "minute_index.bin", "execution_journal.json"):
        assert (prep / art).is_file(), art
    j = json.loads((prep / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "COMPLETED"


def test_stage1_manifest_facts(fixture):
    res = _prepare(fixture)
    prep = Path(res["prep_dir"])
    m = json.loads((prep / "prep_manifest.json").read_text(encoding="utf-8"))
    assert m["market_median_bid"] == fixture["market_median_bid"]
    assert m["market_median_ask"] == fixture["market_median_ask"]
    assert m["observed_minutes"] == fixture["n_minutes"]
    assert m["n_events"] == fixture["n_events"]
    assert m["n_excluded_events"] == fixture["n_excluded"]
    assert m["n_stop_fills"] == 1
    # Stage 1 must never persist a single economic result.
    for banned in ("net_bp", "gross_bp", "profit_factor", "cumulative_net_bp"):
        assert banned not in json.dumps(m)


def test_stage1_event_inputs_shape(fixture):
    res = _prepare(fixture)
    prep = Path(res["prep_dir"])
    import pandas as pd
    df = pd.read_csv(prep / "event_inputs.csv")
    assert len(df) == fixture["n_events"]
    reasons = df["exit_reason"].value_counts().to_dict()
    assert reasons.get("HORIZON") == 1
    assert reasons.get("STRUCTURAL_INVALIDATION") == 1
    assert reasons.get("EXCLUDED_RANGE_MISMATCH") == 1
    assert reasons.get("EXCLUDED_RANGE_RECONSTRUCTION") == 1
    assert reasons.get("EXCLUDED_HORIZON_INCOMPLETE") == 1


def test_stage1_horizon_trade_fields(fixture):
    res = _prepare(fixture)
    import pandas as pd
    df = pd.read_csv(Path(res["prep_dir"]) / "event_inputs.csv")
    horizon = df[df["exit_reason"] == "HORIZON"].iloc[0]
    assert horizon["quote_lookup_entry"] == "exact"
    assert horizon["quote_lookup_exit"] == "exact"
    assert horizon["entry_minute"] == "2024-06-10T07:31:00"
    assert float(horizon["entry_bid"]) == 120.0
    assert float(horizon["entry_ask"]) == 120.1
    assert horizon["exit_minute"] == 12855451  # epoch minute of 09:31
    assert float(horizon["exit_bid"]) == 120.0


def test_stage1_stop_trade_fields(fixture):
    res = _prepare(fixture)
    import pandas as pd
    df = pd.read_csv(Path(res["prep_dir"]) / "event_inputs.csv")
    stop = df[df["exit_reason"] == "STRUCTURAL_INVALIDATION"].iloc[0]
    assert stop["structural_invalidation_level"] == 202.0
    assert float(stop["stop_fill_bid"]) == 200.5
    assert float(stop["stop_fill_ask"]) == 200.6
    assert stop["stop_fill_ts"] == "2024-06-11T07:32:00"
    assert stop["quote_lookup_exit"] == "exact"


def test_stage1_reuse_when_complete_and_matching(fixture):
    r1 = _prepare(fixture)
    r2 = _prepare(fixture)
    assert r2["mode"] == "reused"
    assert r2["preparation_identity"] == r1["preparation_identity"]
    assert Path(r2["prep_dir"]) == Path(r1["prep_dir"])


def test_stage1_modification_invalidates_and_blocks_until_force(fixture):
    r1 = _prepare(fixture)
    prep = Path(r1["prep_dir"])
    (prep / "event_paths.csv").write_text("corrupted\n", encoding="utf-8")
    # Re-run WITHOUT force_rebuild -> fail-closed infrastructure failure.
    with pytest.raises(ExecutionInfrastructureFailure) as ei:
        _prepare(fixture)
    assert "PREPARATION_INTEGRITY_FAILURE" in str(ei.value)


def test_stage1_force_rebuild_archives_not_overwrites(fixture):
    r1 = _prepare(fixture)
    prep = Path(r1["prep_dir"])
    (prep / "event_paths.csv").write_text("corrupted\n", encoding="utf-8")
    r2 = _prepare(fixture, force_rebuild=True)
    assert r2["mode"] == "built"
    assert r2["preparation_identity"] == r1["preparation_identity"]
    assert Path(r2["prep_dir"]).exists()
    # Archived prior dir preserved, journal forced to CRASHED.
    out_parent = fixture["out_root"]
    archived = [p for p in out_parent.iterdir() if "_RECONCILED_" in p.name]
    assert len(archived) == 1
    note = json.loads((archived[0] / "archival_note.json").read_text(encoding="utf-8"))
    assert note["archived_from"] == str(prep)
    j = json.loads((archived[0] / "execution_journal.json").read_text(encoding="utf-8"))
    assert j["state"] == "CRASHED"


def test_stage1_bounded_memory_evidence(fixture):
    res = _prepare(fixture)
    m = json.loads((Path(res["prep_dir"]) / "prep_manifest.json").read_text(encoding="utf-8"))
    # Fixture has exactly one tick per minute, so residency can not exceed 1.
    assert m["max_minute_ticks_resident"] <= 1
    assert m["minutes_flushed"] == fixture["n_minutes"]
    assert m["tick_rows_streamed"] == 123


def test_stage1_minute_quotes_stream_contents(fixture):
    res = _prepare(fixture)
    prep = Path(res["prep_dir"])
    with gzip.open(prep / "minute_quotes.csv.gz", "rt", encoding="utf-8") as g:
        header = g.readline().strip()
        rows = [line for line in g if line.strip()]
    assert header == "epoch_min,minute_utc,bid_median,ask_median,nticks"
    assert len(rows) == fixture["n_minutes"]
    assert rows[0].startswith("12855331,")  # 2024-06-10 07:31


def test_stage1_prep_deterministic_identity(fixture):
    r1 = _prepare(fixture)
    r2 = _prepare(fixture, force_rebuild=True)
    assert r1["preparation_hash"] == r2["preparation_hash"]


def test_stage1_never_has_extra_fields(fixture):
    from research.staged_execution.stage1 import EVENT_INPUT_COLUMNS
    res = _prepare(fixture)
    import pandas as pd
    df = pd.read_csv(Path(res["prep_dir"]) / "event_inputs.csv")
    assert list(df.columns) == EVENT_INPUT_COLUMNS


def test_stage1_infra_failure_on_missing_source(fixture):
    with pytest.raises(ExecutionInfrastructureFailure):
        run_stage1_prepare(
            out_root=fixture["out_root"], repo_root=fixture["repo_root"],
            market=fixture["market"],
            m1_path=fixture["m1"], tick_path=fixture["out_root"].parent / "nope.csv",
            event_table_path=fixture["events"],
            economic_protocol_sha256=ECON_SHA, scientific_protocol_sha256=SCI_SHA,
        )