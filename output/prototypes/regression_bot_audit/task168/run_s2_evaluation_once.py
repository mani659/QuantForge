"""TASK168 — single authorized execution of frozen PROTO-S2-001.

Run ONCE under 168_s2_evaluation_authorization.md. No variants, no rerun.
The frozen engine (s2_engine.py, hash-verified pre-start) is the sole
authority for window, cost, bootstrap and verdict arithmetic.
"""
import csv
import hashlib
import json
import sys

import numpy as np

sys.path.insert(0, "output/prototypes/s2_newyear_week")
import s2_engine as eng  # noqa: E402

DATA = "output/prototypes/lane_b_batch1/data/SPY.csv"
DATA_SHA = "483919f897326b261a669bc595a37112b4de5222c4ad0ed84da08060f4b71231"
SPEC_SHA = "5a318e7e47263c67dc308adf9e326122e56b285e5eaaf585274867525a47eb94"
IMPL_SHA = "2892c8b5f3f9c13fe1dd3317d45f5f33725437be1f3936501943699dcff97f7b"
OUT = "output/prototypes/regression_bot_audit/task168"

print("== TASK168 single authorized execution: PROTO-S2-001 ==")

# --- integrity gates before any outcome arithmetic ---
got = eng.sha256_file(DATA)
assert got == DATA_SHA, "data hash mismatch: " + got
print("data sha256 OK:", got[:16])
assert eng.sha256_file("output/prototypes/s2_newyear_week/s2_engine.py") == IMPL_SHA
print("impl sha256 OK:", IMPL_SHA[:16])

s, meta = eng.load_panel(DATA)
print("panel:", meta)
eng.check_yearly_missing(s)
print("yearly missing check OK (<=5% every year)")

windows, skips = eng.january_windows(s)
events = eng.evaluate(windows)
res = eng.analyze(events)
label = eng.decide_label(res)
ctl = eng.control_leg(windows)
print("eligible windows:", res["n"], "| skips:", skips)

# reproducibility cross-check: regenerate the frozen bootstrap draws
rng = np.random.default_rng(eng.SPEC["seed"])
v = np.array([e["net"] for e in events])
bm = np.array([rng.choice(v, size=len(v), replace=True).mean()
               for _ in range(eng.SPEC["boot_b"])])
ci_re = [float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))]
assert ci_re == res["ci95"], "bootstrap regeneration mismatch"
print("bootstrap regen matches engine CI exactly")

cum_strategy = float(np.prod(1.0 + v) - 1.0)

# --- machine-readable artifacts ---
with open(OUT + "/168_s2_event_results.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["year", "entry_date", "exit_date", "entry_px", "exit_px", "net"])
    for win, ev in zip(windows, events):
        w.writerow([win["year"], str(win["entry_date"].date()),
                    str(win["exit_date"].date()),
                    repr(win["entry_px"]), repr(win["exit_px"]), repr(ev["net"])])

with open(OUT + "/168_s2_bootstrap_replicates.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["replicate", "boot_mean"])
    for i, x in enumerate(bm):
        w.writerow([i, repr(float(x))])

results = {
    "protocol": "PROTO-S2-001 v1-frozen",
    "authorization": "task168/168_s2_evaluation_authorization.md (owner 2026-10-15)",
    "spec_sha256": SPEC_SHA,
    "impl_sha256": IMPL_SHA,
    "data_sha256": DATA_SHA,
    "params": eng.SPEC,
    "panel": meta,
    "skips": skips,
    "chronology": {
        "first_entry": str(windows[0]["entry_date"].date()),
        "last_exit": str(windows[-1]["exit_date"].date()),
        "first_window_year": int(windows[0]["year"]),
        "last_window_year": int(windows[-1]["year"]),
    },
    "primary": {"endpoint": "mean annual net return",
                "n": res["n"], "mean": res["mean"], "ci95": res["ci95"],
                "bootstrap": {"B": eng.SPEC["boot_b"], "seed": eng.SPEC["seed"],
                              "method": "i.i.d. resample of annual events"}},
    "verdict": label,
    "control_descriptive": {
        "definition": "buy-and-hold identical span, same cost schedule once each",
        "entry_px": ctl["entry_px"], "exit_px": ctl["exit_px"], "net": ctl["net"],
        "strategy_cumulative_net": cum_strategy,
    },
}
with open(OUT + "/168_s2_evaluation_results.json", "w") as fh:
    json.dump(results, fh, indent=2, sort_keys=True)

print("mean annual net:", res["mean"])
print("ci95:", res["ci95"])
print("verdict:", label)
print("control net:", ctl["net"], "| strategy cumulative:", cum_strategy)
print("artifacts written; single execution complete")
