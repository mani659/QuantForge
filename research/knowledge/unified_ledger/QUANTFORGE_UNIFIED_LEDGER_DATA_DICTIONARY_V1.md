# QUANTFORGE — UNIFIED LEDGER DATA DICTIONARY V1

## Purpose

This document defines every column, allowed values, provenance rules, and update protocol for the structured CSV ledger files in `research/knowledge/unified_ledger/`.

---

## Files

| File | Purpose |
|---|---|
| `QUANTFORGE_RESEARCH_CANDIDATE_LEDGER_V1.csv` | One row per candidate or formally identified research object |
| `QUANTFORGE_BEHAVIOURAL_KNOWLEDGE_LEDGER_V1.csv` | One row per distinct behavioural knowledge finding |
| `QUANTFORGE_RESEARCH_EVIDENCE_LEDGER_V1.csv` | Structured measurements with provenance |
| `QUANTFORGE_STATE_LIBRARY_LEDGER_V1.csv` | One row per State object/observation/artifact |
| `QUANTFORGE_EXPLORATORY_OBSERVATIONS_LEDGER_V1.csv` | One row per explicitly preserved exploratory finding |
| `QUANTFORGE_NEGATIVE_KNOWLEDGE_LEDGER_V1.csv` | One row per meaningful closed or contradicted conclusion |
| `QUANTFORGE_RESEARCH_RELATIONSHIP_LEDGER_V1.csv` | Conceptual relationships between findings (UNTESTED) |

---

## Master Candidate Ledger Columns

| Column | Type | Description |
|---|---|---|
| `candidate_id` | ID | Unique candidate identifier (e.g., CAND-015, CAND-077) |
| `candidate_name` | Text | Short descriptive name |
| `research_version` | ID | Research cycle (V5, V7, V8, ..., V29) or DISC line |
| `research_date` | Date | Approximate date (YYYY-MM-DD or YYYY-MM) |
| `artifact_class_initial` | Enum | Initial classification at G0 |
| `artifact_class_final` | Enum | Final classification |
| `mechanism_family` | Text | Mechanism category |
| `economic_mechanism` | Text | Why it should produce economics |
| `market` | Text | Primary instrument(s) |
| `timeframe` | Text | Data timeframe |
| `directionality` | Enum | BULLISH/BEARISH/DIRECTIONAL/SYMMETRIC/CONDITIONAL/UNKNOWN |
| `event_definition_summary` | Text | Concise event/condition definition |
| `state_definition_summary` | Text | State concept if applicable |
| `counterfactual_definition_summary` | Text | What the counterfactual compares against |
| `sample_n` | Integer | Treatment sample size |
| `frequency_per_year` | Float | Annualized frequency |
| `net_mean_bps` | Float | Net mean economics (bps or points) |
| `net_median_bps` | Float | Net median economics |
| `counterfactual_n` | Integer | Counterfactual sample size |
| `counterfactual_net_mean_bps` | Float | Counterfactual net mean |
| `counterfactual_net_median_bps` | Float | Counterfactual net median |
| `conditional_delta_mean_bps` | Float | Treatment minus counterfactual mean |
| `conditional_delta_median_bps` | Float | Treatment minus counterfactual median |
| `gate_result` | Text | Hard gate pass/fail summary |
| `counterfactual_validity` | Enum | VALID/INVALID/WEAK/STRONG/UNKNOWN |
| `economic_verdict` | Enum | ECONOMICALLY_NEGATIVE/INFORMATIONALLY_INTERESTING/ECONOMICALLY_PROMISING/QUALIFICATION_WORTHY/INSUFFICIENT/BLOCKED/UNKNOWN |
| `scientific_verdict` | Enum | SUPPORTED/CONTRADICTED/INCONCLUSIVE/EVIDENCE_LIMITED/NOT_TESTED/UNKNOWN |
| `final_classification` | Enum | CLOSED/STATE_OBSERVATION/STATE_ARTIFACT/STATE_REVIEW_ELIGIBLE/ACTIVE_PROTECTED/COMPONENT_CANDIDATE/FORWARD_OBSERVATION/INVALID/UNKNOWN |
| `final_status` | Text | Current governance status |
| `closure_reason` | Text | Why closed (if applicable) |
| `state_library_classification` | Enum | STATE_ARTIFACT/STATE_OBSERVATION/STATE_REVIEW_ELIGIBLE/NONE/UNKNOWN |
| `standalone_alpha_status` | Enum | POSITIVE/NEGATIVE/MIXED/NOT_TESTED/UNKNOWN |
| `relational_admissibility` | Enum | ADMISSIBLE/CONDITIONALLY_ADMISSIBLE/NOT_ADMISSIBLE/PROTECTED/UNKNOWN |
| `exploratory_only` | Boolean | Whether all findings are exploratory |
| `threshold_ratified` | Boolean | Whether any threshold is formally ratified |
| `protected_forward_status` | Enum | ACTIVE_PROTECTED/NOT_FORWARD/UNKNOWN |
| `source_artifact` | Text | Primary source repository path |
| `source_commit` | Text | Git commit if known |
| `provenance_confidence` | Enum | AUTHORITATIVE/HIGH/RECONCILED/PARTIAL/UNKNOWN |
| `notes` | Text | Additional context |

