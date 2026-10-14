"""TASK146 single bounded measurement run (VS-TSMOM-01, approved chain).
Gates G4/G5/G6/G7 verified pre-invocation (see task report). Single run.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vs_tsmom_engine as E

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", ".."))
DATA = os.path.join(REPO, "data", "fred", "fred_NASDAQ100.csv")
EXPECTED_SHA = ("1196c3f2dca171c1b56b4bbe2cc1fcd51ec7ea1f30bb74d7c3cfc2a313"
                "ffe52f")


def main():
    assert os.path.isfile(DATA), "data file missing: " + DATA
    sha = E.sha256_file(DATA)
    assert sha == EXPECTED_SHA, "SHA MISMATCH: " + sha
    s, meta = E.load_fred(DATA)
    E.check_integrity(s)
    rows, skips = E.evaluate_panel(s)
    assert len(rows) > 0, "no evaluable months"
    res = E.analyze(rows)
    res["label"] = E.decide_label(res)
    res["skips"] = skips
    res["meta"] = meta
    res["config"] = E.SPEC
    res["yearly"] = E.diagnostics(rows)["yearly"]
    res["turnover"] = E.diagnostics(rows)["turnover"]
    res["total_cost_s"] = E.diagnostics(rows)["total_cost_s"]
    res["vol_tracking"] = E.diagnostics(rows)["vol_tracking"]
    res["cost_grid"] = E.cost_grid(s)
    res["financing_stress"] = E.financing_stress(rows)
    with open(os.path.join(ROOT, "monthly_series.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["month", "w", "f", "R", "gross_s",
                                           "gross_f", "gross_p", "cost_s",
                                           "cost_f", "cost_p", "net_s",
                                           "net_f", "net_p"])
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(ROOT, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print("months=%d label=%s mean_d1=%.6f ratio=%s" % (
        res["n"], res["label"], res["mean_d1"], res["ratio"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
