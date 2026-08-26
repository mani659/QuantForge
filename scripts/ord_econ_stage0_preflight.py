"""Stage 0 — repeatable preflight CLI (V2.0.1 §3).

Runs `run_stage0_preflight` per market and prints the PASS/FAIL verdict as a
repeatable finding.  Verdict FAIL is a finding (exit code 1), not a crash; only
component failure of the preflight itself raises the registered
`EXECUTION-INFRASTRUCTURE FAILURE` class.
"""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from research.staged_execution.stage0 import run_stage0_preflight  # noqa: E402

V2_0_1_PROTOCOL_SHA = "1D3EE7A6A9FD747CB57A716B43C5EB80BB7D6016011D2C4DF9F0814CC196968D"
M1_DIR = ROOT / "data/m1"
TICK_DIR = ROOT / "data/tick"
MARKETS = ["XAUUSD", "XAGUSD", "USATECHIDXUSD", "BTCUSD"]
OUT_ROOT = ROOT / "output/research_discovery/ORD_ECONOMIC/V1.1.0"


def main():
    p = argparse.ArgumentParser(description="ORD Stage-0 preflight")
    p.add_argument("--market", choices=MARKETS + ["ALL", "all"], default="ALL")
    p.add_argument("--out-root", type=Path, default=OUT_ROOT)
    p.add_argument("--m1-dir", type=Path, default=M1_DIR)
    p.add_argument("--tick-dir", type=Path, default=TICK_DIR)
    p.add_argument("--protocol-sha", default=V2_0_1_PROTOCOL_SHA)
    p.add_argument("--probe-rows", type=int, default=10_000_000)
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    markets = MARKETS if args.market in ("ALL", "all") else [args.market]
    results = {}
    any_fail = False
    for market in markets:
        report = run_stage0_preflight(
            out_root=args.out_root,
            market=market,
            tick_path=args.tick_dir / f"{market}_mt5_ticks.csv",
            m1_path=args.m1_dir / f"{market}_M1.csv",
            probe_rows=args.probe_rows,
            entry_script_path=Path(__file__),
            helper_module_paths=[
                ROOT / "research/staged_execution/_identity.py",
                ROOT / "research/staged_execution/_failure.py",
                ROOT / "research/staged_execution/_stage_recorder.py",
                ROOT / "research/staged_execution/stage0.py",
            ],
            protocol_sha256=args.protocol_sha,
        )
        results[market] = report
        any_fail = any_fail or report["verdict"] != "PASS"
        print(f"[{market}] STAGE0 verdict={report['verdict']} run={report['run_id']}")
        if args.verbose:
            print(json.dumps(report, indent=2, default=str))

    summary = {
        "stage": "STAGE0",
        "protocol_sha256": args.protocol_sha,
        "markets": {m: results[m]["verdict"] for m in markets},
        "overall": "FAIL" if any_fail else "PASS",
    }
    print(json.dumps(summary, indent=2))
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()