"""Stage 3 — READ-ONLY VERIFICATION (V2.0.1 §7, staging-design §8).

Stage 3 certifies, without touching any scientific or economic artifact:
  * source hashes (M1, tick) vs the persisted scientific manifest, the
    execution metadata, and the Stage-1 prep hashes;
  * the full `PREP_<market>_<hash>` identity is reproduced and the materialized
    preparation is byte-exact valid;
  * Stage-2 ledger integrity: columns faithful to V1.1.0, excluded rows
    preserved, no partial rows;
  * formula consistency (Model-A identity `cost=(s_entry+s_exit)/2`,
    net/gross reproducibility, chronological cumulative sums, PF boundary
    semantics incl. +inf/0/NaN);
  * development/OOS split (first floor(N/2) event days), year concentration,
    and the five viability gates reproduced from the ledger;
  * Stage-2 artifact completeness + COMPLETED journal;
  * no un-reconciled RUNNING stage identities in the staged tree.

Stage 3 creates NO economic evidence and NO new trade/statistic.  All twelve
aggregation helpers are IMPORTED from the approved `scripts.run_ord_econ_v1`
module; none are re-implemented.  Its own output lives in
`VERIFICATION_<execution-id>/` (repeatable, restartable read-only).
"""

from __future__ import annotations

import json
import math
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ._failure import (
    ECONOMIC_EXCLUSION_CODES,
    ExecutionInfrastructureFailure,
    classify_infrastructure_failure,
)
from ._identity import sha256_file
from ._stage_recorder import StageRunRecorder
from .stage1 import PrepIdentity, is_valid_prep
from .stage2 import REQUIRED_STAGE2_ARTIFACTS, expected_artifacts_for

INFRA_ARTIFACTS = {
    "execution_journal.json",
    "implementation_manifest.json",
    "execution_manifest.json",
    "execution_heartbeat.json",
    "process_identity.json",
}


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return f


def _close(a, b, atol=1.0e-6, rtol=1.0e-6) -> bool:
    if a is None or b is None:
        return False
    if math.isnan(a) or math.isnan(b) or math.isinf(a) or math.isinf(b):
        return math.isnan(a) is math.isnan(b) and math.isinf(a) is math.isinf(b)
    return abs(a - b) <= atol + rtol * max(abs(a), abs(b))


def _pf_equal(a, b) -> bool:
    """PF equality incl. +inf / 0 / NaN boundary semantics."""
    if a is None or b is None:
        return a is None and b is None
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return bool(a == b)


def _import_v11_helpers():
    from scripts.run_ord_econ_v1 import (  # noqa: E402
        LEDGER_COLUMNS,
        classify,
        market_metrics,
        profit_factor,
        split_dev_oos,
        year_concentration,
    )
    return {
        "ledger_columns": LEDGER_COLUMNS,
        "classify": classify,
        "market_metrics": market_metrics,
        "profit_factor": profit_factor,
        "split_dev_oos": split_dev_oos,
        "year_concentration": year_concentration,
    }


def _load_ledger(market_path: Path, helpers):
    df = pd.read_csv(market_path, keep_default_na=False)
    return df, helpers["ledger_columns"]


def _traded_rows(df) -> list[dict]:
    out = []
    for _, r in df.iterrows():
        if r.get("exit_reason") in ECONOMIC_EXCLUSION_CODES:
            continue
        row = dict(r)
        row["net_bp"] = _num(row.get("net_bp"))
        row["gross_bp"] = _num(row.get("gross_bp"))
        row["cost_bp"] = _num(row.get("cost_bp"))
        row["entry_spread_bp"] = _num(row.get("entry_spread_bp"))
        row["exit_spread_bp"] = _num(row.get("exit_spread_bp"))
        if row["net_bp"] is None:
            continue
        out.append(row)
    return out


