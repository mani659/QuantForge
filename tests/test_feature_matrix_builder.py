import json
import tempfile
from pathlib import Path
import pandas as pd
from research.feature_matrix_builder import FeatureMatrixBuilder


def test_feature_matrix_builder():
    print("Testing Feature Matrix Builder Pipeline...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. Setup Mock Experiment database structure
        experiments_dir = temp_path / "research" / "experiments"
        experiments_dir.mkdir(parents=True, exist_ok=True)

        # --- Experiment 1 (EURUSD Standard Run) ---
        run1_dir = experiments_dir / "run_000001"
        run1_dir.mkdir()
        run1_data = {
            "run_id": "run_000001",
            "metadata": {
                "instrument": "EURUSD",
                "timeframe": "M1",
                "strategy_name": "Adaptive EMA Recoil"
            },
            "parameter_set": {
                "lookback_period": 21,
                "recoil_threshold": 1.5
            },
            "strategy_traits": {
                "entry_type": "recoil"
            },
            "dna_feature_vector": {
                "bull_percent": 46.61,
                "bear_percent": 47.02
            },
            "outcome_vector": {
                "trades": 329,
                "profit_factor": 4.52
            },
            "robustness": {
                "walk_forward_score": 0.82
            }
        }
        with open(run1_dir / "run.json", "w", encoding="utf-8") as f:
            json.dump(run1_data, f)

        # --- Experiment 2 (Mismatched Scheme Run - Custom Keys & Missing values) ---
        run2_dir = experiments_dir / "run_000002"
        run2_dir.mkdir()
        run2_data = {
            "run_id": "run_000002",
            "metadata": {
                "instrument": "GBPUSD",
                "timeframe": "H1",
                "broker": "IC Markets"  # Unique custom metadata field
            },
            "parameter_set": {
                "lookback_period": 34,
                # Missing recoil_threshold
                "ma_type": "exponential"  # Unique parameter
            },
            "strategy_traits": {
                "entry_type": "recoil"
            },
            "dna_feature_vector": {
                "bull_percent": 50.11,
                "bear_percent": 49.89
            },
            "outcome_vector": {
                "trades": 150
                # Missing profit_factor
            },
            "robustness": {
                "walk_forward_score": 0.65
            }
        }
        with open(run2_dir / "run.json", "w", encoding="utf-8") as f:
            json.dump(run2_data, f)

        # --- Experiment 3 (Incomplete Run - Missing run.json) ---
        run3_dir = experiments_dir / "run_000003"
        run3_dir.mkdir()  # Empty run folder to simulate an interrupted test

        # 2. Run the FeatureMatrixBuilder
        builder = FeatureMatrixBuilder(project_root=temp_path)
        df = builder.build_matrix()

        # 3. Assertions and Verifications
        assert not df.empty, "DataFrame should not be empty!"
        assert len(df) == 2, f"Expected exactly 2 completed runs in matrix, got {len(df)}"
        
        # Verify run paths exist
        matrix_dir = temp_path / "research" / "matrix"
        csv_path = matrix_dir / "feature_matrix.csv"
        assert csv_path.exists(), "feature_matrix.csv was not generated!"

        # Verify dynamic flattening namespaces
        assert "metadata_instrument" in df.columns, "Metadata flattening failed!"
        assert "parameter_set_lookback_period" in df.columns, "Parameter set flattening failed!"
        assert "dna_feature_vector_bull_percent" in df.columns, "DNA vector flattening failed!"

        # Verify missing value handling (NaN filling)
        # Experiment 1 has no broker field -> should be NaN
        eurusd_row = df[df["run_id"] == "run_000001"].iloc[0]
        assert pd.isna(eurusd_row.get("metadata_broker")), "Missing values should map to NaN!"

        # Experiment 2 has a broker field -> should be preserved
        gbpusd_row = df[df["run_id"] == "run_000002"].iloc[0]
        assert gbpusd_row["metadata_broker"] == "IC Markets", "Custom field retrieval failed!"

        # Experiment 2 is missing profit_factor -> should be NaN
        assert pd.isna(gbpusd_row.get("outcome_vector_profit_factor")), "Missing fields must default to NaN!"

        print("\nAll Feature Matrix Builder verification assertions passed cleanly!")


if __name__ == "__main__":
    test_feature_matrix_builder()