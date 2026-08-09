"""
QuantForge Adaptive Strategy Engine v1.0.1 (Stable)
Part of Phase 1 Completion: The Decision Layer.

Evaluates Market DNA Profiles against decoupled config thresholds to determine
optimal strategy selection.
"""

import os
import json
import logging
from typing import Dict, Any, Tuple, List, Optional

# Setup Logger
logger = logging.getLogger("QuantForge.AdaptiveStrategyEngine")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RuleEngine:
    """
    Decoupled Rule Engine for the QuantForge Decision Layer.
    Loads thresholds dynamically from external JSON configs and evaluates
    market DNA profiles deterministically.
    """
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_default_config_path()
        self.rules = self._load_rules()

    def _find_default_config_path(self) -> str:
        """Locates the decoupled config file relative to this script."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Check strategy/config/adaptive_rules.json
        path1 = os.path.join(current_dir, "config", "adaptive_rules.json")
        # Check same directory (fallback)
        path2 = os.path.join(current_dir, "adaptive_rules.json")
        
        if os.path.exists(path1):
            return path1
        elif os.path.exists(path2):
            return path2
        
        # Return expected relative path if not found
        return "strategy/config/adaptive_rules.json"

    def _load_rules(self) -> Dict[str, Any]:
        """Reads adaptive_rules.json or falls back to standard thresholds."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    logger.info(f"Loaded active thresholds from: {self.config_path}")
                    return data
            else:
                logger.warning(
                    f"Config path '{self.config_path}' not found. "
                    "Loading safe default fallback parameters."
                )
                return self._get_fallback_rules()
        except Exception as e:
            logger.error(f"Error reading configuration file: {e}. Falling back.")
            return self._get_fallback_rules()

    def _get_fallback_rules(self) -> Dict[str, Any]:
        """Provides default values directly matching original v1.0.0 parameters."""
        return {
            "global_thresholds": {
                "trend_persistence_high": 1.90,
                "volatility_cv_stable": 0.95,
                "volatility_cv_unstable": 1.25,
                "expansion_duration_short": 3.0
            },
            "asset_specific": {
                "default": {
                    "low_atr": 0.001,
                    "high_atr": 0.01,
                    "pullback_min": 0.001
                }
            }
        }

    def evaluate(self, dna_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs deterministic rule evaluations on a loaded profile.
        Returns score matrix, evidence log, and configuration parameters applied.
        """
        # Extract instrument
        dataset_info = dna_profile.get("dataset_information", {})
        instrument = dataset_info.get("instrument", "default")
        
        # Select active parameters
        global_t = self.rules.get("global_thresholds", {})
        asset_specific = self.rules.get("asset_specific", {})
        asset_t = asset_specific.get(instrument, asset_specific.get("default", {}))
        
        # Extract Profile Metrics
        volatility_profile = dna_profile.get("volatility_profile", {})
        atr_profile = dna_profile.get("atr_profile", {})
        trend_persistence = dna_profile.get("trend_persistence", {})
        pullback_statistics = dna_profile.get("pullback_statistics", {})
        expansion_statistics = dna_profile.get("expansion_statistics", {})
        
        cv = volatility_profile.get("coefficient_of_variation", 1.0)
        mean_atr = atr_profile.get("mean", 0.0)
        avg_trend_len = trend_persistence.get("average_trend_length", 1.0)
        mean_pullback = pullback_statistics.get("mean", 0.0)
        
        # Dynamic handling of expansion statistics structures (nested vs single levels)
        expansion_size_dict = expansion_statistics.get("size", {})
        mean_expansion = (
            expansion_size_dict.get("mean", 0.0) 
            if isinstance(expansion_size_dict, dict) 
            else expansion_statistics.get("mean", 0.0)
        )
        
        expansion_dur_dict = expansion_statistics.get("duration_steps", {})
        mean_duration = (
            expansion_dur_dict.get("mean", 0.0)
            if isinstance(expansion_dur_dict, dict)
            else expansion_statistics.get("mean_steps", 0.0)
        )

        # Scopes & Evidence logs
        scores = {
            "Trend Following": 0,
            "Mean Reversion": 0,
            "Scalping": 0,
            "Volatility Breakout": 0
        }
        evidence = {k: [] for k in scores.keys()}
        
        # ----------------- RULE 1: TREND FOLLOWING -----------------
        tp_high = global_t.get("trend_persistence_high", 1.90)
        if avg_trend_len >= tp_high:
            scores["Trend Following"] += 40
            evidence["Trend Following"].append(f"Strong trend persistence: {avg_trend_len:.4f} >= {tp_high}")
        else:
            scores["Trend Following"] -= 10
            evidence["Trend Following"].append(f"Weak trend persistence: {avg_trend_len:.4f} < {tp_high}")
            
        cv_stable = global_t.get("volatility_cv_stable", 0.95)
        if cv < cv_stable:
            scores["Trend Following"] += 30
            evidence["Trend Following"].append(f"Stable volatility structure (CV): {cv:.4f} < {cv_stable}")
        else:
            scores["Trend Following"] -= 15
            evidence["Trend Following"].append(f"High volatility divergence (CV): {cv:.4f} >= {cv_stable}")

        # ----------------- RULE 2: MEAN REVERSION ------------------
        if avg_trend_len < tp_high:
            scores["Mean Reversion"] += 35
            evidence["Mean Reversion"].append(f"Favorable range persistence: {avg_trend_len:.4f} < {tp_high}")
            
        cv_unstable = global_t.get("volatility_cv_unstable", 1.25)
        if cv >= cv_unstable:
            scores["Mean Reversion"] += 25
            evidence["Mean Reversion"].append(f"Elevated relative variance (CV): {cv:.4f} >= {cv_unstable}")
            
        pullback_min = asset_t.get("pullback_min", 0.001)
        if mean_pullback > pullback_min:
            scores["Mean Reversion"] += 20
            evidence["Mean Reversion"].append(f"Healthy pullbacks detected: {mean_pullback:.4f} > {pullback_min}")
            
        if mean_pullback > (mean_expansion * 0.9):
            scores["Mean Reversion"] += 20
            evidence["Mean Reversion"].append(f"Pullback magnitude rivals expansion: {mean_pullback:.4f} vs {mean_expansion:.4f}")

        # ----------------- RULE 3: SCALPING ------------------------
        low_atr = asset_t.get("low_atr", 0.001)
        if mean_atr <= low_atr:
            scores["Scalping"] += 50
            evidence["Scalping"].append(f"Subdued absolute ATR context: {mean_atr:.6f} <= {low_atr:.6f}")
        else:
            scores["Scalping"] -= 20
            evidence["Scalping"].append(f"Range exceedance limits scalping potential: {mean_atr:.6f} > {low_atr:.6f}")
            
        dur_short = global_t.get("expansion_duration_short", 3.0)
        if mean_duration < dur_short:
            scores["Scalping"] += 30
            evidence["Scalping"].append(f"Ultra-short expansion durations: {mean_duration:.4f} < {dur_short}")

        # ----------------- RULE 4: VOLATILITY BREAKOUT -------------
        high_atr = asset_t.get("high_atr", 0.01)
        if mean_atr >= high_atr:
            scores["Volatility Breakout"] += 45
            evidence["Volatility Breakout"].append(f"Active market volatility (ATR): {mean_atr:.6f} >= {high_atr:.6f}")
        else:
            scores["Volatility Breakout"] -= 10
            evidence["Volatility Breakout"].append(f"Insufficient breakout context: {mean_atr:.6f} < {high_atr:.6f}")
            
        if cv >= cv_stable:
            scores["Volatility Breakout"] += 35
            evidence["Volatility Breakout"].append(f"Wide variances present: {cv:.4f} >= {cv_stable}")

        # Resolve strategy hierarchy
        recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_strat, primary_score = recommendations[0]
        secondary_strat, secondary_score = recommendations[1]
        
        status = "Active"
        if primary_score <= 0:
            primary_strat = "Neutral / Cash"
            status = "Inactive"
            
        return {
            "instrument": instrument,
            "status": status,
            "primary_strategy": primary_strat,
            "primary_score": primary_score,
            "secondary_strategy": secondary_strat,
            "secondary_score": secondary_score,
            "all_scores": scores,
            "evidence": evidence,
            "parameters_used": {
                "global": global_t,
                "asset": asset_t
            }
        }


class AdaptiveStrategyEngine:
    """
    Core Controller of the QuantForge Adaptive Strategy Engine (v1.0.1).
    Processes raw files/data and manages system inputs and reports.
    """
    def __init__(self, rules_config_path: Optional[str] = None):
        self.rule_engine = RuleEngine(config_path=rules_config_path)

    def analyze_profile(self, dna_profile_path_or_dict: Any) -> Dict[str, Any]:
        """Processes raw profile and maps to Strategy decision layer."""
        if isinstance(dna_profile_path_or_dict, str):
            with open(dna_profile_path_or_dict, "r") as f:
                profile = json.load(f)
        elif isinstance(dna_profile_path_or_dict, dict):
            profile = dna_profile_path_or_dict
        else:
            raise ValueError("Input profile must be a valid JSON path or dictionary.")
            
        evaluation = self.rule_engine.evaluate(profile)
        primary_strategy = evaluation["primary_strategy"]
        confidence = max(0.0, min(1.0, evaluation["primary_score"] / 100.0))
        strategy_class = primary_strategy.lower().replace(" ", "_")
        holding_style = "Scalping" if primary_strategy == "Scalping" else "Intraday"
        reason = evaluation["evidence"].get(primary_strategy, [])
        
        return {
            # Frozen Interface 4 contract.
            "strategy_class": strategy_class,
            "holding_style": holding_style,
            "risk_profile": "Low",
            "confidence": float(confidence),
            "reason": reason,
            # Existing decision detail is retained for current consumers and reports.
            "engine": "QuantForge Adaptive Strategy Engine",
            "version": "1.0.1",
            "decision_summary": {
                "instrument": evaluation["instrument"],
                "status": evaluation["status"],
                "primary_strategy": primary_strategy,
                "confidence_score": evaluation["primary_score"],
                "secondary_strategy": evaluation["secondary_strategy"],
                "secondary_confidence": evaluation["secondary_score"]
            },
            "detailed_scores": evaluation["all_scores"],
            "rationale": evaluation["evidence"],
            "parameters_applied": evaluation["parameters_used"]
        }

    def generate_text_report(self, report: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """Formats and optionally saves a publication-ready textual representation."""
        summary = report["decision_summary"]
        scores = report["detailed_scores"]
        rationale = report["rationale"]
        
        lines = [
            "=" * 65,
            f"QUANTFORGE DECISION LAYER REPORT - {summary['instrument'].upper()}",
            f"Engine Version: {report['version']} (Stable / Freeze Candidate)",
            "=" * 65,
            f"Deployment Status:  {summary['status']}",
            f"Primary Strategy:   {summary['primary_strategy']} (Confidence: {summary['confidence_score']} pts)",
            f"Secondary Strategy: {summary['secondary_strategy']} (Confidence: {summary['secondary_confidence']} pts)",
            "-" * 65,
            "DETERMINISTIC MATRIX PROFILE SCORING:"
        ]
        
        for strat, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  * {strat:<22} : {score:>3} points")
            
        lines.append("-" * 65)
        lines.append("RATIONALE EVIDENCE DEDUCTION LOGS:")
        
        for strat, evidence_list in rationale.items():
            lines.append(f"  {strat.upper()}:")
            if not evidence_list:
                lines.append("    - No triggering indicators logged.")
            for item in evidence_list:
                lines.append(f"    - {item}")
                
        lines.append("=" * 65)
        text_report = "\n".join(lines)
        
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(text_report)
            logger.info(f"Text report archived at: {output_path}")
            
        return text_report


# Self-contained testing validation logic
if __name__ == "__main__":
    # Standard testing layout across diverse asset formats
    test_profile = {
        "dataset_information": {"instrument": "XAUUSD"},
        "volatility_profile": {"coefficient_of_variation": 1.4878},
        "atr_profile": {"mean": 0.8972},
        "trend_persistence": {"average_trend_length": 1.9439},
        "pullback_statistics": {"mean": 1.4771},
        "expansion_statistics": {
            "size": {"mean": 1.4675},
            "duration_steps": {"mean": 2.9278}
        }
    }
    
    print("\n--- Validating QuantForge Adaptive Strategy Engine v1.0.1 ---\n")
    engine = AdaptiveStrategyEngine()
    result = engine.analyze_profile(test_profile)
    print(engine.generate_text_report(result))