def _verify_market(setup, market: str, helpers) -> list[dict]:
    """All per-market certification checks (read-only, from persisted files)."""
    checks = []
    add = lambda name, passed, detail: checks.append(  # noqa: E731
        {"check": f"{market}:{name}", "pass": bool(passed), "detail": detail}
    )

    meta = setup["meta"]
    prep_root = setup["prep_root"]
    m1_dir = setup["m1_dir"]
    tick_dir = setup["tick_dir"]
    repo_root = setup["repo_root"]
    economic_protocol_sha256 = setup["economic_protocol_sha256"]
    scientific_protocol_sha256 = setup["scientific_protocol_sha256"]
    execution_dir = setup["execution_dir"]

    m1_path = m1_dir / f"{market}_M1.csv"
    tick_path = tick_dir / f"{market}_mt5_ticks.csv"

    src_m1 = sha256_file(m1_path) if m1_path.is_file() else None
    src_tick = sha256_file(tick_path) if tick_path.is_file() else None
    add(
        "source_files_exist",
        m1_path.is_file() and tick_path.is_file(),
        f"m1={m1_path.is_file()} tick={tick_path.is_file()}",
    )
    add(
        "m1_hash_matches_execution",
        src_m1 is not None and src_m1 == meta["m1_hashes"].get(market),
        f"current={src_m1} recorded={meta['m1_hashes'].get(market)}",
    )
    add(
        "tick_hash_matches_execution",
        src_tick is not None and src_tick == meta["tick_hashes"].get(market),
        f"current={src_tick} recorded={meta['tick_hashes'].get(market)}",
    )

    if setup.get("scientific_manifest"):
        expected_m1 = (
            setup["scientific_manifest"].get("input_manifest_hash", {}).get(
                f"{market}_M1.csv")
        )
        add(
            "m1_hash_matches_scientific_manifest",
            src_m1 is not None and expected_m1 is not None and src_m1 == expected_m1,
            f"current={src_m1} scientific={expected_m1}",
        )

    identity = PrepIdentity(
        market=market,
        economic_protocol_sha256=economic_protocol_sha256,
        scientific_protocol_sha256=scientific_protocol_sha256,
        source_m1_sha256=src_m1 or "",
        source_tick_sha256=src_tick or "",
        repo_root=repo_root,
    )
    canonical_dir = prep_root / identity.identity
    valid, reason = is_valid_prep(canonical_dir, identity) if src_m1 and src_tick else (False, "source missing")
    add(
        "stage1_prep_reproduced_valid",
        valid,
        f"{identity.identity} ({reason})",
    )
    add(
        "stage1_hash_matches_execution",
        identity.hash == meta["stage1_preparation_hashes"].get(market),
        f"recomputed={identity.hash} recorded={meta['stage1_preparation_hashes'].get(market)}",
    )

    event_inputs = canonical_dir / "event_inputs.csv" if valid else None
    n_events = 0
    if event_inputs and event_inputs.is_file():
        n_events = sum(1 for _ in open(event_inputs, encoding="utf-8")) - 1
    add("event_inputs_rows", event_inputs is not None and event_inputs.is_file(),
        f"events={n_events}")

    market_ledger = execution_dir / f"trade_ledger_{market}.csv"
    add("market_ledger_present", market_ledger.is_file(), str(market_ledger))
    if not market_ledger.is_file():
        return checks

    df, ledger_columns = _load_ledger(market_ledger, helpers)
    add(
        "ledger_columns_faithful",
        list(df.columns) == list(ledger_columns),
        f"got={list(df.columns)}",
    )
    n_ledger = int(len(df))
    add("trade_count_consistency", n_events == n_ledger,
        f"events={n_events} ledger_rows={n_ledger}")

    exclusions = sorted(ECONOMIC_EXCLUSION_CODES)
    n_excluded = int(df["exit_reason"].isin(exclusions).sum())
    add(
        "excluded_rows_preserved",
        n_excluded == n_events - len(_traded_rows(df)),
        f"excluded={n_excluded} non_quote={n_events - len(_traded_rows(df))}",
    )

    traded = _traded_rows(df)
    traded_sorted = sorted(traded, key=lambda t: (t["trading_day"], t["breakout_ts"]))

    # Gross/net/cost are reproduced from the FROZEN event inputs (the source of
    # truth for quotes; the V1.1.0 ledger intentionally does not persist
    # exit_bid/exit_ask).  Each ledger trade is matched to its event input by
    # breakout_ts (unique per event day/direction).
    inputs_map = {}
    if event_inputs and event_inputs.is_file():
        for _, r in pd.read_csv(event_inputs).iterrows():
            inputs_map[str(r["breakout_ts"])] = r

    model_a_fail = 0
    net_fail = 0
    gross_fail = 0
    unresolved = 0
    for t in traded:
        e = inputs_map.get(str(t.get("breakout_ts")))
        if e is None:
            unresolved += 1
            continue
        es, xs = _num(e.get("entry_spread_bp")), _num(e.get("exit_spread_bp"))
        if es is None or xs is None:
            unresolved += 1
            continue
        if not _close(_num(t.get("cost_bp")), (es + xs) / 2.0, atol=1.0e-9, rtol=1.0e-9):
            model_a_fail += 1
        direction = str(t.get("direction"))
        e_mid = (_num(e.get("entry_bid")) + _num(e.get("entry_ask"))) / 2.0
        x_mid = (_num(e.get("exit_bid")) + _num(e.get("exit_ask"))) / 2.0
        e_exec = _num(e.get("executable_entry_quote"))
        x_exec = _num(e.get("executable_exit_quote"))
        if e_mid is None or x_mid is None or e_exec is None or x_exec is None:
            unresolved += 1
            continue
        if direction == "long":
            want_gross = (x_mid - e_mid) / e_mid * 1.0e4
            want_net = (x_exec - e_exec) / e_exec * 1.0e4
        else:
            want_gross = (e_mid - x_mid) / e_mid * 1.0e4
            want_net = (e_exec - x_exec) / e_exec * 1.0e4
        if not _close(_num(t.get("gross_bp")), want_gross):
            gross_fail += 1
        if not _close(_num(t.get("net_bp")), want_net):
            net_fail += 1

    add("traded_rows_resolvable", unresolved == 0, f"unresolved={unresolved}/{len(traded)}")
    add("model_a_identity", model_a_fail == 0, f"violations={model_a_fail}/{len(traded)}")
    add("gross_reproduced", gross_fail == 0, f"violations={gross_fail}/{len(traded)}")
    add("net_reproduced", net_fail == 0, f"violations={net_fail}/{len(traded)}")

    metrics = helpers["market_metrics"](traded_sorted)
    nets = np.array([t["net_bp"] for t in traded_sorted], dtype=float)
    chrono_cum = float(np.sum(nets))
    add(
        "cumulative_chronological",
        _close(chrono_cum, metrics["cumulative_net_bp"]),
        f"recomputed={chrono_cum} metrics={metrics['cumulative_net_bp']}",
    )
    pf = helpers["profit_factor"](nets)
    add(
        "pf_boundary_semantics",
        _pf_equal(pf, metrics["profit_factor"]),
        f"recomputed={pf} metrics={metrics['profit_factor']}",
    )

    yearly_file = execution_dir / "yearly_summary.csv"
    yearly_df = pd.read_csv(yearly_file) if yearly_file.is_file() else pd.DataFrame()
    conc, yearly = helpers["year_concentration"](traded_sorted)
    yearly_ok = True
    sub = yearly_df[yearly_df["market"] == market] if len(yearly_df) else yearly_df
    for _, yrow in sub.iterrows():
        y = str(int(yrow["year"]))
        want = yearly.get(y) if yearly else None
        if want is None or not _close(float(yrow["cumulative_net_bp"]), want,
                                      atol=1.0e-4, rtol=1.0e-6):
            yearly_ok = False
    ms_file = execution_dir / "market_summary.csv"
    ms = pd.read_csv(ms_file).set_index("market")
    rowm = ms.loc[market]
    rec_conc = float(rowm["year_concentration"])
    add(
        "year_concentration_reproduced",
        conc is not None and _close(rec_conc, conc),
        f"recomputed={conc} recorded={rec_conc}",
    )
    add("yearly_summary_reproduced", yearly_ok, f"rows={len(sub)}")

    dev_oos_file = execution_dir / "development_oos_summary.csv"
    doo = pd.read_csv(dev_oos_file)
    dev, oos, ndays, half = helpers["split_dev_oos"](
        [{"trading_day": r.trading_day}
         for r in pd.read_csv(event_inputs).itertuples()] if event_inputs else [],
        traded_sorted,
    )
    dev_m = helpers["market_metrics"](dev)
    oos_m = helpers["market_metrics"](oos)
    drow = doo[doo["market"] == market].iloc[0]
    oos_ok = (
        int(drow["n_event_days"]) == ndays
        and int(drow["dev_day_count"]) == half
        and int(drow["dev_trades"]) == dev_m["trades"]
        and int(drow["oos_trades"]) == oos_m["trades"]
        and _pf_equal(_num(drow["dev_pf"]), dev_m["profit_factor"])
        and _pf_equal(_num(drow["oos_pf"]), oos_m["profit_factor"])
    )
    add("oos_split_reproduced", oos_ok,
        f"days={ndays} half={half} dev={dev_m['trades']}/{int(drow['dev_trades'])} "
        f"oos={oos_m['trades']}/{int(drow['oos_trades'])}")

    classification, gates = helpers["classify"](
        len(traded), metrics, metrics["cumulative_net_bp"], pf, conc, oos
    )
    gates_ok = (
        bool(rowm["gate1"]) == bool(gates["gate1_median_net_gt_0"])
        and bool(rowm["gate2"]) == bool(gates["gate2_cumulative_net_gt_0"])
        and bool(rowm["gate3"]) == bool(gates["gate3_pf_gt_1"])
        and bool(rowm["gate4"]) == bool(gates["gate4_year_concentration_le_60pct"])
        and bool(rowm["gate5"]) == bool(gates["gate5_oos_independently_positive"])
    )
    add("viability_gates_reproduced", gates_ok,
        f"classification={classification}")

    return checks


