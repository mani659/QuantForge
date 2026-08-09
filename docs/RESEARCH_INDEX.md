# QuantForge Research Index
Version: 1.0
Status: Active Development
Last Updated: 2026-07-15

===========================================================
PURPOSE
===========================================================

This document is the master index of every validated
research activity performed within QuantForge.

It is not a journal.

It is not a changelog.

It is a searchable catalogue of completed research,
modules, experiments, validators and datasets.

===========================================================
RESEARCH STATUS
===========================================================

Research Infrastructure

COMPLETE

Trading Intelligence

----------------------------------------------------------

PHASE 8 RESEARCH INDUSTRIALIZATION MATURITY

Research
COMPLETE

Validation
COMPLETE

Strategy Assembly
COMPLETE

Deployment Assembly
COMPLETE

Deployment Runtime
COMPLETE

Research Industrialization
COMPLETE

The frozen scientific lifecycle (Research → Validation → Validated Behaviour →
Strategy Manifest → Deployment Runtime → Execution → Deployment Evidence →
Human Research Review) is complete through Phase 8. Phase 8 industrializes the
Research Industrialization closes the research lifecycle loop operationally
(planning-era phrase: "Research Feedback loop") without altering any frozen
scientific domain. The automated pipeline terminates at the read-only
OutcomeReader
service; Human Research Review is outside QuantForge software.

Signal Generator

Status

Stable

Version

1.0.0

Purpose

Transform Adaptive Strategy recommendations into
deterministic trade signals.

Outputs

BUY

SELL

NO TRADE

Confidence

Signal Strength

Reasoning

ACTIVE

Execution Layer

NOT STARTED

Production EA

NOT STARTED

===========================================================
VALIDATED DATASETS
===========================================================

Status

Validated

Datasets

✔ EURUSD

✔ XAUUSD

✔ XAGUSD

✔ BTC

✔ USATECHIDX

Validation Pipeline

Tick Validator

↓

Tick → M1 Converter

↓

M1 Validator

===========================================================
DATA VALIDATION MODULES
===========================================================

Tick Validator

Status

Stable

Purpose

Validate raw broker tick data.

Outputs

TXT

CSV

JSON

Validation

PASS

-----------------------------------------------------------

Tick → M1 Converter

Status

Stable

Purpose

Convert validated ticks into deterministic M1 candles.

Outputs

M1 CSV

-----------------------------------------------------------

M1 Validator

Status

Stable

Purpose

Validate generated OHLC candles.

Outputs

TXT

CSV

JSON

===========================================================
MARKET DNA
===========================================================

Market DNA Profiler

Status

Stable

Purpose

Generate statistical market fingerprints.

Outputs

DNA JSON

DNA TXT

-----------------------------------------------------------

DNA Comparator

Status

Stable

Purpose

Compare behavioural characteristics across markets.

Outputs

Comparison Report

===========================================================
RESEARCH DATABASE
===========================================================

Experiment Recorder

Status

Stable

Purpose

Store every experiment using a standardized schema.

Outputs

Run Folder

run.json

metadata.json

dna_snapshot.json

robustness.json

trades.csv

equity.csv

manifest.json

-----------------------------------------------------------

Feature Matrix Builder

Status

Stable

Purpose

Aggregate experiment data for statistical analysis.

Outputs

feature_matrix.csv

feature_matrix.parquet

===========================================================
TRADING INTELLIGENCE
===========================================================

Strategy Intelligence Engine

Status

Stable

Purpose

Discover statistical relationships between

Market DNA

↓

Strategy Performance

Outputs

strategy_intelligence.json

strategy_intelligence.txt

-----------------------------------------------------------

Adaptive Strategy Engine

Status

Stable

Version

1.0.1

Purpose

Recommend

Strategy Class

Holding Style

Risk Profile

Exit Style

Confidence

Configuration

adaptive_rules.json

Outputs

adaptive_strategy.json

adaptive_strategy.txt

===========================================================
RESEARCH FINDINGS
===========================================================

Validated

✔ Behavioural Mean Reversion

✔ Expansion Behaviour

✔ Pullback Behaviour

✔ Virtual Signals

✔ Robust Exit Logic

✔ Walk Forward Stability

✔ Monte Carlo Stability

✔ Spread Stress

✔ Latency Stress

✔ Monthly Stability

✔ Cross-Market Universality

✔ Data Integrity Framework

✔ Market DNA Framework

===========================================================
CROSS-MARKET VALIDATION
===========================================================

Markets

EURUSD

XAUUSD

XAGUSD

BTC

USATECHIDX

Result

Behavioural transfer confirmed.

Research continues.

===========================================================
ACTIVE DEVELOPMENT
===========================================================

Current Module

Signal Generator

Purpose

Generate deterministic trade entries.

Status

Planned

===========================================================
PLANNED MODULES
===========================================================

Signal Generator

Risk Engine

Execution Engine

Python Trading Engine

Portfolio Validation

MT5 Expert Advisor

===========================================================
RESEARCH FILES
===========================================================

Primary Documents

CONTEXT.md

CHANGELOG.md

ROADMAP.md

ARCHITECTURE.md

CODING_STANDARD.md

RESEARCH_INDEX.md

Research Journal v2.x

===========================================================
RESEARCH PIPELINE
===========================================================

Tick Data

↓

Validation

↓

M1

↓

Validation

↓

DNA

↓

Experiment

↓

Feature Matrix

↓

Strategy Intelligence

↓

Adaptive Strategy

↓

Signal Generator

↓

Risk

↓

Execution

↓

EA

===========================================================
MODULE MATURITY
===========================================================

Tick Validator

★★★★★

-----------------------------------------------------------

Tick → M1 Converter

★★★★★

-----------------------------------------------------------

M1 Validator

★★★★★

-----------------------------------------------------------

DNA Profiler

★★★★★

-----------------------------------------------------------

DNA Comparator

★★★★★

-----------------------------------------------------------

Experiment Recorder

★★★★★

-----------------------------------------------------------

Feature Matrix Builder

★★★★★

-----------------------------------------------------------

Strategy Intelligence

★★★★★

-----------------------------------------------------------

Adaptive Strategy Engine

★★★★★

-----------------------------------------------------------

Signal Generator
★★★★★



===========================================================
NEXT MILESTONE
===========================================================

Execution Layer

MT5 Connection Manager

ConnectionStatus

MT5 Broker Adapter

TradeResult

-----------------------------------------------------------

Build

Risk Engine
☆☆☆☆☆

This module marks the transition from

Research Intelligence

↓

Executable Trading Logic

===========================================================
END OF RESEARCH INDEX
===========================================================
