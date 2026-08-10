import json
from pathlib import Path
from dataclasses import dataclass, asdict

from research.experiment_recorder import ExperimentRecorder
from research.engine.configuration import ExperimentConfiguration
from research.analytics.metrics import ResearchResult


@dataclass(frozen=True)
class ValidationReport:
    """
    Deterministic research report containing config, results, and validation status.
    It deliberately avoids claiming strategies are 'profitable' or 'proven'.
    """
    experiment_id: str
    dataset_id: str
    dataset_partition: str
    instrument: str
    timeframe: str
    date_range_start: str
    date_range_end: str
    strategy_id: str
    strategy_version: str
    strategy_parameters: dict
    execution_assumptions: dict
    
    results: ResearchResult


class AnalyticsPersister:
    """
    Persists the ValidationReport alongside existing frozen BOE evidence 
    without modifying the execution boundary or the original evidence.
    """
    def __init__(self, recorder: ExperimentRecorder):
        self.experiments_dir = recorder.experiments_dir
        
    def save_report(
        self,
        run_id: str,
        report: ValidationReport
    ) -> str:
        """
        Persists a ValidationReport in the target run directory without altering its canonical identity.
        Returns the path to the written analytics report.
        """
        run_folder = self.experiments_dir / run_id
        if not run_folder.is_dir():
            raise ValueError(f"Run folder not found for run_id: {run_id}")
        
        report_file = run_folder / "analytics_report.json"
        
        # M5: Prevent silent overwrite
        if report_file.exists():
            raise FileExistsError(f"Analytics report already exists at {report_file}. Overwrite rejected to preserve reproducibility.")
            
        report_dict = asdict(report)
        
        # M5: Sanitize Infinity to valid JSON string
        if report_dict["results"]["profit_factor"] == float('inf'):
            report_dict["results"]["profit_factor"] = "Infinity"
            
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=4, allow_nan=False)
            
        # Update manifest.json to include the new file if it exists
        manifest_file = run_folder / "manifest.json"
        if manifest_file.is_file():
            with open(manifest_file, "r+", encoding="utf-8") as f:
                try:
                    manifest_data = json.load(f)
                    files = manifest_data.get("files", [])
                    if "analytics_report.json" not in files:
                        files.append("analytics_report.json")
                        manifest_data["files"] = files
                        f.seek(0)
                        json.dump(manifest_data, f, indent=4)
                        f.truncate()
                except json.JSONDecodeError:
                    pass
                    
        return str(report_file)