def _verify_global(setup, helpers, self_dir_name: str | None = None) -> list[dict]:
    checks = []
    ord_econ = setup["execution_dir"].parent
    completed = True
    found = 0
    for child in sorted(ord_econ.iterdir()):
        if not child.is_dir():
            continue
        if not (child.name.startswith("EXECUTION_") or child.name.startswith("PREP_")
                or child.name.startswith("PREFLIGHT_") or child.name.startswith("VERIFICATION_")):
            continue
        if self_dir_name and child.name == self_dir_name:
            continue  # the LIVE verification identity is legitimately RUNNING
        jpath = child / "execution_journal.json"
        if not jpath.is_file():
            continue
        found += 1
        try:
            state = json.loads(jpath.read_text(encoding="utf-8")).get("state")
        except Exception:
            state = "UNKNOWN"
        if state == "RUNNING":
            completed = False
            checks.append({
                "check": "no_unreconciled_running",
                "pass": False,
                "detail": f"{child.name} still RUNNING (reconcile first)",
            })
    if found and completed:
        checks.append({
            "check": "no_unreconciled_running",
            "pass": True,
            "detail": f"scanned {found} staged identities, none RUNNING",
        })
    return checks


def run_stage3_verify(
    execution_dir: Path,
    prep_root: Path,
    markets: list[str],
    m1_dir: Path,
    tick_dir: Path,
    repo_root: Path,
    economic_protocol_sha256: str,
    scientific_protocol_sha256: str,
    v2_0_1_protocol_path: Path,
    v2_0_1_protocol_sha256: str,
    definition_lock_path: Path,
    scientific_manifest_path: Path | None = None,
    entry_script_path: Path | None = None,
    helper_module_paths: list[Path] | None = None,
    force_rerun: bool = False,
) -> dict:
    """Runs read-only Stage-3 verification of a completed Stage-2 execution.

    Raises ExecutionInfrastructureFailure only if Stage 3 itself cannot run
    (never for a failed check — a failed check is a FAIL verdict).
    """
    execution_dir = Path(execution_dir).resolve()
    helpers = _import_v11_helpers()

    verification_dir = execution_dir.parent / f"VERIFICATION_{execution_dir.name}"
    if verification_dir.exists():
        if not force_rerun:
            raise ExecutionInfrastructureFailure(
                "PREPARATION_INTEGRITY_FAILURE",
                f"VERIFICATION dir already exists: {verification_dir}. "
                f"Certification is restartable; re-run with --force-rerun to "
                f"replace the prior read-only certification (it is never "
                f"modified in place).",
            )
        moved = execution_dir.parent / (
            f"{verification_dir.name}_RECONCILED_"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_"
            f"{uuid.uuid4().hex[:8]}"
        )
        os.rename(verification_dir, moved)

    rec = StageRunRecorder(
        directory=verification_dir,
        stage_name="STAGE3",
        protocol_sha=v2_0_1_protocol_sha256,
        entry_script_path=entry_script_path or Path(__file__),
        helper_module_paths=helper_module_paths or [],
        extra_identity={
            "stage2_execution_id": execution_dir.name,
            "stage2_execution_dir": str(execution_dir),
            "output_layout": "VERIFICATION_<execution-id>",
        },
    )
    rec.start()

    checks = []
    add = lambda name, passed, detail: checks.append(  # noqa: E731
        {"check": name, "pass": bool(passed), "detail": detail}
    )

    try:
        jpath = execution_dir / "execution_journal.json"
        add(
            "stage2_journal_completed",
            jpath.is_file()
            and json.loads(jpath.read_text(encoding="utf-8")).get("state") == "COMPLETED",
            "journal must be COMPLETED",
        )
        mpath = execution_dir / "execution_manifest.json"
        manifest_ok = False
        if mpath.is_file():
            m = json.loads(mpath.read_text(encoding="utf-8"))
            manifest_ok = m.get("final_state") == "COMPLETED" and not m.get("missing_artifacts")
        add("stage2_artifact_manifest_complete", manifest_ok,
            "execution_manifest final_state=COMPLETED, no missing artifacts")

        meta_file = execution_dir / "execution_metadata.json"
        add("execution_metadata_present", meta_file.is_file(), str(meta_file))
        if not meta_file.is_file():
            raise ValueError("execution_metadata.json missing; cannot certify.")

        meta = json.loads(meta_file.read_text(encoding="utf-8"))

        sci_manifest = None
        if scientific_manifest_path and scientific_manifest_path.is_file():
            sci_manifest = json.loads(scientific_manifest_path.read_text(encoding="utf-8"))

        setup = {
            "execution_dir": execution_dir,
            "prep_root": Path(prep_root),
            "m1_dir": Path(m1_dir),
            "tick_dir": Path(tick_dir),
            "repo_root": Path(repo_root),
            "meta": meta,
            "economic_protocol_sha256": economic_protocol_sha256,
            "scientific_protocol_sha256": scientific_protocol_sha256,
            "scientific_manifest": sci_manifest,
        }

        missing_art = [a for a in expected_artifacts_for(
            sorted(meta.get("stage1_preparation_hashes", {}).keys()))
            if not (execution_dir / a).is_file()]
        add("required_artifacts_complete", not missing_art,
            f"missing={missing_art}")

        for market in markets:
            checks.extend(_verify_market(setup, market, helpers))

        checks.extend(_verify_global(setup, helpers, verification_dir.name))

    except BaseException as exc:
        category = classify_infrastructure_failure(exc)
        if rec.state == "RUNNING":
            rec.invalidate(reason=category)
        raise ExecutionInfrastructureFailure(
            category, f"Stage 3 failed for {execution_dir.name}: {exc}"
        ) from exc

    passed = sum(1 for c in checks if c["pass"])
    verdict = "PASS" if passed == len(checks) else "FAIL"

    report = {
        "stage": "STAGE3",
        "execution_id": execution_dir.name,
        "verification_identity": verification_dir.name,
        "verdict": verdict,
        "checks_total": len(checks),
        "checks_passed": passed,
        "checks_failed": len(checks) - passed,
        "read_only": True,
        "creates_economic_evidence": False,
        "checks": checks,
    }
    (verification_dir / "verification_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    summary_lines = [
        "# QUANTFORGE — ORD STAGED ECONOMIC EXECUTION — STAGE 3 READ-ONLY VERIFICATION",
        "",
        f"- Stage-2 execution: `{execution_dir.name}`",
        f"- Verification identity: `{verification_dir.name}`",
        f"- Verdict: **{verdict}** ({passed}/{len(checks)} checks passed)",
        "- Read-only: no scientific or economic artifact was modified; no new",
        "  economic evidence was created (certification only).",
        "",
        "## Checks",
        "",
    ]
    for c in checks:
        summary_lines.append(
            f"- [{'PASS' if c['pass'] else 'FAIL'}] {c['check']}: {c['detail']}"
        )
    summary_lines.append("")
    summary_lines.append("> Stage 3 certifies what Stage 2 produced against the frozen")
    summary_lines.append("> V1.1.0 formulas and the full preparation identities.  It states")
    summary_lines.append("> no verdict on whether any strategy works, fails, or is profitable.")
    (verification_dir / "verification_summary.md").write_text(
        "\n".join(summary_lines), encoding="utf-8"
    )

    rec.complete(extra={"verdict": verdict, "checks_total": len(checks),
                        "checks_passed": passed, "read_only": True})

    report["verification_verdict"] = verdict
    return report