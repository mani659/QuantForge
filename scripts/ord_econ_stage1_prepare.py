"""Stage 1 — frozen preparation CLI (V2.0.1 §4).

Registers this file in the canonical preparation-implementation hash set
(field 7 of `build_canonical_manifest`); see `_PREP_SOURCE_FILES` in
`research/staged_execution/_identity.py`.

Consumes, one market at a time: the frozen event table, the frozen M1 file and
the frozen tick file.  Produces the immutable `PREP_<market>_<FULL_SHA256>`
directory (prep_manifest + minute index + minute quotes.gz + event inputs +
event paths).  Computes NO economic result.  Reuses an existing completed
preparation only when it matches the current frozen identity byte-exact.
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

from research.staged_execution.stage1 import run_stage1_prepare  # noqa: E402

V2_0_1_PROTOCOL_SHA = "1D3EE7A6A9FD747CB57A716B43C5EB80BB7D6016011D2C4DF9F0814CC196968D"
ECONOMIC_PROTOCOL_SHA = "8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663"
SCIENTIFIC_PROTOCOL_SHA = "85263B848E49E718A099CAFE8FA7FE6F8AE0C74EC04C46477A0FCD1D9E759C06"
EVENT_TABLE = (
    ROOT
    / "output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/event_table_all_markets.csv"
)
M1_DIR = ROOT / "data/m1"
TICK_DIR = ROOT / "data/tick"
MARKETS = ["XAUUSD", "XAGUSD", "USATECHIDXUSD", "BTCUSD"]
OUT_ROOT = ROOT / "output/research_discovery/ORD_ECONOMIC/V1.1.0"

HELPERS = [
    ROOT / "research/staged_execution/_identity.py",
    ROOT / "research/staged_execution/_failure.py",
    ROOT / "research/staged_execution/_stage_recorder.py",
    ROOT / "research/staged_execution/stage1.py",
]


def main():
    p = argparse.ArgumentParser(description="ORD Stage-1 frozen preparation")
    p.add_argument("--market", choices=MARKETS + ["ALL", "all"], default="ALL")
    p.add_argument("--out-root", type=Path, default=OUT_ROOT)
    p.add_argument("--repo-root", type=Path, default=ROOT)
    p.add_argument("--m1-dir", type=Path, default=M1_DIR)
    p.add_argument("--tick-dir", type=Path, default=TICK_DIR)
    p.add_argument("--event-table", type=Path, default=EVENT_TABLE)
    p.add_argument("--economic-protocol-sha", default=ECONOMIC_PROTOCOL_SHA)
    p.add_argument("--scientific-protocol-sha", default=SCIENTIFIC_PROTOCOL_SHA)
    p.add_argument("--v2-protocol-sha", default=V2_0_1_PROTOCOL_SHA)
    p.add_argument("--force-rebuild", action="store_true")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    markets = MARKETS if args.market in ("ALL", "all") else [args.market]
    results = {}
    for market in markets:
        res = run_stage1_prepare(
            out_root=args.out_root,
            repo_root=args.repo_root,
            market=market,
            m1_path=args.m1_dir / f"{market}_M1.csv",
            tick_path=args.tick_dir / f"{market}_mt5_ticks.csv",
            event_table_path=args.event_table,
            economic_protocol_sha256=args.economic_protocol_sha,
            scientific_protocol_sha256=args.scientific_protocol_sha,
            v2_0_1_protocol_sha256=args.v2_protocol_sha,
            force_rebuild=args.force_rebuild,
            entry_script_path=Path(__file__),
            helper_module_paths=HELPERS,
        )
        results[market] = res
        print(f"[{market}] mode={res['mode']} identity={res['preparation_identity']}")
        if args.verbose:
            print(json.dumps(res, indent=2, default=str))

    print(json.dumps({"stage": "STAGE1", "results": results}, indent=2, default=str))


if __name__ == "__main__":
    main()