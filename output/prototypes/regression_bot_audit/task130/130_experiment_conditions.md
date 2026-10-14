# TASK130 — Experiment Conditions (conditional requirements, NOT authorization)

**Status:** pre-stated conditions that ANY future permitted VS-TSMOM-01
experiment must satisfy. Listing them authorizes nothing; each requires
its own future act.

1. **Permitted benchmark:** must not execute the prohibited closed
   DISC-022 rule. Acceptable: buy-and-hold NASDAQ100 (tests momentum vs
   passive without running the closed line) or another benchmark with no
   closed-mechanism content. Fixed-TSMOM leg requires separate explicit
   permission or stays out.
2. **Frozen estimator and rules:** volatility estimator definition
   (e.g., trailing window, annualization), target-vol value with recorded
   justification, leverage/exposure limits ([-1,+1] or stated bounds),
   monthly rebalance convention, tie handling — all frozen pre-outcome.
3. **Frozen cost model:** NASDAQ100-vehicle-specific spread/commission/
   slippage schedule (Batch-1 family is a starting point only, not a
   transplant).
4. **Estimand and inference:** paired-differential primary outcome with
   dependence-robust inference (Newey-West or block bootstrap,
   predeclared); no bare t-test.
5. **Preregistered bars:** minimum economically meaningful effect,
   pass/fail/inconclusive criteria, and falsification conditions fixed
   before ANY period's outcomes are observed (development-informed
   thresholds prohibited).
6. **Chronology:** development/validation/final boundaries with the final
   evaluation blinded by freeze (procedural protection stated, since no
   holdout exists).
7. **Separate evaluation authorization** under §3B (budgets, data scope)
   remains required even if admission is ever granted. Admission ≠
   execution, now and always.
