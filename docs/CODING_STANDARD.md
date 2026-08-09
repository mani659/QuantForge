# QuantForge Coding Standard
Version: 1.0
Status: Active Development
Last Updated: 2026-07-15

===========================================================
PURPOSE
===========================================================

This document defines the coding standards used throughout
QuantForge.

Every module must follow these standards to ensure
consistency, maintainability, reproducibility, and long-term
scalability.

These rules apply to every future Python module.

===========================================================
CORE DEVELOPMENT PRINCIPLES
===========================================================

Rule 1

Correctness before performance.

Always produce correct results before optimizing speed.

-----------------------------------------------------------

Rule 2

Readable code is preferred over clever code.

Future maintainability is more important than writing fewer
lines.

-----------------------------------------------------------

Rule 3

Deterministic outputs only.

The same input must always produce the same output.

-----------------------------------------------------------

Rule 4

No hidden magic.

Every calculation should be explainable.

-----------------------------------------------------------

Rule 5

Configuration belongs outside source code.

Business rules must never be hardcoded.

===========================================================
PROJECT STRUCTURE
===========================================================

Every module should follow

QuantForge/

data/

validation/

dna/

research/

strategy/

execution/

reports/

tests/

docs/

config/

Never create arbitrary folders.

Keep the project structure consistent.

===========================================================
MODULE DESIGN
===========================================================

Every module must have one responsibility.

Examples

Tick Validator

Validate raw tick data.

---------------------------------------

DNA Profiler

Generate market fingerprints.

---------------------------------------

Risk Engine

Calculate position size.

Avoid combining unrelated functionality into one module.

===========================================================
OBJECT ORIENTED DESIGN
===========================================================

Preferred

One primary class per module.

Example

TickValidator

DNAProfiler

ExperimentRecorder

RiskEngine

ExecutionEngine

Public methods should remain small and descriptive.

===========================================================
FILE NAMING
===========================================================

Use lowercase with underscores.

Examples

tick_validator.py

market_dna.py

feature_matrix.py

adaptive_strategy_engine.py

Avoid

Final.py

New.py

temp.py

test2.py

===========================================================
CLASS NAMING
===========================================================

PascalCase

Examples

TickValidator

DNAProfiler

SignalGenerator

RiskEngine

===========================================================
FUNCTION NAMING
===========================================================

snake_case

Examples

validate()

generate_profile()

save_report()

load_configuration()

calculate_atr()

===========================================================
VARIABLE NAMING
===========================================================

Use descriptive names.

Preferred

trend_length

average_spread

confidence_score

position_size

Avoid

x

tmp

data2

value123

===========================================================
CONFIGURATION
===========================================================

Never hardcode strategy parameters.

Store configuration inside JSON files.

Examples

adaptive_rules.json

risk_rules.json

signal_rules.json

execution_rules.json

Every module should load configuration during startup.

===========================================================
PATH HANDLING
===========================================================

Always use pathlib.

Never hardcode Windows paths.

Preferred

project_root

↓

data

↓

tick

↓

EURUSD.csv

Project root should always be detected automatically.

===========================================================
ERROR HANDLING
===========================================================

Catch expected exceptions.

Provide meaningful error messages.

Never silently ignore failures.

Example

Missing configuration

Missing data

Invalid JSON

Corrupted CSV

Failures should explain

What happened

Why it happened

How to resolve it

===========================================================
LOGGING
===========================================================

Every major module should display

Module Name

Input

Output

Summary

Status

Example

================================================

QUANTFORGE DNA PROFILER

================================================

Input

EURUSD_M1.csv

Output

EURUSD_dna_profile.json

Status

PASS

===========================================================

REPORTS
===========================================================

Every completed module should generate

TXT Report

JSON Report

CSV (when appropriate)

Console Summary

Reports must be reproducible.

===========================================================
TESTING
===========================================================

Every production module requires

Unit Test

Verification Test

Sample Dataset

Expected Output

Regression Safety

A module is considered stable only after tests pass.

===========================================================
VERSIONING
===========================================================

Version format

Major.Minor.Patch

Example

1.0.0

Major

Architectural change

Minor

New functionality

Patch

Bug fixes

Stable modules are frozen.

===========================================================
DEPENDENCIES
===========================================================

Preferred libraries

pathlib

json

csv

statistics

numpy

pandas

pyarrow

Avoid unnecessary external dependencies.

Keep installation simple.

===========================================================
DOCUMENTATION
===========================================================

Every module should begin with

Purpose

Inputs

Outputs

Dependencies

Public API

Example

Tick Validator

Purpose

Validate broker tick data.

Input

Tick CSV

Output

Validation Report

===========================================================
PERFORMANCE
===========================================================

Optimize only after correctness.

Prefer streaming large files.

Avoid loading multi-GB datasets into memory when unnecessary.

Use vectorized pandas operations where practical.

Profile performance before optimizing.

===========================================================
CROSS-MARKET COMPATIBILITY
===========================================================

Never optimize code for a single instrument.

Every module should support

Forex

Metals

Crypto

Indices

Future instruments

No instrument-specific assumptions inside business logic.

===========================================================
RESEARCH STANDARDS
===========================================================

Research must be

Repeatable

Deterministic

Statistically justified

Documented

Validated

No conclusions should rely on visual inspection alone.

===========================================================
AI POLICY
===========================================================

Current QuantForge versions are deterministic.

Machine Learning is postponed until

Python EA is complete

Cross-market validation succeeds

Deterministic engine is stable

ML must improve statistical performance before adoption.

===========================================================
MODULE COMPLETION CHECKLIST
===========================================================

Before freezing a module verify

✔ Code Compiles

✔ Tests Pass

✔ Validation Complete

✔ Reports Generated

✔ JSON Output Valid

✔ Configuration Externalized

✔ Documentation Updated

✔ Changelog Updated

✔ Context Updated

Only then may a module be marked

Stable

===========================================================
DEVELOPMENT PHILOSOPHY
===========================================================

Always ask

Does this module move QuantForge closer to the Adaptive EA?

If the answer is

No

Postpone it.

Avoid over-engineering.

Prefer incremental progress.

Finish modules completely before starting new ones.

===========================================================
QUANTFORGE MOTTO
===========================================================

Validate.

Measure.

Understand.

Decide.

Execute.

Improve.

===========================================================
END OF CODING STANDARD
===========================================================