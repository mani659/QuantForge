"""TASK120 single bounded measurement run (CAND025-RM-01, approved chain).
Phase 1 (outcome-blind): load -> M5 -> enumerate -> COUNT GATE.
  count < 157 -> write gate-failure record, exit 3, NO returns computed.
Phase 2 (only if gate passes): evaluate -> analyze -> T4 -> write outputs.
Single invocation. Fixed config: see run_config.md (frozen pre-outcome).
"""
import csv
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cand025_engine as E

ROOT = os.path.dirname(os.path.abspath(__file__))
# task120/ -> regression_bot_audit -> prototypes -> output -> repo root:
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", ".."))
DATA = os.path.join(REPO, "data", "m1", "USATECHIDXUSD_M1.csv")
EXPECTED_SHA = "39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6"


def main():
    assert os.path.isfile(DATA), "data file missing: " + DATA
    sha = E.sha256_file(DATA)
    assert sha == EXPECTED_SHA, "SHA MISMATCH: " + sha
    m1, meta = E.load_m1(DATA)
    m5 = E.to_m5_complete(m1)
    events, skips = E.enumerate_events(m5)
    count = len(events)
    phase1 = {"data_sha256": sha, "meta": meta, "m5_bars": len(m5),
              "event_count": count, "skips": skips}
    with open(os.path.join(ROOT, "phase1_count.json"), "w") as fh:
        json.dump(phase1, fh, indent=1, sort_keys=True)
    print("phase1: count=%d skips=%s" % (count, skips), flush=True)
    if count < 157:
        with open(os.path.join(ROOT, "GATE_FAILURE.md"), "w") as fh:
            fh.write("# COUNT GATE FAILURE\n\nFrozen record N=157; "
                     "enumerated %d rule-satisfying events on the verified "
                     "panel. Possible ATR-definition or panel discrepancy. "
                     "No returns computed. No second mapping attempt "
                     "(would be a parameter search).\n" % count)
        print("COUNT GATE FAILED -> stop, no returns", flush=True)
        return 3
    disc = ("record-consistent" if count == 157
            else "contingency: full-set primary; verification-subset "
                 "subclause UNEXECUTABLE (no G1 event list on any record)")
    print("count rule: " + disc, flush=True)
    rows = E.evaluate(events)
    res = E.analyze(rows)
    res["t4"] = E.t4_flag(m5, events)
    res["count_disposition"] = disc
    res["skips"] = skips
    res["config"] = E.SPEC
    with open(os.path.join(ROOT, "events.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "entry_open", "exit_open",
                                           "dir", "gross", "net2", "net3"])
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(ROOT, "summary.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print("phase2: n=%d t1=%s t3=%s t4=%s" % (
        res["n"], res.get("t1_pass"), res.get("t3_pass"), res.get("t4")),
        flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
