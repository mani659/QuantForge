import json
from pathlib import Path
import pandas as pd


class FeatureMatrixBuilder:
    """
    QuantForge Feature Matrix Builder v1.0.0
    
    Scans the research database directory, processes every complete experiment
    by parsing only the 'run.json' files, recursively flattens nested schemas 
    into a single-level feature row, and compiles a consolidated master dataset.
    """

    def __init__(self, project_root):
        """
        Initializes the FeatureMatrixBuilder.

        Args:
            project_root (str or Path): The absolute or relative path to the root 
                                        of the QuantForge directory.
        """
        self.project_root = Path(project_root).resolve()
        self.experiments_dir = self.project_root / "research" / "experiments"
        self.matrix_dir = self.project_root / "research" / "matrix"
        self.schema_version = "1.0.0"

    def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '_') -> dict:
        """
        Recursively traverses and flattens a nested dictionary structure, 
        combining nested keys with a separator (e.g., metadata_instrument).

        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): Accumulative key prefix from parent nesting levels.
            sep (str): Separator to use when joining keys.

        Returns:
            dict: A single-level flattened dictionary.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def build_matrix(self) -> pd.DataFrame:
        """
        Scans all experiment subdirectories, loads 'run.json' from completed runs,
        flattens nested components recursively, constructs a unified Pandas DataFrame,
        and saves it to both CSV and Parquet formats.

        Returns:
            pd.DataFrame: The generated, unified feature matrix.
        """
        rows = []
        
        # Ensure target database search space exists
        if not self.experiments_dir.exists():
            # If database doesn't exist yet, return an empty DataFrame gracefully
            return pd.DataFrame()

        # Iterate through experiment folders
        for run_dir in sorted(self.experiments_dir.glob("run_*")):
            if not run_dir.is_dir():
                continue

            run_file = run_dir / "run.json"
            if not run_file.exists():
                # Incomplete experiment: skip run gracefully
                continue

            try:
                with open(run_file, "r", encoding="utf-8") as f:
                    run_data = json.load(f)
            except Exception:
                # Corrupted file: skip run gracefully to maintain database compilation integrity
                continue

            # Establish baseline primary key identification
            run_id = run_data.get("run_id", run_dir.name)
            flat_row = {"run_id": run_id}

            # Target blocks to extract and recursively flatten
            target_blocks = [
                "metadata",
                "parameter_set",
                "strategy_traits",
                "dna_feature_vector",
                "outcome_vector",
                "robustness"
            ]

            for block_key in target_blocks:
                if block_key in run_data:
                    block_content = run_data[block_key]
                    if isinstance(block_content, dict):
                        # Flatten dictionary contents under prefix namespace
                        flat_row.update(self._flatten_dict(block_content, parent_key=block_key))
                    else:
                        # Fallback for scalar schemas
                        flat_row[block_key] = block_content

            rows.append(flat_row)

        # Build DataFrame (Pandas automatically aligns uneven columns and fills missing with NaN)
        if not rows:
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(rows)

        # Output persistence
        parquet_saved = False
        if not df.empty:
            self.matrix_dir.mkdir(parents=True, exist_ok=True)
            
            # Save CSV file (UTF-8)
            csv_path = self.matrix_dir / "feature_matrix.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8")

            # Save Parquet file gracefully (checks for pyarrow/fastparquet dependencies)
            try:
                import pyarrow
                parquet_path = self.matrix_dir / "feature_matrix.parquet"
                df.to_parquet(parquet_path, index=False)
                parquet_saved = True
            except (ImportError, Exception):
                pass

        # Console Report Generation
        print("================================================")
        print("QUANTFORGE FEATURE MATRIX BUILDER")
        print("================================================")
        print("Experiments Found")
        print(len(rows))
        print("Columns")
        print(df.shape[1] if not df.empty else 0)
        print("Rows")
        print(df.shape[0])
        print("Output")
        print("feature_matrix.csv")
        if parquet_saved:
            print("feature_matrix.parquet")
        print("================================================")

        return df