### Allowed Enums

**artifact_class_initial/final:** STANDALONE_ALPHA, RARE_EVENT_ALPHA, STATE_CONDITION, REGIME_SPECIALIST, COMPONENT_CANDIDATE, RESEARCH_FINDING, GOVERNANCE, INVALID, UNKNOWN

**directionality:** BULLISH, BEARISH, DIRECTIONAL, SYMMETRIC, CONDITIONAL, UNKNOWN

**counterfactual_validity:** VALID, INVALID, WEAK, STRONG, UNKNOWN

**economic_verdict:** ECONOMICALLY_NEGATIVE, INFORMATIONALLY_INTERESTING, ECONOMICALLY_PROMISING, QUALIFICATION_WORTHY, RARE_EVENT_QUALIFICATION_WORTHY, INSUFFICIENT, BLOCKED, INVALID, HYPOTHESIS_CONTRADICTED, REDUNDANT, UNKNOWN

**final_classification:** CLOSED, STATE_OBSERVATION, STATE_ARTIFACT, STATE_REVIEW_ELIGIBLE, ACTIVE_PROTECTED, COMPONENT_CANDIDATE, FORWARD_OBSERVATION, INVALID, UNKNOWN

**provenance_confidence:** AUTHORITATIVE, HIGH, RECONCILED, PARTIAL, AMBIGUOUS, UNKNOWN

---

## Behavioural Knowledge Ledger Columns

| Column | Type | Description |
|---|---|---|
| `knowledge_id` | ID | Unique knowledge identifier |
| `source_candidate_id` | ID | Originating candidate |
| `research_version` | ID | Research cycle |
| `knowledge_type` | Enum | Type of knowledge |
| `behaviour_description` | Text | What was observed |
| `market_mechanism` | Text | Proposed mechanism |
| `observable_inputs` | Text | Variables used |
| `temporal_structure` | Text | When the behaviour occurs |
| `direction_of_effect` | Enum | Direction |
| `evidence_strength` | Enum | Strength classification |
| `sample_context` | Text | N, frequency, market |
| `quantitative_summary` | Text | Key numbers |
| `absolute_economics` | Text | Standalone result |
| `conditional_information` | Text | Treatment vs CF |
| `counterfactual_result` | Text | CF outcome |
| `replication_status` | Enum | REPLICATED/NOT_REPLICATED/NOT_TESTED/UNKNOWN |
| `persistence_status` | Enum | DEMONSTRATED/NOT_DEMONSTRATED/UNKNOWN |
| `causality_status` | Enum | DEMONSTRATED/HYPOTHESIZED/NOT_DEMONSTRATED/UNKNOWN |
| `current_governance_status` | Enum | Governance classification |
| `relational_relevance` | Enum | ADMISSIBLE/CONDITIONALLY_ADMISSIBLE/NOT_ADMISSIBLE/UNKNOWN |
| `source_artifact` | Text | Primary source path |
| `provenance_confidence` | Enum | Confidence level |
| `limitations` | Text | Known limitations |

### knowledge_type enum:
POSITIVE_BEHAVIOURAL_FINDING, CONDITIONAL_INFORMATION, NEGATIVE_FINDING, CONTRADICTED_HYPOTHESIS, STATE_OBSERVATION, STATE_ARTIFACT, EXPLORATORY_OBSERVATION, MECHANISM_INSIGHT, REPLICATION_RESULT, ECONOMIC_LIMITATION

