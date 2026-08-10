import pandas as pd
from typing import List, Dict, Any

from research.analytics.report import ValidationReport


class AggregationReporter:
    """
    Transforms a collection of individual experiment reports into deterministic, 
    aggregated descriptive analytics to evaluate parameter sensitivity and robustness.
    """
    
    @staticmethod
    def aggregate_to_dataframe(reports: List[ValidationReport]) -> pd.DataFrame:
        """
        Creates a flat DataFrame containing parameters and key metrics for all runs.
        """
        rows = []
        
        for report in reports:
            # Flatten parameters
            row = {}
            row["experiment_id"] = report.experiment_id
            row["dataset_id"] = report.dataset_id
            row["dataset_partition"] = report.dataset_partition if hasattr(report, "dataset_partition") else "UNKNOWN"
            row["strategy_id"] = report.strategy_id
            row["status"] = report.execution_assumptions.get("orchestration_status", "UNKNOWN")
            
            for param_name, param_val in report.strategy_parameters.items():
                row[f"param_{param_name}"] = param_val
                
            # Flatten metrics
            res = report.results
            row["trades"] = res.number_of_trades
            row["net_pnl"] = res.net_pnl
            row["win_rate"] = res.win_rate
            row["profit_factor"] = res.profit_factor
            row["max_drawdown"] = res.maximum_drawdown
            row["max_dd_pct"] = res.maximum_drawdown_percentage
            
            rows.append(row)
            
        return pd.DataFrame(rows)

    @staticmethod
    def analyze_parameter_sensitivity(df: pd.DataFrame, param_name: str) -> pd.DataFrame:
        """
        Groups the aggregate dataframe by a specific parameter to reveal performance distributions.
        This provides descriptive analytics without claiming a 'best' parameter.
        """
        target_col = f"param_{param_name}"
        if target_col not in df.columns:
            raise ValueError(f"Parameter '{param_name}' not found in aggregated reports.")
            
        # Filter out failed runs for meaningful stats
        valid_df = df[df["status"] == "SUCCESS"]
        
        # Calculate median and std for key metrics across the specific parameter slices
        grouped = valid_df.groupby(target_col).agg(
            median_pnl=("net_pnl", "median"),
            mean_pnl=("net_pnl", "mean"),
            median_win_rate=("win_rate", "median"),
            median_profit_factor=("profit_factor", "median"),
            median_drawdown=("max_dd_pct", "median"),
            sample_size=("dataset_id", "count")
        ).reset_index()
        
        return grouped
