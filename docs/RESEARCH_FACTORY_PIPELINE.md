# QuantForge Research Factory Pipeline

The following diagram illustrates the structural pipeline and flow of data from the frozen core and research domains down through the Dataset Foundation, culminating in the continuous Research Factory feedback loop.

```text
                 QUANTFORGE
                     │
          ┌──────────┴──────────┐
          │                     │
       FROZEN                 RESEARCH
          │                     │
     BOE / Deployment     Orchestration V1
     Temporal             Execution Context V1
     Lifecycle            Dataset Foundation V1
     Governance                  │
          │                      ▼
          │              Historical Data
          │                      │
          └──────────────► EnvironmentSnapshot
                                 │
                                 ▼
                         Research Orchestration
                                 │
                                 ▼
                          Execution Evidence
                                 │
                                 ▼
                     Scientific Hypothesis Evaluator V1
                                 │
                                 ▼
                    Validated Strategy Packaging   ← NEXT
                                 │
                                 ▼
                         Strategy Assembly
                                 │
                                 ▼
                         Paper / Live Trading
                                 │
                                 └────► Market Evidence
                                          │
                                          ▼
                                   Research Factory
```

## Scientific Hypothesis Evaluator V1

**Status: COMPLETE | FROZEN**

**Purpose:**
The Scientific Hypothesis Evaluator provides the deterministic scientific decision layer between TRAIN experimentation and subsequent Strategy Assembly. It evaluates behavioral market hypotheses to ensure they survive out-of-sample validation cleanly.

**TRAIN Champion Selection:**
Selection is performed using a deterministic selection policy. Only reports from the `TRAIN` partition are eligible. The policy enforces minimum trade samples (`min_train_trades`) and selects exactly one champion configuration based on maximum Profit Factor, breaking ties using minimum Drawdown, and finally the cryptographic experiment identity.

**VALIDATION Execution Boundary & Cryptographic Configuration Matching:**
> **IMPORTANT:** VALIDATION evidence must correspond to the selected TRAIN champion configuration.

The evaluator mathematically guarantees this by verifying that the VALIDATION report's cryptographic identity maps exclusively to the reconstructed TRAIN champion configuration, varying only by the partition flag (`dataset_partition`). Different strategy parameters, datasets, or strategy IDs will immediately result in rejection.

**OOS Degradation Analysis:**
Out-of-sample execution is graded against deterministic mathematical thresholds:
* **PF Degradation:** Maximum allowed percentage degradation of the Profit Factor (relative).
* **WR Degradation:** Maximum allowed absolute degradation of the Win Rate.
* **MDD Degradation:** Maximum allowed absolute increase in Drawdown percentage.
* **Minimum Validation Sample:** A strict minimum trade count is enforced on the validation sample.

**Infinity PF Handling:**
When the TRAIN Profit Factor is mathematically infinite (e.g. zero losses), standard relative degradation equations are safely bypassed. A strict absolute fallback threshold is enforced instead.

**Invalid Metric Handling:**
Any metrics resulting in `NaN` or negative Profit Factors are structurally trapped and produce explicit rejection reasons (e.g., "VALIDATION PF is NaN").

**Scientific Verdict & Provenance:**
The final output is an immutable `ScientificVerdict`. It stores exact cryptographic provenance tying the validation identity back to the original execution. All underlying dicts and lists are deep-frozen.

**Leakage Protection:**
The evaluation layer completely partitions TRAIN selection from VALIDATION validation. The TRAIN selection returns only a blind `ExperimentConfiguration` with no execution artifacts, guaranteeing the Orchestration engine maintains boundary blindness during VALIDATION execution.

**Scientific Limitation (V1):**
> Repeatedly evaluating the same VALIDATION partition can itself create validation overfitting. Once VALIDATION has influenced parameter selection, it is no longer scientifically blind.

**Test Evidence:**
The V1 implementation passed 32 strict behavioral tests, verifying cryptographic identity matching, failed validation execution trapping, duplicate experiment rejection, mathematical degradation correctness, and immutability. All test orderings execute perfectly with 100% isolation.

**Frozen Boundaries:**
The evaluator sits as a pure mathematical layer atop the outputs. No modifications were made to `boe/`, `research/lifecycle/`, `research/engine/`, or `research/dataset/`.
