import json
from pathlib import Path
import numpy as np
import pandas as pd


class StrategyIntelligence:
    """
    QuantForge Strategy Intelligence Engine v1.0.0
    
    Reads the compiled 'feature_matrix.csv', automatically separates 
    machine-learning-ready features and outcome metrics based on configurable 
    prefixes, performs Pearson and Spearman correlation analysis, and ranks 
    the relationships to reveal what features drive strategy performance.
    """

    def __init__(self, project_root, feature_prefixes=None, outcome_prefixes=None):
        """
        Initializes the StrategyIntelligence Engine.

        Args:
            project_root (str or Path): Path to the QuantForge project root.
            feature_prefixes (list, optional): Column prefixes that identify features.
                Defaults to ["dna_feature_vector_", "strategy_traits_", "parameter_set_"].
            outcome_prefixes (list, optional): Column prefixes that identify outcomes.
                Defaults to ["outcome_vector_"].
        """
        self.project_root = Path(project_root).resolve()
        self.matrix_file = self.project_root / "research" / "matrix" / "feature_matrix.csv"
        self.reports_dir = self.project_root / "strategy" / "reports"
        
        self.feature_prefixes = feature_prefixes or [
            "dna_feature_vector_",
            "strategy_traits_",
            "parameter_set_"
        ]
        self.outcome_prefixes = outcome_prefixes or ["outcome_vector_"]
        self.schema_version = "1.0.0"

    def _calculate_spearman(self, s1: pd.Series, s2: pd.Series) -> float:
        """
        Calculates Spearman's rank correlation coefficient without requiring SciPy.
        This is mathematically equivalent to Pearson correlation of the ranks 
        on pairwise-complete observations.
        """
        # Align series and drop any rows with NaN in either column (pairwise deletion)
        valid_mask = s1.notna() & s2.notna()
        if not valid_mask.any():
            return np.nan
            
        s1_clean = s1[valid_mask]
        s2_clean = s2[valid_mask]
        
        # Avoid division by zero if standard deviation of ranks is zero (e.g., constant columns)
        if s1_clean.nunique() <= 1 or s2_clean.nunique() <= 1:
            return np.nan
            
        # Rank observations using average fractional ranking for ties (standard behavior)
        rank1 = s1_clean.rank(method='average')
        rank2 = s2_clean.rank(method='average')
        
        # Return standard Pearson correlation of these ranks
        p_corr = rank1.corr(rank2, method='pearson')
        return float(p_corr) if not pd.isna(p_corr) else np.nan

    def analyze(self) -> dict:
        """
        Loads the feature matrix, calculates Pearson and Spearman correlations
        between every numeric feature and outcome, ranks the most influential 
        positive and negative predictors, and writes both structured JSON 
        and human-readable TXT reports.

        Returns:
            dict: The complete analyzed correlation metrics and rankings structure.
        """
        if not self.matrix_file.exists():
            raise FileNotFoundError(
                f"Feature matrix not found at: {self.matrix_file}. "
                "Please run FeatureMatrixBuilder.build_matrix() first."
            )

        # Load matrix
        df = pd.read_csv(self.matrix_file)
        
        # If matrix is empty, return empty analysis structure gracefully
        if df.empty:
            return {
                "meta": {
                    "experiments_count": 0,
                    "features_count": 0,
                    "outcomes_count": 0,
                    "relationships_tested": 0
                },
                "correlations": {},
                "rankings": {}
            }

        # Select only numeric columns to completely ignore non-numeric parameters
        df_numeric = df.select_dtypes(include=[np.number])

        # Separate feature columns from outcome columns based on prefixes
        features = [
            col for col in df_numeric.columns 
            if any(col.startswith(p) for p in self.feature_prefixes)
        ]
        outcomes = [
            col for col in df_numeric.columns 
            if any(col.startswith(p) for p in self.outcome_prefixes)
        ]

        experiments_count = len(df)
        features_count = len(features)
        outcomes_count = len(outcomes)
        relationships_tested = features_count * outcomes_count

        analysis_results = {
            "meta": {
                "experiments_count": experiments_count,
                "features_count": features_count,
                "outcomes_count": outcomes_count,
                "relationships_tested": relationships_tested
            },
            "correlations": {},
            "rankings": {}
        }

        # Process correlations and rankings outcome-by-outcome
        for outcome in outcomes:
            analysis_results["correlations"][outcome] = {
                "pearson": {},
                "spearman": {}
            }
            analysis_results["rankings"][outcome] = {
                "pearson": {"top_positive": [], "top_negative": []},
                "spearman": {"top_positive": [], "top_negative": []}
            }

            pearson_vals = {}
            spearman_vals = {}

            # Calculate individual correlation coefficients
            for feature in features:
                # Pearson correlation (native, doesn't require scipy)
                p_corr = df_numeric[feature].corr(df_numeric[outcome], method='pearson')
                if not pd.isna(p_corr):
                    analysis_results["correlations"][outcome]["pearson"][feature] = float(p_corr)
                    pearson_vals[feature] = float(p_corr)
                
                # Zero-dependency Spearman rank correlation
                s_corr = self._calculate_spearman(df_numeric[feature], df_numeric[outcome])
                if not pd.isna(s_corr):
                    analysis_results["correlations"][outcome]["spearman"][feature] = float(s_corr)
                    spearman_vals[feature] = float(s_corr)

            # Extract top 5 Positive/Negative rankings (Pearson)
            if pearson_vals:
                pos_p = sorted(
                    [{"feature": f, "coefficient": c} for f, c in pearson_vals.items() if c > 0],
                    key=lambda x: x["coefficient"],
                    reverse=True
                )[:5]
                neg_p = sorted(
                    [{"feature": f, "coefficient": c} for f, c in pearson_vals.items() if c < 0],
                    key=lambda x: x["coefficient"]
                )[:5]
                analysis_results["rankings"][outcome]["pearson"]["top_positive"] = pos_p
                analysis_results["rankings"][outcome]["pearson"]["top_negative"] = neg_p

            # Extract top 5 Positive/Negative rankings (Spearman)
            if spearman_vals:
                pos_s = sorted(
                    [{"feature": f, "coefficient": c} for f, c in spearman_vals.items() if c > 0],
                    key=lambda x: x["coefficient"],
                    reverse=True
                )[:5]
                neg_s = sorted(
                    [{"feature": f, "coefficient": c} for f, c in spearman_vals.items() if c < 0],
                    key=lambda x: x["coefficient"]
                )[:5]
                analysis_results["rankings"][outcome]["spearman"]["top_positive"] = pos_s
                analysis_results["rankings"][outcome]["spearman"]["top_negative"] = neg_s

        # Write generated data structures and text reports
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Output json compilation
        json_path = self.reports_dir / "strategy_intelligence.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=4)

        # 2. Output human-readable .txt report
        txt_path = self.reports_dir / "strategy_intelligence.txt"
        self._write_txt_report(txt_path, analysis_results)

        # Print standard console output
        print("================================================")
        print("QUANTFORGE STRATEGY INTELLIGENCE")
        print("================================================")
        print(f"Experiments\n{experiments_count}")
        print(f"Features\n{features_count}")
        print(f"Outcome Metrics\n{outcomes_count}")
        print(f"Relationships Tested\n{relationships_tested}")
        print("Report Saved")
        print("strategy_intelligence.json")
        print("strategy_intelligence.txt")
        print("================================================")

        return analysis_results

    def _write_txt_report(self, path: Path, results: dict):
        """Compiles and writes a standardized text output formatted for visual analysis."""
        meta = results["meta"]
        with open(path, "w", encoding="utf-8") as f:
            f.write("================================================================================\n")
            f.write("QUANTFORGE STRATEGY INTELLIGENCE ENGINE v1.0.0\n")
            f.write("================================================================================\n")
            f.write(f"Experiments Analyzed: {meta['experiments_count']}\n")
            f.write(f"Features Processed: {meta['features_count']}\n")
            f.write(f"Outcome Metrics Processed: {meta['outcomes_count']}\n")
            f.write(f"Total Relationships Evaluated: {meta['relationships_tested']}\n\n")
            
            f.write("================================================================================\n")
            f.write("ANALYSIS BY OUTCOME METRIC\n")
            f.write("================================================================================\n\n")
            
            for outcome, methods in results["rankings"].items():
                f.write(f"--------------------------------------------------------------------------------\n")
                f.write(f"OUTCOME: {outcome}\n")
                f.write(f"--------------------------------------------------------------------------------\n")
                
                for method in ["pearson", "spearman"]:
                    f.write(f"{method.upper()} CORRELATION RANKINGS:\n")
                    
                    pos = methods[method]["top_positive"]
                    f.write("  Top Positive Features:\n")
                    if pos:
                        for idx, item in enumerate(pos, 1):
                            f.write(f"    {idx}. {item['feature']} ({item['coefficient']:.4f})\n")
                    else:
                        f.write("    (No positive correlation identified)\n")
                        
                    neg = methods[method]["top_negative"]
                    f.write("  Top Negative Features:\n")
                    if neg:
                        for idx, item in enumerate(neg, 1):
                            f.write(f"    {idx}. {item['feature']} ({item['coefficient']:.4f})\n")
                    else:
                        f.write("    (No negative correlation identified)\n")
                    f.write("\n")
                f.write("\n")