import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from types import MappingProxyType


class ExperimentRecorder:
    """
    QuantForge Experiment Recorder v1.0.0
    
    Responsible for organizing, structuring, and storing the complete output 
    of individual trading strategy runs in dedicated, self-contained directories.
    """

    def __init__(self, project_root):
        """
        Initializes the ExperimentRecorder.

        Args:
            project_root (str or Path): The absolute or relative path to the root 
                                        of the QuantForge directory.
        """
        self.project_root = Path(project_root).resolve()
        self.experiments_dir = self.project_root / "research" / "experiments"
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        self.schema_version = "1.0.0"

    def list_deployment_outcomes(self) -> tuple:
        """Locate all persisted DeploymentOutcome run identifiers.

        Sprint 8.3 — read-only retrieval API consumed by OutcomeReader.

        Returns:
            tuple[str, ...]: Sorted run identifiers that contain a persisted
            deployment_outcome.json artifact.
        """
        run_ids = []
        for path in sorted(self.experiments_dir.glob("run_*")):
            if path.is_dir() and (path / "deployment_outcome.json").is_file():
                run_ids.append(path.name)
        return tuple(run_ids)

    def get_deployment_outcome(self, run_id: str) -> dict:
        """Retrieve the raw persisted DeploymentOutcome artifact for a run.

        Sprint 8.3 — read-only retrieval API consumed by OutcomeReader.

        Args:
            run_id (str): The run identifier (e.g. 'run_000001').

        Returns:
            dict: The raw persisted artifact data.

        Raises:
            ValueError: If the artifact cannot be located.
        """
        run_folder = self.experiments_dir / run_id
        artifact_file = run_folder / "deployment_outcome.json"
        if not artifact_file.is_file():
            raise ValueError(
                f"ExperimentRecorder could not locate deployment outcome artifact for run '{run_id}'."
            )
        with open(artifact_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def append_deployment_outcome(self, deployment_outcome) -> str:
        """Append a DeploymentOutcome to the experiment ledger as immutable evidence.

        Sprint 8.2 introduces this method to extend the ExperimentRecorder with
        the ability to capture deployment evidence. This method creates a new
        run directory for the deployment outcome and saves it as an immutable
        scientific artifact.

        Args:
            deployment_outcome: The DeploymentOutcome to append.

        Returns:
            str: The unique identifier for the appended deployment outcome.

        Raises:
            ValueError: If the deployment_outcome is invalid.
        """

        run_id = self._get_next_run_id()
        run_folder = self.experiments_dir / run_id
        run_folder.mkdir(parents=True, exist_ok=True)

        saved_files = []

        # Save the DeploymentOutcome as deployment_outcome.json
        deployment_file = run_folder / "deployment_outcome.json"
        deployment_data = {
            "schema_version": self.schema_version,
            "outcome_id": deployment_outcome.outcome_id,
            "strategy_manifest_id": deployment_outcome.strategy_manifest_id,
            "execution_reference": deployment_outcome.execution_reference,
            "execution_metadata": dict(deployment_outcome.execution_metadata),
            "deployment_metadata": dict(deployment_outcome.deployment_metadata),
            "recorded_timestamp": deployment_outcome.recorded_timestamp.isoformat(),
            "provenance": {
                "research_candidate_id": deployment_outcome.provenance.research_candidate_id,
                "validation_id": deployment_outcome.provenance.validation_id,
                "experiment_id": deployment_outcome.provenance.experiment_id,
                "strategy_manifest_id": deployment_outcome.provenance.strategy_manifest_id,
                "created_timestamp": deployment_outcome.provenance.created_timestamp.isoformat(),
            },
            "schema_version": deployment_outcome.schema_version,
        }

        with open(deployment_file, "w", encoding="utf-8") as f:
            json.dump(deployment_data, f, indent=4)
        saved_files.append("deployment_outcome.json")

        # Create and save manifest.json
        manifest_file = run_folder / "manifest.json"
        manifest_data = {
            "run_id": run_id,
            "files": saved_files,
        }

        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)
        saved_files.append("manifest.json")

        # Standard console report output
        print("================================================")
        print("QUANTFORGE EXPERIMENT RECORDER")
        print("================================================")
        print("Created Deployment Outcome")
        print(run_id)
        print("Saved Files")
        for filename in saved_files:
            print(filename)
        print("================================================")

        return run_id

    def _get_next_run_id(self) -> str:
        """
        Scans the experiments directory to find existing runs and sequentially 
        determines the next available run ID, ensuring previous runs are never overwritten.

        Returns:
            str: The sequential run ID in 'run_000001' format.
        """
        existing_runs = list(self.experiments_dir.glob("run_*"))
        if not existing_runs:
            return "run_000001"

        run_numbers = []
        for path in existing_runs:
            if path.is_dir():
                try:
                    parts = path.name.split("_")
                    if len(parts) == 2 and parts[0] == "run":
                        run_num = int(parts[1])
                        run_numbers.append(run_num)
                except (ValueError, IndexError):
                    continue

        next_num = max(run_numbers) + 1 if run_numbers else 1
        return f"run_{next_num:06d}"

    def _extract_dna_features(self, dna_profile: dict) -> dict:
        """
        Recursively traverses the DNA profile to dynamically extract 
        every numeric field (integer or float, excluding booleans) 
        and flattens them into a single-level feature vector.

        Args:
            dna_profile (dict): The raw loaded DNA profile dictionary.

        Returns:
            dict: A flattened dictionary containing core market characteristics.
        """
        features = {}
        if not isinstance(dna_profile, dict):
            return features

        def traverse(data, prefix=""):
            if isinstance(data, dict):
                for k, v in data.items():
                    new_key = f"{prefix}_{k}" if prefix else k
                    traverse(v, new_key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    new_key = f"{prefix}_{i}" if prefix else str(i)
                    traverse(item, new_key)
            else:
                # Ensure we capture integers/floats while ignoring booleans (since bool is a subclass of int)
                if isinstance(data, (int, float)) and not isinstance(data, bool):
                    features[prefix] = data

        traverse(dna_profile)
        return features

    def save_experiment(
        self,
        metadata: dict,
        parameter_set: dict,
        strategy_traits: dict,
        dna_profile: dict,
        outcome_vector: dict,
        robustness: dict,
        trades_df: pd.DataFrame = None,
        equity_df: pd.DataFrame = None
    ) -> str:
        """
        Creates a dedicated folder for the current run, writes all individual artifacts 
        and structural summaries, and generates the consolidated run.json file.

        Args:
            metadata (dict): Contextual facts (e.g., strategy name, dates).
            parameter_set (dict): Free-form dynamic parameter key-values.
            strategy_traits (dict): Standardized classifications of strategy style.
            dna_profile (dict): Complete raw DNA snapshot dict.
            outcome_vector (dict): Analytical results and transaction costs metrics.
            robustness (dict): Walk-forward, stress tests, and MC parameters.
            trades_df (pd.DataFrame, optional): Flat list of individual trade logs.
            equity_df (pd.DataFrame, optional): Historical time-series equity curve.

        Returns:
            str: The unique generated run directory name (e.g., 'run_000001').
        """
        run_id = self._get_next_run_id()
        run_folder = self.experiments_dir / run_id
        run_folder.mkdir(parents=True, exist_ok=True)

        saved_files = []

        # 1. Compile and save metadata.json (preserving user fields + ensuring defaults exist)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        defaults = {
            "instrument": "UNKNOWN",
            "timeframe": "UNKNOWN",
            "strategy_name": "UNKNOWN",
            "strategy_version": "UNKNOWN",
            "date_range_start": "UNKNOWN",
            "date_range_end": "UNKNOWN",
            "timestamp": current_time,
            "QuantForge_version": "1.0.0"
        }
        metadata_to_store = {**defaults, **metadata}
        
        metadata_file = run_folder / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata_to_store, f, indent=4)
        saved_files.append("metadata.json")

        # 2. Save dna_snapshot.json (exact copy of market environment)
        dna_snapshot_file = run_folder / "dna_snapshot.json"
        with open(dna_snapshot_file, "w", encoding="utf-8") as f:
            json.dump(dna_profile, f, indent=4)
        saved_files.append("dna_snapshot.json")

        # 3. Filter and save robustness.json (summaries only, no large raw lists)
        robustness_keys = [
            "walk_forward_score",
            "monte_carlo_ruin_probability",
            "spread_stress_factor",
            "latency_stress_factor",
            "sequence_stability"
        ]
        robustness_to_store = {
            key: robustness.get(key, 0.0) for key in robustness_keys
        }
        
        robustness_file = run_folder / "robustness.json"
        with open(robustness_file, "w", encoding="utf-8") as f:
            json.dump(robustness_to_store, f, indent=4)
        saved_files.append("robustness.json")

        # 4. Save trades.csv (if supplied)
        if trades_df is not None and isinstance(trades_df, pd.DataFrame):
            trades_file = run_folder / "trades.csv"
            trades_df.to_csv(trades_file, index=False)
            saved_files.append("trades.csv")

        # 5. Save equity.csv (if supplied)
        if equity_df is not None and isinstance(equity_df, pd.DataFrame):
            equity_file = run_folder / "equity.csv"
            equity_df.to_csv(equity_file, index=False)
            saved_files.append("equity.csv")

        # 6. Compile and save the master structural contract: run.json
        dna_features = self._extract_dna_features(dna_profile)
        run_master_data = {
            "schema_version": self.schema_version,
            "run_id": run_id,
            "metadata": metadata_to_store,
            "parameter_set": parameter_set,
            "strategy_traits": strategy_traits,
            "dna_feature_vector": dna_features,
            "outcome_vector": outcome_vector,
            "robustness": robustness_to_store
        }

        run_file = run_folder / "run.json"
        with open(run_file, "w", encoding="utf-8") as f:
            json.dump(run_master_data, f, indent=4)
        saved_files.insert(0, "run.json")

        # 7. Create and save manifest.json
        saved_files.append("manifest.json")
        manifest_data = {
            "run_id": run_id,
            "files": saved_files
        }
        
        manifest_file = run_folder / "manifest.json"
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)

        # Standard console report output
        print("================================================")
        print("QUANTFORGE EXPERIMENT RECORDER")
        print("================================================")
        print("Created Run")
        print(run_id)
        print("Saved Files")
        for filename in saved_files:
            print(filename)
        print("================================================")

        return run_id