### evidence_strength enum:
DEMONSTRATED, SUPPORTED, PLAUSIBLE, EXPLORATORY, WEAK, INSUFFICIENT, CONTRADICTED, UNKNOWN

---

## Evidence Ledger Columns

| Column | Type | Description |
|---|---|---|
| `evidence_id` | ID | Unique evidence identifier |
| `candidate_id` | ID | Source candidate |
| `knowledge_id` | ID | Linked knowledge record |
| `measurement_name` | Text | What was measured |
| `measurement_type` | Enum | Type of measurement |
| `treatment_definition` | Text | Treatment group definition |
| `control_definition` | Text | Control/CF group definition |
| `sample_n` | Integer | Treatment N |
| `control_n` | Integer | Control/CF N |
| `value` | Float | Measured value |
| `unit` | Text | bps, points, percent, ratio |
| `comparison_value` | Float | Comparison group value |
| `comparison_unit` | Text | Unit of comparison |
| `delta` | Float | Treatment minus control |
| `statistical_status` | Text | Statistical assessment |
| `economic_status` | Text | Economic assessment |
| `gate_context` | Text | Which gate this relates to |
| `dataset_context` | Text | Data source description |
| `market` | Text | Instrument |
| `timeframe` | Text | Data timeframe |
| `source_artifact` | Text | Source path |
| `source_section` | Text | Section within source |
| `provenance_confidence` | Enum | Confidence |
| `notes` | Text | Additional context |

### measurement_type enum:
TREATMENT_NET_MEAN, TREATMENT_NET_MEDIAN, COUNTERFACTUAL_NET_MEAN, COUNTERFACTUAL_NET_MEDIAN, CONDITIONAL_DELTA_MEAN, CONDITIONAL_DELTA_MEDIAN, WIN_RATE, FREQUENCY, SAMPLE_SIZE, CONFIDENCE_INTERVAL, P_VALUE, PERMUTATION_RESULT, OTHER

---

## State Library Ledger Columns

| Column | Type | Description |
|---|---|---|
| `state_id` | ID | State identifier |
| `candidate_id` | ID | Source candidate |
| `state_name` | Text | Short name |
| `state_concept` | Text | What the State represents |
| `state_temporal_level` | Enum | REGIME, EVENT_PRE, EVENT_POST, SEQUENCE, TRANSITION, UNKNOWN |
| `observable_definition` | Text | What variables define it |
| `mechanism_hypothesis` | Text | Why it matters |
| `classification` | Enum | STATE_ARTIFACT, STATE_OBSERVATION, STATE_REVIEW_ELIGIBLE |
| `conditional_delta_mean_bps` | Float | Conditional separation |
| `conditional_delta_median_bps` | Float | Median delta |
| `absolute_economics` | Text | Standalone result |
| `counterfactual_quality` | Enum | VALID_STRONG, VALID_WEAK, INVALID, UNKNOWN |
| `sample_n` | Integer | Sample size |
| `threshold_status` | Enum | RATIFIED, NO_THRESHOLD_RATIFIED, EXPLORATORY, NOT_APPLICABLE |
| `persistence_status` | Enum | DEMONSTRATED, NOT_DEMONSTRATED, UNKNOWN |
| `causality_status` | Enum | DEMONSTRATED, HYPOTHESIZED, NOT_DEMONSTRATED, UNKNOWN |
| `independence_notes` | Text | Relationship to other States |
| `relational_admissibility` | Enum | ADMISSIBLE, CONDITIONALLY_ADMISSIBLE, NOT_ADMISSIBLE, PROTECTED |
| `known_related_states` | Text | Related State objects |
| `source_artifact` | Text | Primary source path |
| `governance_status` | Text | Current governance |

---

## Exploratory Observations Ledger Columns

| Column | Type | Description |
|---|---|---|
| `observation_id` | ID | Unique observation identifier |
| `source_candidate_id` | ID | Originating candidate |
| `observation_description` | Text | What was observed |
| `discovery_context` | Text | How it was discovered |
| `quantitative_result` | Text | Key numbers |
| `why_not_confirmed` | Text | Why it remains exploratory |
| `current_classification` | Text | Current governance status |
| `permitted_future_path` | Text | What governance allows |
| `relational_admissibility` | Enum | Admissibility to relational research |
| `requires_new_g0` | Boolean | Whether new G0 is required |
| `source_artifact` | Text | Primary source path |
| `provenance_confidence` | Enum | Confidence |

