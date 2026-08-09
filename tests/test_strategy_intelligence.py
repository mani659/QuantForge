import tempfile
from pathlib import Path
import pandas as pd
import numpy as np
import json
from strategy.strategy_intelligence import StrategyIntelligence


def test_strategy_intelligence():
    print("Testing Strategy Intelligence Engine Pipeline...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. Setup Mock Feature Matrix File
        matrix_dir = temp_path / "research" / "matrix"
        matrix_dir.mkdir(parents=True, exist_ok=True)
        
        # We model 5 experiments with known correlation behaviors:
        # - "dna_feature_vector_volatility" goes up, "outcome_vector_profit_factor" goes UP (Positive Corr)
        # - "dna_feature_vector_volatility" goes up, "outcome_vector_drawdown" goes DOWN (Negative Corr)
        # - Contains a non-numeric string column which must be gracefully bypassed
        # - Contains NaN values which must be gracefully skipped
        mock_data = {
            "run_id": ["run_01", "run_02", "run_03", "run_04", "run_05"],
            "metadata_instrument": ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD", "USATECHIDXUSD"],  # Ignored string
            "dna_feature_vector_volatility": [10.0, 20.0, 15.0, 30.0, 25.0],
            "parameter_set_period": [5.0, 10.0, 7.0, 12.0, np.nan],  # NaN robust feature
            "outcome_vector_profit_factor": [1.1, 2.3, 1.6, 3.2, 2.7],  # Strong Positive Corr with volatility
            "outcome_vector_drawdown": [-4.0, -14.0, -8.0, -22.0, -11.0]  # Strong Negative Corr with volatility
        }
        
        df = pd.DataFrame(mock_data)
        df.to_csv(matrix_dir / "feature_matrix.csv", index=False)
        
        # 2. Instantiate and Run Strategy Intelligence Engine
        engine = StrategyIntelligence(project_root=temp_path)
        results = engine.analyze()
        
        # 3. Assertions and Verifications
        meta = results["meta"]
        assert meta["experiments_count"] == 5, "Failed to capture all experiments!"
        assert meta["features_count"] == 2, f"Should have found 2 numeric features, found {meta['features_count']}"
        assert meta["outcomes_count"] == 2, f"Should have found 2 numeric outcomes, found {meta['outcomes_count']}"
        assert meta["relationships_tested"] == 4, "Incorrect math for tested relationships!"
        
        # Verify file output integrity
        reports_dir = temp_path / "strategy" / "reports"
        assert (reports_dir / "strategy_intelligence.json").exists(), "JSON report missing!"
        assert (reports_dir / "strategy_intelligence.txt").exists(), "TXT report missing!"
        
        # Validate calculations (mathematical truth assertions)
        # Volatility should have high positive correlation against Profit Factor
        pf_corrs = results["correlations"]["outcome_vector_profit_factor"]["pearson"]
        assert pf_corrs["dna_feature_vector_volatility"] > 0.9, "Pearson mathematical accuracy check failed!"
        
        # Volatility should have high negative correlation against Drawdown
        dd_corrs = results["correlations"]["outcome_vector_drawdown"]["pearson"]
        assert dd_corrs["dna_feature_vector_volatility"] < -0.9, "Spearman negative coefficient mathematical accuracy check failed!"

        # Ensure NaNs didn't crash parameter_set_period calculations
        period_corrs = results["correlations"]["outcome_vector_profit_factor"]["pearson"]
        assert "parameter_set_period" in period_corrs, "NaN-heavy metrics were incorrectly completely stripped!"

        # Confirm rankings categorized values into logical positive/negative folders
        rankings_pf = results["rankings"]["outcome_vector_profit_factor"]["pearson"]
        assert len(rankings_pf["top_positive"]) > 0, "Positive rankings failed to populate!"
        assert rankings_pf["top_positive"][0]["feature"] == "dna_feature_vector_volatility"
        
        print("\nAll Strategy Intelligence Engine verification assertions passed cleanly!")


if __name__ == "__main__":
    test_strategy_intelligence()