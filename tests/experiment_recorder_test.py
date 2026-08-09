import json
import tempfile
from pathlib import Path
import pandas as pd
from research.experiment_recorder import ExperimentRecorder


def test_recorder_pipeline():
    print("Running full suite verification...")
    
    # Safe temp workspace context
    with tempfile.TemporaryDirectory() as temp_dir:
        recorder = ExperimentRecorder(project_root=temp_dir)
        
        # Setup metadata with non-whitelisted custom keys to test preservation
        mock_metadata = {
            "instrument": "EURUSD",
            "timeframe": "M1",
            "strategy_name": "Adaptive EMA Recoil",
            "strategy_version": "1.2.0",
            "date_range_start": "2025-01-01 22:00:00",
            "date_range_end": "2026-04-01 00:59:00",
            "QuantForge_version": "1.0.0",
            "broker": "IC Markets",
            "commission_model": "raw_spread",
            "timezone": "GMT+2"
        }
        
        mock_parameters = {
            "lookback_period": 21,
            "recoil_threshold_atr": 1.5,
            "exit_time_minutes": 120
        }
        
        mock_traits = {
            "entry_type": "recoil",
            "exit_type": "time",
            "risk_model": "fixed"
        }
        
        # Try to load the real EURUSD DNA file if available, otherwise fallback
        try:
            with open("EURUSD_dna_profile.json", "r", encoding="utf-8") as f:
                dna_profile = json.load(f)
        except FileNotFoundError:
            dna_profile = {
                "dataset_information": {
                    "instrument": "EURUSD"
                },
                "bull_bear_statistics": {
                    "bull_percent": 46.61,
                    "bear_percent": 47.02
                },
                "nested": {
                    "deep_metric": 123.45,
                    "is_active": True  # boolean should be filtered out
                }
            }

        mock_outcomes = {
            "trades": 329,
            "profit_factor": 4.52
        }

        mock_robustness = {
            "walk_forward_score": 0.82,
            "monte_carlo_ruin_probability": 0.0,
            "spread_stress_factor": 0.76,
            "latency_stress_factor": 0.91,
            "sequence_stability": 1.98
        }

        mock_trades_df = pd.DataFrame({
            "trade_id": [1, 2],
            "pnl": [50.0, -20.0]
        })

        mock_equity_df = pd.DataFrame({
            "tick_id": [1, 2],
            "balance": [10000.0, 10050.0]
        })

        # Run recorder
        run_id = recorder.save_experiment(
            metadata=mock_metadata,
            parameter_set=mock_parameters,
            strategy_traits=mock_traits,
            dna_profile=dna_profile,
            outcome_vector=mock_outcomes,
            robustness=mock_robustness,
            trades_df=mock_trades_df,
            equity_df=mock_equity_df
        )
        
        # Read back run.json to verify dynamic DNA extraction and metadata preservation
        run_json_path = Path(temp_dir) / "research" / "experiments" / run_id / "run.json"
        with open(run_json_path, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
            
        # Assertions / Checks
        assert saved_data["metadata"]["broker"] == "IC Markets", "Custom metadata key was filtered out!"
        assert "candle_structure_body_size_mean" in saved_data["dna_feature_vector"] or "bull_bear_statistics_bull_percent" in saved_data["dna_feature_vector"], "Dynamic DNA extraction failed!"
        
        # Verify manifest is present
        manifest_path = Path(temp_dir) / "research" / "experiments" / run_id / "manifest.json"
        assert manifest_path.exists(), "manifest.json was not created!"
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        
        assert manifest_data["run_id"] == run_id
        assert "manifest.json" in manifest_data["files"]
        assert "trades.csv" in manifest_data["files"]
        assert "equity.csv" in manifest_data["files"]

        print("\nAll pipeline assertions passed cleanly!")


if __name__ == "__main__":
    test_recorder_pipeline()