---

## Negative Knowledge Ledger Columns

| Column | Type | Description |
|---|---|---|
| `negative_knowledge_id` | ID | Unique identifier |
| `candidate_id` | ID | Source candidate |
| `mechanism_family` | Text | Mechanism category |
| `hypothesis_tested` | Text | What was proposed |
| `what_failed` | Text | What specifically failed |
| `failure_type` | Enum | Classification of failure |
| `key_evidence` | Text | Critical evidence |
| `counterfactual_result` | Text | CF outcome |
| `closure_reason` | Text | Formal closure reason |
| `what_is_now_known` | Text | Positive knowledge from failure |
| `what_remains_unknown` | Text | Open questions |
| `future_firewall` | Text | What is prohibited |
| `can_be_reopened` | Boolean | Whether reopening is permitted |
| `permitted_use` | Text | How this knowledge may be used |
| `prohibited_use` | Text | What is forbidden |
| `source_artifact` | Text | Primary source path |

### failure_type enum:
NEGATIVE_ABSOLUTE_ECONOMICS, WEAK_CONDITIONAL_INFORMATION, COUNTERFACTUAL_INVALID, HYPOTHESIS_CONTRADICTED, REDUNDANT_MECHANISM, NON_REPRODUCTION, CONTEMPORARY_FAILURE, DATA_LIMITATION, DESIGN_BLOCKED, INSUFFICIENT_EVIDENCE, G1_INVALID, OVERCONSTRAINED, OUTLIER_DEPENDENT, CF_SUPERIOR

---

## Research Relationship Ledger Columns

| Column | Type | Description |
|---|---|---|
| `relationship_id` | ID | Unique identifier |
| `object_a_type` | Enum | CANDIDATE, STATE, KNOWLEDGE, OBSERVATION |
| `object_a_id` | ID | Object A identifier |
| `object_b_type` | Enum | CANDIDATE, STATE, KNOWLEDGE, OBSERVATION |
| `object_b_id` | ID | Object B identifier |
| `relationship_type` | Enum | Type of relationship |
| `temporal_relationship` | Text | A before/after/simultaneous B |
| `mechanism_relationship` | Text | How mechanisms relate |
| `independence_status` | Enum | INDEPENDENT, POTENTIALLY_RELATED, REDUNDANT, UNKNOWN |
| `relationship_status` | Enum | CONCEPTUAL, UNTESTED, EMPIRICALLY_TESTED, CONTRADICTED |
| `evidence_basis` | Text | What supports this relationship |
| `expected_interaction` | Text | What might happen if combined |
| `incremental_question` | Text | Does B add beyond A? |
| `relational_admissibility` | Enum | Can this be tested? |
| `registered_hypothesis` | Boolean | Whether formally registered |
| `tested` | Boolean | Whether empirically tested |
| `source` | Text | Source of relationship information |
| `notes` | Text | Additional context |

### relationship_type enum:
TEMPORAL_PRECEDENCE, POTENTIAL_CAUSAL_CHAIN, MECHANISM_COMPLEMENTARITY, POTENTIAL_CONDITIONING, INDEPENDENT, REDUNDANT, EXTENSION, CONTRADICTORY, SAME_MECHANISM_FAMILY, UNKNOWN

---

## Update Protocol

After every future milestone (G0, G1, G2, closure, governance review, State review, relational study):

1. Check if a new candidate row is needed
2. Check if new behavioural knowledge emerged
3. Check if new evidence should be recorded
4. Check if State classification changed
5. Check if an exploratory observation emerged
6. Check if negative knowledge emerged
7. Check if a conceptual relationship became relevant
8. Check if governance status changed

**Do not modify existing historical evidence** unless a provenance-corrected update is required.

---

## Provenance Rules

Every substantive row must trace to repository evidence:

- `AUTHORITATIVE`: Directly from an authoritative governance artifact
- `HIGH`: From a research artifact with clear provenance
- `RECONCILED`: Reconstructed from multiple sources during this ledger creation
- `PARTIAL`: Incomplete or uncertain provenance
- `UNKNOWN`: Cannot be reliably sourced

---

## Format Requirements

- UTF-8 encoding
- Comma-delimited
- Double-quoted fields where commas or newlines appear
- One header row per file
- No merged cells
- Stable identifiers
- Empty string for unknown values (not "N/A" or "NULL")

---

*End of Data Dictionary V1.*
