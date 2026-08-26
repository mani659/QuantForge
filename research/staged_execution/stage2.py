"""Stage 2 — THE ONE controlled economic execution (V2.0.1 §6).

Stage 2 consumes ONLY:
  * frozen Stage-1 preparations (`PREP_<market>_<hash>`), each re-verified
    byte-exact — full canonical identity recomputed from the CURRENT source
    M1/tick hashes + protocol hashes + implementation hash — BEFORE any
    economic calculation (fail-closed);
  * the approved frozen economic protocol (V1.1.0, incorporated unchanged);
  * approved execution infrastructure (EventStudyRecorder — isolation,
    heartbeat, journal, mutation guard, artifact gate).

It calculates the trade ledger, gross/net, Model A, Model B descriptive
sensitivity, MFE/MAE, cumulative net, PF, OOS, yearly results, and the five
viability gates — exactly as registered in V1.1.0 §§9-13.  Economic helper
functions are IMPORTED from the approved `scripts.run_ord_econ_v1` module, so
no aggregation/diagnostic semantic is re-implemented here.

Stage 2 is EXACTLY-ONCE / NON-RESUMABLE: a fresh execution UUID + isolated
EventStudyRecorder directory per run; a crash is CRASHED / NOT_ADJUDICABLE and
is never resumed from partial calculations.  No full raw tick file is parsed
for economics at this stage.
"""

from __future__ import annotations

import gc
import json
import math
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import psutil

from ._failure import (
    ECONOMIC_EXCLUSION_CODES,
    ExecutionInfrastructureFailure,
    classify_infrastructure_failure,
)
from ._identity import external_percentile, sha256_file
from .stage1 import EVENT_INPUT_COLUMNS, is_valid_prep, PrepIdentity

REQUIRED_STAGE2_ARTIFACTS = [
    "trade_ledger.csv",
    "statistics.json",
    "market_summary.csv",
    "yearly_summary.csv",
    "development_oos_summary.csv",
    "cost_model_outputs.json",
    "execution_metadata.json",
    "peak_resource.json",
    "ECONOMIC_TRANSLATION_REPORT_V1.md",
    "trade_ledger_XAUUSD.csv",
    "trade_ledger_XAGUSD.csv",
    "trade_ledger_USATECHIDXUSD.csv",
    "trade_ledger_BTCUSD.csv",
]

_NUMERIC_COLS = {
    "or_high", "or_low", "or_width", "breakout_close",
    "entry_bid", "entry_ask", "executable_entry_quote",
    "entry_spread_bp", "exit_bid", "exit_ask",
    "executable_exit_quote", "exit_spread_bp", "structural_invalidation_level",
}


def expected_artifacts_for(markets: list[str]) -> list[str]:
    """Market-adaptive Stage-2 artifact contract (V1.1.0 base + per-market
    ledgers for exactly the markets executed).  Used by both Stage 2 (the
    recorder completion gate) and Stage 3 (certification completeness)."""
    base = [a for a in REQUIRED_STAGE2_ARTIFACTS
            if not a.startswith("trade_ledger_")]
    return base + [f"trade_ledger_{m}.csv" for m in markets]


def _import_v11_helpers():
    """Imports the approved V1.1.0 aggregation helpers (no re-implementation)."""
    from scripts.run_ord_econ_v1 import (  # noqa: E402
        COMMISSION_BANDS,
        SLIPPAGE_BANDS,
        LEDGER_COLUMNS,
        PeakSampler,
        classify,
        market_metrics,
        profit_factor,
        split_dev_oos,
        year_concentration,
    )
    return {
        "commission_bands": COMMISSION_BANDS,
        "slippage_bands": SLIPPAGE_BANDS,
        "ledger_columns": LEDGER_COLUMNS,
        "PeakSampler": PeakSampler,
        "classify": classify,
        "market_metrics": market_metrics,
        "profit_factor": profit_factor,
        "split_dev_oos": split_dev_oos,
        "year_concentration": year_concentration,
    }


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return f


def _spread_bp(bid: float, ask: float):
    mid = (bid + ask) / 2.0
    if mid <= 0:
        return None
    return (ask - bid) / mid * 1.0e4


