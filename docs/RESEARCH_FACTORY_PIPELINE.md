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
     Lifecycle                   │
     Governance                  │
          │                      ▼
          │             ┌─────────────────┐
          │             │ Dataset         │
          │             │ Foundation V1   │  ← NEXT
          │             └────────┬────────┘
          │                      │
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
                        Analytics / Validation
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
