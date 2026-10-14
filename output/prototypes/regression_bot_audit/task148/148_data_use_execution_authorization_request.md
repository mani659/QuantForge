# TASK148 — Data-Use and Execution Authorization Request (UNAPPROVED)

**Status:** request prepared for the owner. Grants nothing. No verdict,
signature, or date prefilled; none inferred from technical delegation.

## Precise operations the owner would authorize (single bounded run)

1. Read the 11 `_t37_m1_{SYM}.npz` files (OHLC+spread + timestamps only);
   compute per-file SHA pre-use and record it; verify row counts against
   the preregistration §2 table; verify timestamp parse (epoch-ns → UTC).
2. Build daily features per the frozen preregistration §3 (training-fit
   scaling only); run KMeans k∈{2,3} (n_init=10, seeds 0–9) + tertile
   baseline + shuffled null; compute stability metrics per §6.
3. Write ONE bounded report (stability verdict per §8 decision rules,
   prevalence/persistence tables, integrity log, conformance attestation).

## Dataset and study version

`_t37` M1 panel as inventoried in the preregistration §2; study version =
that preregistration file (fingerprint recorded at filing verification).

## Allowed measurement (only this)

Descriptive regime-stability characterization per §§6–8. No trading
signals, no returns-based claims, no candidate, no profitability.

## Prohibited operations

Model fitting beyond the frozen k/seed set; feature changes; any use of
adxcache files, tick data, M1 price-content beyond feature construction,
holdouts (none exist), recorders, runtime/MT5 contact, paper/live
execution, deployment, governance edits, follow-on tasks.

## Termination conditions

Completion → report, no continuation. Budget exhaustion (one run),
hash/count/parse mismatch, missing-data stop, integrity failure →
stop with a record, no retry without a new explicit act.

## Distinction preserved

Approval of THIS request (if granted) authorizes the single descriptive
run only. Any trading-use design, sizing rule, or evaluation needs a
separate future act with its own preregistration.