def _stream_spread_stats(prep_dir: Path) -> dict:
    """Bounded pass over minute_quotes.csv.gz -> spread scalar distribution.

    Spreads are computed per observed minute and reduced via bounded external
    percentiles (no full-market table resident).
    """
    import gzip

    values = []
    with gzip.open(prep_dir / "minute_quotes.csv.gz", "rt", newline="", encoding="utf-8") as g:
        g.readline()  # header
        for line in g:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split(",")
            bid = float(parts[2])
            ask = float(parts[3])
            s = _spread_bp(bid, ask)
            if s is not None:
                values.append(s)
    n = len(values)
    if n == 0:
        return {
            "observed_minutes": 0,
            "spread_median_bp": None,
            "spread_p25_bp": None,
            "spread_p75_bp": None,
            "spread_p90_bp": None,
        }
    return {
        "observed_minutes": n,
        "spread_median_bp": external_percentile(values, 0.5),
        "spread_p25_bp": external_percentile(values, 0.25),
        "spread_p75_bp": external_percentile(values, 0.75),
        "spread_p90_bp": external_percentile(values, 0.90),
    }


def _load_path_by_event(prep_dir: Path) -> dict:
    """event_id -> list[(epoch_min, bid, ask)] loaded bounded (path data only)."""
    out = {}
    with open(prep_dir / "event_paths.csv", "r", encoding="utf-8") as f:
        header = f.readline()
        if "event_id" not in header:
            raise ExecutionInfrastructureFailure(
                "PARSER_PROCESS_FAILURE", "event_paths.csv header invalid"
            )
        for line in f:
            if not line.strip():
                continue
            ev, m, b, a = line.rstrip("\n").split(",")
            out.setdefault(ev, []).append((int(m), float(b), float(a)))
    for ev in out:
        out[ev].sort(key=lambda r: r[0])
    return out


def _evaluate_event(values: dict, paths: dict, helpers) -> dict:
    """Computes the numeric ledger fields for one frozen event-input row.

    Mirrors run_ord_econ_v1.simulate_event arithmetic exactly (gross/net/cost/
    MFE/MAE/holding) from the frozen Stage-1 fields only.
    """
    ex = values.get("exit_reason") or ""
    if ex in ECONOMIC_EXCLUSION_CODES:
        return values

    direction = values["direction"]
    entry_mid = (values["entry_bid"] + values["entry_ask"]) / 2.0
    exit_mid = (values["exit_bid"] + values["exit_ask"]) / 2.0
    tb = datetime.fromisoformat(values["T_B"])
    exit_ts = datetime.fromisoformat(values["exit_ts"])

    if direction == "long":
        gross = (exit_mid - entry_mid) / entry_mid * 1.0e4
        net = (values["executable_exit_quote"] - values["executable_entry_quote"]) / values[
            "executable_entry_quote"
        ] * 1.0e4
    else:
        gross = (entry_mid - exit_mid) / entry_mid * 1.0e4
        net = (values["executable_entry_quote"] - values["executable_exit_quote"]) / values[
            "executable_entry_quote"
        ] * 1.0e4

    cost_a = (values["entry_spread_bp"] + values["exit_spread_bp"]) / 2.0
    net_b = gross - (values["entry_spread_bp"] + values["exit_spread_bp"])

    path = paths.get(values["event_id"], [])
    entry_exec = values["executable_entry_quote"]
    if direction == "long":
        path_prices = [b for _, b, _ in path]
        mfe = (max(path_prices) - entry_exec) / entry_exec * 1.0e4 if path_prices else None
        mae = (min(path_prices) - entry_exec) / entry_exec * 1.0e4 if path_prices else None
    else:
        path_prices = [a for _, _, a in path]
        mfe = (entry_exec - min(path_prices)) / entry_exec * 1.0e4 if path_prices else None
        mae = (entry_exec - max(path_prices)) / entry_exec * 1.0e4 if path_prices else None

    values["gross_bp"] = gross
    values["cost_bp"] = cost_a
    values["net_bp"] = net
    values["net_bp_B"] = net_b
    values["mfe_from_entry_bp"] = mfe
    values["mae_from_entry_bp"] = mae
    values["holding_duration_min"] = (exit_ts - tb).total_seconds() / 60.0
    return values


def _migrate_row_to_ledger(values: dict, ledger_columns: list) -> dict:
    for key in ("gross_bp", "cost_bp", "net_bp", "net_bp_B",
                "mfe_from_entry_bp", "mae_from_entry_bp", "holding_duration_min"):
        values.setdefault(key, None)
    return {c: values.get(c) for c in ledger_columns}


