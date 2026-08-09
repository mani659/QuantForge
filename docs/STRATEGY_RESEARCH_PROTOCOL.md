# Strategy Research Protocol v1.0

## 1. Objective

The purpose of the Strategy Research Protocol is to provide a single standard scientific workflow for developing every future trading strategy inside QuantForge. 

QuantForge standardises the process of discovering and validating market behaviour. The protocol itself does not contain strategy logic. QuantForge should never reinvent the research process. The protocol is designed to maximise the reuse of existing QuantForge components before introducing new infrastructure.

---

## 2. Research Lifecycle

The research lifecycle is a continuous and **iterative** process, rather than a linear one:

Idea
↓
Hypothesis
↓
Experiment Design
↓
Scientific Validation
↓
Strategy Assembly
↓
Paper Trading
↓
Demo Trading
↓
Live Trading
↓
Performance Review
↓
Scientific Findings
↓
New Hypothesis

---

## 3. Mandatory Research Questions

Every new strategy must answer:

- What market behaviour is being investigated?
- Why should it exist?
- Which markets will be tested?
- What evidence is expected?
- What would invalidate the hypothesis?
- What constitutes success?

---

## 4. Component Reuse Checklist

Before creating any new component, researchers must ask:

- Can an existing Observer be reused?
- Can an existing Behaviour Profile be reused?
- Can an existing Interpretation Model be reused?
- Can an existing Decision Policy be reused?
- Can an existing Risk Policy be reused?

Only if every answer is NO may new infrastructure be introduced.

---

## 5. Cross-Market Validation

Every strategy should be evaluated across applicable markets.

**Examples:**
- Gold
- Silver
- BTC
- EURUSD
- NASDAQ

**Record:**
- Supported Markets
- Rejected Markets
- Unknown Markets

---

## 6. Live Validation

Define live trading as another scientific experiment.

Live performance must never trigger optimisation by default.

Instead ask:
*"What changed?"*

Record new observations. Generate new hypotheses.

---

## 7. Scientific Findings

Every completed strategy should produce reusable findings.

**Examples:**
- Works during trend.
- Fails during expansion.
- Fails under high volatility.
- Works only on commodities.

These findings become inputs to future hypotheses.

---

## 8. Architectural Principles

- Research evolves.
- QuantForge Core remains frozen.
- Strategies evolve.
- Infrastructure changes only when genuinely required.
