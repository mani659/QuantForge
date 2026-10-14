"""TASK126 — Corrected XSM calibration and power study.

Applies the smallest demonstrated correction from the method audit:
generate net returns with mean = effect (not effect - cost).

Frozen correction preregistration: 126_calibration_preregistration.md.
"""
import hashlib
import json
import math
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "prototypes",
                                     "lane_b_batch1", "data"))
TICKERS = ["SPY", "VEU", "AGG", "BIL"]
N_MONTHS = 216
N_RUNS = 2000
SEED_PRIMARY = 20261013
SEED_SENSITIVITY = 20261014
EFFECT_BPS = [0, 25, 50, 75, 100]
ALPHA = 0.05
COST_ROUND_TRIP_BPS = 30.0
TRAIN_MONTHS = 12


def load_monthly_returns():
    rets = {}
    for t in TICKERS:
        p = os.path.join(DATA, t + ".csv")
        df = pd.read_csv(p, parse_dates=["date"]).sort_values("date")
        df = df.set_index("date")
        monthly = df["close"].astype(float).resample("ME").last().pct_change().dropna()
        rets[t] = monthly
    return pd.DataFrame(rets).dropna()


def estimate_xsm_spread_stats(panel):
    spreads = []
    for t in range(TRAIN_MONTHS, len(panel)):
        formation = panel.iloc[t - TRAIN_MONTHS:t]
        trailing = (1 + formation).prod() - 1
        ranking = trailing.sort_values(ascending=False)
        top2 = ranking.iloc[:2].index
        bottom2 = ranking.iloc[2:].index
        spread = panel.iloc[t][top2].mean() - panel.iloc[t][bottom2].mean()
        spreads.append(spread)
    return float(np.mean(spreads)), float(np.std(spreads, ddof=1))


def simulate_xsm_returns_corrected(rng, spread_std, effect_bps, n_months):
    """CORRECTED: generate net returns with mean = effect (not effect - cost).

    The cost is already netted in the return definition; the simulation mean
    is the net return mean directly.
    """
    effect_decimal = effect_bps / 10000.0
    return rng.normal(effect_decimal, spread_std, n_months)


def run_power_simulation(spread_std, seed):
    rng = np.random.default_rng(seed)
    results = {}
    for effect in EFFECT_BPS:
        pvals = []
        for _ in range(N_RUNS):
            rets = simulate_xsm_returns_corrected(rng, spread_std, effect, N_MONTHS)
            n = len(rets)
            mean = np.mean(rets)
            std = np.std(rets, ddof=1)
            if std == 0:
                pval = 1.0
            else:
                t_stat = mean / (std / np.sqrt(n))
                pval = 2 * (1 - 0.5 * (1 + math.erf(abs(t_stat) / np.sqrt(2))))
            pvals.append(pval)
        pvals = np.array(pvals)
        power = float(np.mean(pvals < ALPHA))
        results[effect] = {
            "power": power,
            "power_std": float(np.sqrt(power * (1 - power) / N_RUNS)),
        }
    return results


def main():
    print("TASK126 corrected calibration study", flush=True)
    panel = load_monthly_returns()
    print("  panel shape:", panel.shape, flush=True)
    spread_mean, spread_std = estimate_xsm_spread_stats(panel)
    print("  XSM spread mean: %.1f bps" % (spread_mean * 10000), flush=True)
    print("  XSM spread std:  %.1f bps" % (spread_std * 10000), flush=True)

    print("Running primary study (seed %d) ..." % SEED_PRIMARY, flush=True)
    primary = run_power_simulation(spread_std, SEED_PRIMARY)

    print("Running sensitivity study (seed %d) ..." % SEED_SENSITIVITY, flush=True)
    sensitivity = run_power_simulation(spread_std, SEED_SENSITIVITY)

    fp_rate = primary[0]["power"]
    power_50 = primary[50]["power"]

    # Decision rules (frozen in 126_calibration_preregistration.md)
    if fp_rate > 0.10:
        classification = "C_UNRESOLVED"
    elif power_50 < 0.80:
        classification = "A_CALIBRATED_LOW_POWER"
    else:
        classification = "B_CALIBRATED_TESTABLE"

    print("\n=== CORRECTED RESULTS ===", flush=True)
    print("Type-I error (effect=0): %.3f +/- %.3f" % (
        fp_rate, primary[0]["power_std"]), flush=True)
    for effect in EFFECT_BPS:
        p = primary[effect]["power"]
        ps = primary[effect]["power_std"]
        print("Effect %3d bps/mo: power = %.3f +/- %.3f" % (effect, p, ps), flush=True)
    print("Classification: %s" % classification, flush=True)

    out = {
        "spread_mean_bps": spread_mean * 10000,
        "spread_std_bps": spread_std * 10000,
        "seed_primary": SEED_PRIMARY,
        "seed_sensitivity": SEED_SENSITIVITY,
        "n_runs": N_RUNS,
        "n_months": N_MONTHS,
        "alpha": ALPHA,
        "effect_bps": EFFECT_BPS,
        "cost_round_trip_bps": COST_ROUND_TRIP_BPS,
        "primary": {str(k): v for k, v in primary.items()},
        "sensitivity": {str(k): v for k, v in sensitivity.items()},
        "type_I_error": fp_rate,
        "power_at_50bps": power_50,
        "classification": classification,
    }
    with open(os.path.join(ROOT, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nResults written to results.json", flush=True)


if __name__ == "__main__":
    main()