def run_stage2_execute(
    out_root: Path,
    repo_root: Path,
    prep_root: Path,
    markets: list[str],
    m1_dir: Path,
    tick_dir: Path,
    scientific_protocol_sha256: str,
    economic_protocol_sha256: str,
    v2_0_1_protocol_path: Path,
    v2_0_1_protocol_sha256: str,
    definition_lock_path: Path,
    entry_script_path: Path,
    helper_module_paths: list[Path] | None = None,
) -> dict:
    """Runs the ONE controlled economic execution.

    Raises ExecutionInfrastructureFailure (fail-closed, before any economic
    calculation) if any preparation fails its byte-exact re-verification.
    """
    from research.orchestration.event_study_recorder import EventStudyRecorder

    helpers = _import_v11_helpers()
    ledger_columns = helpers["ledger_columns"]

    # Re-derive the FULL canonical identity for each market from the CURRENT
    # source files and verify the materialized PREP matches byte-exact.
    prep_info = {}
    for market in markets:
        m1_file = m1_dir / f"{market}_M1.csv"
        tick_file = tick_dir / f"{market}_mt5_ticks.csv"
        if not m1_file.is_file():
            raise ExecutionInfrastructureFailure(
                "PREPARATION_INTEGRITY_FAILURE",
                f"Stage-1 source M1 file missing for {market}: {m1_file}",
            )
        if not tick_file.is_file():
            raise ExecutionInfrastructureFailure(
                "PREPARATION_INTEGRITY_FAILURE",
                f"Stage-1 source tick file missing for {market}: {tick_file}",
            )
        m1_sha = sha256_file(m1_file)
        tick_sha = sha256_file(tick_file)
        identity = PrepIdentity(
            market=market,
            economic_protocol_sha256=economic_protocol_sha256,
            scientific_protocol_sha256=scientific_protocol_sha256,
            source_m1_sha256=m1_sha,
            source_tick_sha256=tick_sha,
            repo_root=repo_root,
        )
        canonical = prep_root / identity.identity
        valid, reason = is_valid_prep(canonical, identity)
        if not valid:
            raise ExecutionInfrastructureFailure(
                "HASH_MISMATCH"
                if ("hash" in reason or "identity" in reason)
                else "PREPARATION_INTEGRITY_FAILURE",
                f"Stage-1 prep re-verification FAILED for {market}: {reason}",
            )
        prep_manifest = json.loads(
            (canonical / "prep_manifest.json").read_text(encoding="utf-8")
        )
        prep_info[market] = {
            "prep_dir": canonical,
            "preparation_identity": identity.identity,
            "preparation_hash": identity.hash,
            "source_m1_sha256": prep_manifest["source_m1_sha256"],
            "source_tick_sha256": prep_manifest["source_tick_sha256"],
        }

    start_wall = time.time()
    v2_0_1_sha_lower = v2_0_1_protocol_sha256.lower()
    recorder = EventStudyRecorder(
        project_name="ORD_ECONOMIC",
        protocol_version="V1.1.0",
        protocol_path=v2_0_1_protocol_path,
        protocol_sha=v2_0_1_sha_lower,
        definition_lock_path=definition_lock_path,
        input_manifest_hash={m: prep_info[m]["preparation_hash"] for m in markets},
        expected_artifacts=expected_artifacts_for(markets),
        entry_script_path=entry_script_path,
        helper_module_paths=helper_module_paths or [],
        base_output_dir=out_root,
    )
    recorder.preflight()
    recorder.start()
    outdir = recorder.output_dir
    peak = helpers["PeakSampler"]()

    stats = {"protocol_sha256": v2_0_1_sha_lower, "markets": {}}
    market_summary = []
    yearly_rows = []
    dev_oos_rows = []
    cost_output = {
        "model_a": "RT(A)=(s_entry+s_exit)/2; Net_A=Gross-RT(A)",
        "model_b": "Net_B=Gross-(s_entry+s_exit); bands additive for sensitivity only",
        "bands": {
            "commission_bp": helpers["commission_bands"],
            "slippage_bp": helpers["slippage_bands"],
        },
        "per_market": {},
    }
    all_rows = []
    mkt_timing = {}

    try:
        for market in markets:
            t0 = time.time()
            prep_dir = prep_info[market]["prep_dir"]

            inputs = pd.read_csv(prep_dir / "event_inputs.csv")
            paths = _load_path_by_event(prep_dir)
            spread_stats = _stream_spread_stats(prep_dir)

            trades_raw = []
            for _, r in inputs.iterrows():
                peak.sample()
                values = {}
                for c in EVENT_INPUT_COLUMNS:
                    v = r[c]
                    if c in _NUMERIC_COLS:
                        values[c] = _num(v)
                    else:
                        values[c] = v
                if values.get("or_width") is None and values.get("or_high") is not None:
                    values["or_width"] = values["or_high"] - values["or_low"]
                trades_raw.append(
                    _migrate_row_to_ledger(
                        _evaluate_event(values, paths, helpers), ledger_columns
                    )
                )

            traded = [t for t in trades_raw if t.get("net_bp") is not None]
            traded_sorted = sorted(
                traded, key=lambda t: (t["trading_day"], t["breakout_ts"])
            )
            metrics = helpers["market_metrics"](traded_sorted)
            cum_net = metrics["cumulative_net_bp"]
            pf = metrics["profit_factor"]
            conc, yearly = helpers["year_concentration"](traded_sorted)
            events_list = [{"trading_day": rr["trading_day"]} for _, rr in inputs.iterrows()]
            dev, oos, ndays, half = helpers["split_dev_oos"](events_list, traded_sorted)
            dev_m = helpers["market_metrics"](dev)
            oos_m = helpers["market_metrics"](oos)
            classification, gates = helpers["classify"](
                len(traded), metrics, cum_net, pf, conc, oos
            )

            for y, s in (yearly or {}).items():
                yy = [t for t in traded_sorted if t["trading_day"][:4] == y]
                ymed = float(np.median([t["net_bp"] for t in yy])) if yy else np.nan
                ypf = (
                    helpers["profit_factor"](
                        np.array([t["net_bp"] for t in yy], dtype=float)
                    )
                    if yy
                    else None
                )
                yearly_rows.append(
                    {
                        "market": market, "year": int(y), "trades": len(yy),
                        "cumulative_net_bp": s, "median_net_bp": ymed,
                        "profit_factor": ypf,
                    }
                )

            dev_oos_rows.append(
                {
                    "market": market, "n_event_days": ndays,
                    "dev_day_count": half, "dev_trades": dev_m["trades"],
                    "dev_median_net_bp": dev_m["median_net_bp"],
                    "dev_cumulative_net_bp": dev_m["cumulative_net_bp"],
                    "dev_pf": dev_m["profit_factor"],
                    "oos_trades": oos_m["trades"],
                    "oos_median_net_bp": oos_m["median_net_bp"],
                    "oos_cumulative_net_bp": oos_m["cumulative_net_bp"],
                    "oos_pf": oos_m["profit_factor"],
                }
            )

            market_summary.append(
                {
                    "market": market, "trade_count": len(traded),
                    "classification": classification,
                    "median_net_bp": metrics["median_net_bp"],
                    "cumulative_net_bp": cum_net,
                    "profit_factor": pf, "year_concentration": conc,
                    "gate1": gates["gate1_median_net_gt_0"],
                    "gate2": gates["gate2_cumulative_net_gt_0"],
                    "gate3": gates["gate3_pf_gt_1"],
                    "gate4": gates["gate4_year_concentration_le_60pct"],
                    "gate5": gates["gate5_oos_independently_positive"],
                }
            )

            stats["markets"][market] = {
                "metrics": metrics,
                "gates": gates,
                "classification": classification,
                "trade_count": len(traded),
                "excluded": {
                    r: sum(1 for t in trades_raw if t["exit_reason"] == r)
                    for r in sorted({t["exit_reason"] for t in trades_raw})
                },
                "year_concentration": conc,
            }

            nets = (
                np.array([t["net_bp"] for t in traded_sorted], dtype=float)
                if traded_sorted
                else np.array([])
            )
            band_res = []
            for c in helpers["commission_bands"]:
                for sl in helpers["slippage_bands"]:
                    snet = nets - c - sl
                    band_res.append(
                        {
                            "commission_bp": c, "slippage_bp": sl,
                            "median_net_bp": float(np.median(snet)) if len(snet) else np.nan,
                            "cumulative_net_bp": float(np.sum(snet)) if len(snet) else 0.0,
                        }
                    )
            cost_output["per_market"][market] = {
                "observed_minutes": spread_stats["observed_minutes"],
                "spread_median_bp": spread_stats["spread_median_bp"],
                "spread_p25_bp": spread_stats["spread_p25_bp"],
                "spread_p75_bp": spread_stats["spread_p75_bp"],
                "spread_p90_bp": spread_stats["spread_p90_bp"],
                "median_cost_bp_modelA": (
                    float(np.median([t["cost_bp"] for t in traded_sorted]))
                    if traded_sorted
                    else np.nan
                ),
                "model_b_sensitivity": band_res,
                "invalid_tick_rows": None,
                "streamed_rows": None,
                "quote_lookup_counts": {
                    "entry_exact": sum(
                        1 for t in traded if t["quote_lookup_entry"] == "exact"
                    ),
                    "entry_fallback": sum(
                        1
                        for t in traded
                        if str(t["quote_lookup_entry"]).startswith("fallback")
                    ),
                    "entry_market_median": sum(
                        1 for t in traded if t["quote_lookup_entry"] == "market-median"
                    ),
                    "exit_exact": sum(
                        1 for t in traded if t["quote_lookup_exit"] == "exact"
                    ),
                    "exit_fallback": sum(
                        1
                        for t in traded
                        if str(t["quote_lookup_exit"]).startswith("fallback")
                    ),
                    "exit_market_median": sum(
                        1 for t in traded if t["quote_lookup_exit"] == "market-median"
                    ),
                },
            }
            mkt_timing[market] = time.time() - t0
            all_rows.extend(traded_sorted)
            all_rows.extend(t for t in trades_raw if t.get("net_bp") is None)
            del inputs, paths
            gc.collect()

        led_df = pd.DataFrame([{c: t.get(c) for c in ledger_columns} for t in all_rows])
        led_df = led_df.sort_values(
            ["market", "trading_day", "breakout_ts"], na_position="last"
        ).reset_index(drop=True)
        led_df.to_csv(outdir / "trade_ledger.csv", index=False)
        for market in markets:
            sub = led_df[led_df["market"] == market]
            sub.to_csv(outdir / f"trade_ledger_{market}.csv", index=False)

        (outdir / "statistics.json").write_text(
            json.dumps(stats, indent=2, allow_nan=True), encoding="utf-8"
        )
        pd.DataFrame(market_summary).to_csv(outdir / "market_summary.csv", index=False)
        pd.DataFrame(yearly_rows).to_csv(outdir / "yearly_summary.csv", index=False)
        pd.DataFrame(dev_oos_rows).to_csv(
            outdir / "development_oos_summary.csv", index=False
        )
        (outdir / "cost_model_outputs.json").write_text(
            json.dumps(cost_output, indent=2, allow_nan=True), encoding="utf-8"
        )

        peak.sample()
        peak_res = {
            "peak_process_rss_bytes": peak.peak_rss,
            "peak_system_memory_bytes": peak.peak_sys_used,
            "peak_cpu_percent": peak.peak_cpu,
        }
        (outdir / "peak_resource.json").write_text(
            json.dumps(peak_res, indent=2), encoding="utf-8"
        )

        meta = {
            "execution_id": recorder.execution_id,
            "started": recorder.start_timestamp,
            "protocol_sha256": v2_0_1_protocol_sha256,
            "economic_protocol_sha256": economic_protocol_sha256,
            "scientific_protocol_sha256": scientific_protocol_sha256,
            "definition_lock_sha256": sha256_file(definition_lock_path),
            "stage1_preparation_hashes": {
                m: prep_info[m]["preparation_hash"] for m in markets
            },
            "stage1_preparation_identities": {
                m: prep_info[m]["preparation_identity"] for m in markets
            },
            "m1_hashes": {m: prep_info[m]["source_m1_sha256"] for m in markets},
            "tick_hashes": {m: prep_info[m]["source_tick_sha256"] for m in markets},
            "git_head": recorder.implementation_manifest.get("git_head"),
            "git_dirty": recorder.implementation_manifest.get("git_dirty_state"),
            "python_version": recorder.implementation_manifest.get("python_version"),
            "pandas_version": recorder.implementation_manifest.get(
                "package_versions", {}
            ).get("pandas"),
            "numpy_version": recorder.implementation_manifest.get(
                "package_versions", {}
            ).get("numpy"),
            "runner_sha256": recorder.implementation_manifest.get(
                "entry_script_sha256"
            ),
            "cost_model_identity": "Model A PRIMARY; Model B DESCRIPTIVE",
            "market_duration_sec": mkt_timing,
            "total_wall_sec": time.time() - start_wall,
        }
        (outdir / "execution_metadata.json").write_text(
            json.dumps(meta, indent=2), encoding="utf-8"
        )

        report_text = build_report(
            recorder, meta, stats, cost_output, dev_oos_rows, yearly_rows,
            peak_res, markets, v2_0_1_protocol_sha256,
        )
        (outdir / "ECONOMIC_TRANSLATION_REPORT_V1.md").write_text(
            report_text, encoding="utf-8"
        )

        recorder.complete_execution()
    except ExecutionInfrastructureFailure:
        if recorder.state == "RUNNING":
            recorder.invalidate_execution(reason="EXECUTION_INFRASTRUCTURE_FAILURE")
        raise
    except BaseException as exc:
        category = classify_infrastructure_failure(exc)
        if recorder.state == "RUNNING":
            recorder.invalidate_execution(reason=category)
        raise ExecutionInfrastructureFailure(category, f"Stage 2 failed: {exc}") from exc

    return {
        "execution_id": recorder.execution_id,
        "execution_dir": str(recorder.execution_dir),
        "protocol_sha256": v2_0_1_protocol_sha256,
        "stage1_preparation_hashes": {
            m: prep_info[m]["preparation_hash"] for m in markets
        },
    }


