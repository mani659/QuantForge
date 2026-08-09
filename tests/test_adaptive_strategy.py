import json
from pathlib import Path
from strategy.adaptive_strategy_engine import AdaptiveStrategyEngine


def run_adaptive_test():
    project_root = Path(__file__).resolve().parent
    
    # 1. Setup simulated paths locally
    dna_dir = project_root / "dna" / "profiles"
    dna_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Ensure your provided DNA content is written to EURUSD_dna_profile.json
    mock_dna_data = {
      "module": "QuantForge Market DNA Profiler",
      "version": "1.0.0",
      "dataset_information": {
        "instrument": "EURUSD",
        "total_candles": 462799,
        "first_candle": "2025-01-01 22:00:00",
        "last_candle": "2026-04-01 00:59:00",
        "coverage_days": 454
      },
      "trend_persistence": {
        "average_trend_length": 1.8694778771697886
      },
      "pullback_statistics": {
        "mean": 0.0003062373828406634
      },
      "expansion_statistics": {
        "size": {
          "mean": 0.00030156925919250243
        },
        "duration_steps": {
          "mean": 2.8794610670511895
        }
      },
      "volatility_profile": {
        "coefficient_of_variation": 0.9191932324746932
      },
      "atr_profile": {
        "mean": 0.000170796413578324
      }
    }
    
    with open(dna_dir / "EURUSD_dna_profile.json", "w", encoding="utf-8") as f:
        json.dump(mock_dna_data, f, indent=4)
        
    # 3. Instantiate and run recommendations
    engine = AdaptiveStrategyEngine(project_root)
    recommendation = engine.recommend("EURUSD")
    
    # Validation checks
    assert recommendation["instrument"] == "EURUSD"
    assert recommendation["recommended_strategy"] == "Mean Reversion"
    assert recommendation["holding_style"] == "Scalping"
    assert recommendation["risk_profile"] == "Low"
    assert recommendation["preferred_exit"] == "Hybrid Exit"
    assert recommendation["confidence"] == 83
    
    print("\n[SUCCESS]: Adaptive Strategy Engine generated exact outputs!")


if __name__ == "__main__":
    run_adaptive_test()