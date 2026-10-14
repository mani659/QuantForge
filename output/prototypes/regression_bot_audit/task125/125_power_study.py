"""TASK125 — XSM detectability and power study (direct simulation).

Estimates whether a 4-asset monthly-rebalanced cross-sectional momentum
design can distinguish economically meaningful effects from noise and costs.

This is a POWER STUDY, not a strategy backtest. It directly simulates the
XSM portfolio return distribution under known effect sizes and tests
whether the inference procedure can detect them.

Frozen preregistration: 125_preregistration.md (hash 153b9acc...).
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
    """Estimate the mean and std of the XSM spread from real data.

    The XSM spread is: mean(top-2 by trailing 12mo) - mean(bottom-2 by trailing 12mo).
    Under H0 (no momentum), this has mean 0. We estimate its std from the data.
    """
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


def simulate_xsm_returns(rng, spread_std, effect_bps, n_months):
    """Simulate XSM net monthly returns under a given effect size.

    Under H0: returns ~ N(0, spread_std)
    Under H1: returns ~ N(effect - cost, spread_std)
    """
    effect_decimal = effect_bps / 10000.0
    cost_decimal = COST_ROUND_TRIP_BPS / 10000.0
    mean = effect_decimal - cost_decimal
    return rng.normal(mean, spread_std, n_months)


def run_power_simulation(spread_std, seed):
    rng = np.random.default_rng(seed)
    results = {}
    for effect in EFFECT_BPS:
        pvals = []
        for _ in range(N_RUNS):
            rets = simulate_xsm_returns(rng, spread_std, effect, N_MONTHS)
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
    print("TASK125 power study (direct simulation)", flush=True)
    panel = load_monthly_returns()
    print("  panel shape:", panel.shape, flush=True)
    spread_mean, spread_std = estimate_xsm_spread_stats(panel)
    print("  XSM spread mean: %.6f (%.1f bps)" % (spread_mean, spread_mean * 10000), flush=True)
    print("  XSM spread std:  %.6f (%.1f bps)" % (spread_std, spread_std * 10000), flush=True)

    print("Running primary study (seed %d) ..." % SEED_PRIMARY, flush=True)
    primary = run_power_simulation(spread_std, SEED_PRIMARY)

    print("Running sensitivity study (seed %d) ..." % SEED_SENSITIVITY, flush=True)
    sensitivity = run_power_simulation(spread_std, SEED_SENSITIVITY)

    fp_rate = primary[0]["power"]
    power_50 = primary[50]["power"]
    power_100 = primary[100]["power"]

    if power_50 >= 0.80 and fp_rate <= 0.05:
        classification = "A_TESTABLE"
    elif power_100 < 0.80 or fp_rate > 0.05:
        classification = "B_LOW_POWER"
    else:
        classification = "C_INDETERMINATE"

    print("\n=== RESULTS ===", flush=True)
    print("False-positive rate (effect=0): %.3f +/- %.3f" % (
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
        "false_positive_rate": fp_rate,
        "power_at_50bps": power_50,
        "power_at_100bps": power_100,
        "classification": classification,
    }
    with open(os.path.join(ROOT, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nResults written to results.json", flush=True)


if __name__ == "__main__":
    main()