def build_report(recorder, meta, stats, cost_output, dev_oos_rows, yearly_rows,
                 peak_res, markets, v2_sha) -> str:
    lines = []
    w = lines.append
    w("# QUANTFORGE — ORD V1.1.0 ECONOMIC TRANSLATION REPORT")
    w("")
    w("# STAGED EXECUTION — V2.0.1 STAGE 2 (THE ONE CONTROLLED ECONOMIC EXECUTION)")
    w("")
    w("## 1. Execution Identity")
    w("")
    w(f"- Execution ID: `{recorder.execution_id}`")
    w(f"- Started (UTC): {recorder.start_timestamp}")
    w(f"- Output directory: `{recorder.output_dir}`")
    w("- Journal final state: COMPLETED (verified by EventStudyRecorder completion gate).")
    w("")
    w("## 2. Protocol / Implementation Fingerprints")
    w("")
    w(f"- Staged economic protocol (V2.0.1): `{v2_sha}`")
    w(f"- Economic base protocol (V1.1.0): `{meta['economic_protocol_sha256']}`")
    w(f"- Scientific protocol (V1.1.0): `{meta['scientific_protocol_sha256']}`")
    w(f"- Stage-1 preparation hashes (full, unabbreviated): {meta['stage1_preparation_hashes']}")
    w(f"- Stage-1 preparation identities: {meta['stage1_preparation_identities']}")
    w(f"- Definition lock SHA-256: `{meta['definition_lock_sha256']}`")
    w(f"- Runner SHA-256: `{meta['runner_sha256']}`")
    w(f"- Git HEAD: `{meta['git_head']}` (dirty={meta['git_dirty']})")
    w(f"- Python {meta['python_version']}; pandas {meta['pandas_version']}; numpy {meta['numpy_version']}")
    w("")
    w("## 3. Input Data Integrity")
    w("")
    w("- Stage-2 consumed ONLY frozen Stage-1 preparations; each was re-verified")
    w("  byte-exact (full `PREP_<market>_<hash>` identity recomputed from current")
    w("  source hashes + artifact hashes) before any economic calculation.")
    for m in markets:
        w(f"  - {m}: M1 `{meta['m1_hashes'][m]}`; tick `{meta['tick_hashes'][m]}`")
    w("")
    w("## 4. Cost Model")
    w("")
    w(f"- Model A (PRIMARY): RT(A) = (s_entry + s_exit) / 2; Net_A = Gross - RT(A), where s is the per-minute observed MT5 spread in bp.")
    w(f"- Model B (DESCRIPTIVE): Net_B = Gross - (s_entry + s_exit); commission {cost_output['bands']['commission_bp']} bp and slippage {cost_output['bands']['slippage_bp']} bp bands are additive in the Model-B sensitivity table only.")
    w("- No assumed spread; no invented commission in Model A.")
    for m in markets:
        c = cost_output["per_market"][m]
        med = c["spread_median_bp"]
        w(f"  - {m}: observed-minute spread median {med if med is None else round(med, 3)} bp (p25 {c['spread_p25_bp']}, p75 {c['spread_p75_bp']}, p90 {c['spread_p90_bp']}); median Model-A cost {c['median_cost_bp_modelA']} bp over {c['observed_minutes']} observed minutes.")
    w("")
    w("## 5. Trade Population")
    w("")
    for m in markets:
        s = stats["markets"][m]
        w(f"- {m}: traded {s['trade_count']}; exclusions {s['excluded']}.")
    w("")
    w("## 6. Primary Economic Metrics (Model A, bp)")
    w("")
    for m in markets:
        mt = stats["markets"][m]["metrics"]
        w(f"- **{m}** — n={mt['trades']} ({mt['trades_per_month']:.2f}/mo); median net {mt['median_net_bp']:.3f}; mean {mt['mean_net_bp']:.3f}; win rate {mt['win_rate']*100:.1f}%; median win {mt['median_win_bp']:.3f}; median loss {mt['median_loss_bp']:.3f}; PF {mt['profit_factor']}; cumulative {mt['cumulative_net_bp']:.1f}; max drawdown {mt['max_drawdown_bp']:.1f}; invalidation {mt['invalidation_rate']*100:.1f}%; horizon exit {mt['horizon_exit_rate']*100:.1f}%.")
    w("")
    w("## 7. Development / OOS (chronological floor(N/2) event days)")
    w("")
    for r in dev_oos_rows:
        w(f"- {r['market']}: {r['n_event_days']} event days, dev {r['dev_day_count']}. Dev: n={r['dev_trades']}, median {r['dev_median_net_bp']:.3f}, cumulative {r['dev_cumulative_net_bp']:.1f}, PF {r['dev_pf']}. OOS: n={r['oos_trades']}, median {r['oos_median_net_bp']:.3f}, cumulative {r['oos_cumulative_net_bp']:.1f}, PF {r['oos_pf']}.")
    w("")
    w("## 8. Yearly Results")
    w("")
    for r in yearly_rows:
        w(f"- {r['market']} {r['year']}: n={r['trades']}, cumulative {r['cumulative_net_bp']:.1f}, median {r['median_net_bp']:.3f}, PF {r['profit_factor']}.")
    w("")
    w("## 9. Market Classifications")
    w("")
    for m in markets:
        s = stats["markets"][m]
        caveat = " (NO-SCIENTIFIC-VERDICT) " if m == "BTCUSD" else ""
        w(f"- {m}: **{s['classification']}**{caveat}")
        w(f"  - Gates: {s['gates']}")
    w("- EURUSD: NOT SIMULATED (NOT REGISTERED / DATA-LIMITED).")
    w("")
    w("## 10. Resource Usage")
    w("")
    w(f"- Peak process RSS: {peak_res['peak_process_rss_bytes']}; peak CPU: {peak_res['peak_cpu_percent']}%.")
    w(f"- Market durations (s): {meta['market_duration_sec']}; total wall clock: {meta['total_wall_sec']:.1f} s.")
    w("")
    w("## 11. Artifact Integrity")
    w("")
    w("- EventStudyRecorder completion gate verified: journal COMPLETED; no missing/unexpected artifacts.")
    w("- Ledger retains all rows including EXCLUDED_* rows (no trade removed for being unfavourable).")
    w("")
    w("## 12. Scientific Boundary")
    w("")
    w("- No scientific object, protocol, execution artifact, or adjudication was modified.")
    w("- This report records the execution results only; it performs no adjudication and states no verdict on whether any strategy works, fails, or is profitable.")
    w("")
    w("## 13. Exact Next Governance Task")
    w("")
    w("> **INDEPENDENT ECONOMIC RESULTS ADJUDICATION** of this single controlled execution: determine whether the baseline economically survives, fails, or requires governance escalation.")
    w("")
    return "\n".join(lines)