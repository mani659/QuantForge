"""Stage 3 — read-only verification CLI (V2.0.1 §7).

Certifies a completed Stage-2 execution against the frozen V1.1.0 formulas and
the full Stage-1 preparation identities.  Read-only with respect to all
scientific and economic artifacts; its own output lives in
`VERIFICATION_<execution-id>/` and is restartable (`--force-rerun`).
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

from research.staged_execution._failure import ExecutionInfrastructureFailure  # noqa: E402
from research.staged_execution.stage3 import run_stage3_verify  # noqa: E402

V2_0_1_PROTOCOL = ROOT / "output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_1_AMENDED.md"
V2_0_1_PROTOCOL_SHA = "1D3EE7A6A9FD747CB57A716B43C5EB80BB7D6016011D2C4DF9F0814CC196968D"
ECONOMIC_PROTOCOL_SHA = "8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663"
SCIENTIFIC_PROTOCOL_SHA = "85263B848E49E718A099CAFE8FA7FE6F8AE0C74EC04C46477A0FCD1D9E759C06"
DEFLOCK = ROOT / "output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md"
SCIENTIFIC_MANIFEST = (
    ROOT
    / "output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/implementation_manifest.json"
)
M1_DIR = ROOT / "data/m1"
TICK_DIR = ROOT / "data/tick"
MARKETS = ["XAUUSD", "XAGUSD", "USATECHIDXUSD", "BTCUSD"]
PREP_ROOT = ROOT / "output/research_discovery/ORD_ECONOMIC/V1.1.0"

HELPERS = [
    ROOT / "research/staged_execution/_identity.py",
    ROOT / "research/staged_execution/_failure.py",
    ROOT / "research/staged_execution/_stage_recorder.py",
    ROOT / "research/staged_execution/stage1.py",
    ROOT / "research/staged_execution/stage2.py",
    ROOT / "research/staged_execution/stage3.py",
    ROOT / "scripts/run_ord_econ_v1.py",
    ROOT / "research/orchestration/event_study_recorder.py",
]


def main():
    p = argparse.ArgumentParser(description="ORD Stage-3 read-only verification")
    p.add_argument("execution_dir", type=Path, help="Stage-2 EXECUTION_* directory")
    p.add_argument("--repo-root", type=Path, default=ROOT)
    p.add_argument("--prep-root", type=Path, default=PREP_ROOT)
    p.add_argument("--markets", nargs="+", default=MARKETS)
    p.add_argument("--m1-dir", type=Path, default=M1_DIR)
    p.add_argument("--tick-dir", type=Path, default=TICK_DIR)
    p.add_argument("--economic-protocol-sha", default=ECONOMIC_PROTOCOL_SHA)
    p.add_argument("--scientific-protocol-sha", default=SCIENTIFIC_PROTOCOL_SHA)
    p.add_argument("--v2-protocol-path", type=Path, default=V2_0_1_PROTOCOL)
    p.add_argument("--v2-protocol-sha", default=V2_0_1_PROTOCOL_SHA)
    p.add_argument("--definition-lock", type=Path, default=DEFLOCK)
    p.add_argument("--scientific-manifest", type=Path, default=SCIENTIFIC_MANIFEST)
    p.add_argument("--force-rerun", action="store_true")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    try:
        report = run_stage3_verify(
            execution_dir=args.execution_dir,
            prep_root=args.prep_root,
            markets=list(args.markets),
            m1_dir=args.m1_dir,
            tick_dir=args.tick_dir,
            repo_root=args.repo_root,
            economic_protocol_sha256=args.economic_protocol_sha,
            scientific_protocol_sha256=args.scientific_protocol_sha,
            v2_0_1_protocol_path=args.v2_protocol_path,
            v2_0_1_protocol_sha256=args.v2_protocol_sha,
            definition_lock_path=args.definition_lock,
            scientific_manifest_path=args.scientific_manifest,
            entry_script_path=Path(__file__),
            helper_module_paths=HELPERS,
            force_rerun=args.force_rerun,
        )
    except ExecutionInfrastructureFailure as exc:
        print(f"[STAGE3] {exc}")
        sys.exit(1)

    print(f"[STAGE3] verdict={report['verdict']} "
          f"({report['checks_passed']}/{report['checks_total']} checks)")
    if args.verbose:
        print(json.dumps(report, indent=2, default=str))
    sys.exit(0 if report["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()