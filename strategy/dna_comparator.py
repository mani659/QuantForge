import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

class MarketDNAComparator:
    def __init__(self):
        self.version = "1.1.0"
        
        # 1. Project Path Standardization
        # Resolves the QuantForge root assuming this script is in QuantForge/strategy/
        self.project_root = Path(__file__).resolve().parent.parent
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.profiles = {}
        self.metrics_df = None
        self.feature_corr = None

    def load_profiles(self):
        """Discovers and loads all DNA profile JSON files in the reports directory."""
        file_paths = list(self.reports_dir.glob("*_dna_profile.json"))
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    instrument = data.get("dataset_information", {}).get("instrument", "UNKNOWN")
                    if instrument != "UNKNOWN":
                        self.profiles[instrument] = data
            except Exception as e:
                print(f"Failed to load {file_path.name}: {e}")
                
        return len(self.profiles)

    def _extract_highest_activity_stat(self, intraday_activity, key):
        """Safely extracts both the hour and the max value for a given metric."""
        if not intraday_activity:
            return None, 0.0
        highest = max(intraday_activity, key=lambda x: x.get(key, 0))
        return highest.get("hour"), highest.get(key, 0)

    def _extract_extreme_event(self, events_list, key):
        """Safely extracts the highest value from extreme events."""
        if not events_list:
            return 0.0
        return max([event.get(key, 0) for event in events_list])

    def compile_metrics(self):
        """Extracts required metrics (Averages, Medians, Percentiles) into a structured format."""
        compiled_data = []
        
        for instrument, data in self.profiles.items():
            bull_bear = data.get("bull_bear_statistics", {})
            volatility = data.get("volatility_profile", {})
            atr = data.get("atr_profile", {})
            trend = data.get("trend_persistence", {})
            pullback = data.get("pullback_statistics", {})
            expansion = data.get("expansion_statistics", {}).get("size", {})
            volume = data.get("volume_profile", {})
            intraday = data.get("intraday_activity", [])
            extremes = data.get("extreme_events", {})

            total_candles = data.get("dataset_information", {}).get("total_candles", 1)
            doji_pct = (bull_bear.get("doji_candles", 0) / total_candles) * 100 if total_candles else 0

            # Get peak intraday stats for fingerprinting
            peak_vol_hour, peak_vol_val = self._extract_highest_activity_stat(intraday, "average_volume")
            peak_rng_hour, peak_rng_val = self._extract_highest_activity_stat(intraday, "average_range")

            record = {
                "Instrument": instrument,
                "Bull_%": bull_bear.get("bull_percent", 0),
                "Bear_%": bull_bear.get("bear_percent", 0),
                "Doji_%": doji_pct,
                "Avg_Bull_Body": bull_bear.get("average_bullish_body", 0),
                "Avg_Bear_Body": bull_bear.get("average_bearish_body", 0),
                "Avg_Range": volatility.get("average_range", 0),
                "Med_Range": volatility.get("median_range", 0),
                "P95_Range": volatility.get("range_95", 0),
                "Avg_ATR": atr.get("mean", 0),
                "ATR_Std": atr.get("std", 0),
                "Avg_Trend_Length": trend.get("average_trend_length", 0),
                "Med_Trend_Length": trend.get("median_trend_length", 0),
                "Max_Trend_Length": trend.get("maximum_trend_length", 0),
                "Avg_Pullback": pullback.get("mean", 0),
                "Med_Pullback": pullback.get("median", 0),
                "P95_Pullback": pullback.get("p95", 0),
                "Avg_Expansion": expansion.get("mean", 0),
                "Med_Expansion": expansion.get("median", 0),
                "P95_Expansion": expansion.get("p95", 0),
                "Avg_Volume": volume.get("average_volume", 0),
                "Med_Volume": volume.get("median_volume", 0),
                "Max_Volume": volume.get("maximum_volume", 0),
                "Peak_Volume_Val": peak_vol_val,
                "Peak_Range_Val": peak_rng_val,
                "Largest_Candle": self._extract_extreme_event(extremes.get("largest_candles", []), "range"),
                "Largest_ATR": self._extract_extreme_event(extremes.get("largest_atr", []), "atr")
            }
            compiled_data.append(record)
            
        self.metrics_df = pd.DataFrame(compiled_data).set_index("Instrument")

    def generate_rankings(self):
        """Generates cross-market rankings for every numerical metric."""
        rankings = {}
        for col in self.metrics_df.select_dtypes(include=[np.number]).columns:
            sorted_series = self.metrics_df[col].sort_values(ascending=False)
            rankings[col] = {i+1: instr for i, instr in enumerate(sorted_series.index)}
        return rankings

    def calculate_similarity_matrix(self):
        """Calculates Euclidean distance similarity matrix on ALL normalized numerical metrics."""
        df_num = self.metrics_df.select_dtypes(include=[np.number]).copy()
        
        # Min-Max Normalization to scale 0-1 for fair comparison across asset classes
        df_norm = (df_num - df_num.min()) / (df_num.max() - df_num.min() + 1e-9)
        
        instruments = df_norm.index
        dist_matrix = pd.DataFrame(index=instruments, columns=instruments, dtype=float)
        
        for i in instruments:
            for j in instruments:
                dist = np.linalg.norm(df_norm.loc[i] - df_norm.loc[j])
                dist_matrix.loc[i, j] = round(dist, 2)
                
        return dist_matrix

    def calculate_feature_correlation(self):
        """Calculates the correlation between different DNA metrics (e.g., Trend vs Pullback)."""
        df_num = self.metrics_df.select_dtypes(include=[np.number])
        self.feature_corr = df_num.corr(method='pearson')
        return self.feature_corr

    def generate_fingerprints(self):
        """Generates expanded deterministic fingerprints based on statistical rankings."""
        fingerprints = {}
        
        for instr in self.metrics_df.index:
            row = self.metrics_df.loc[instr]
            traits = []
            
            # Trend Persistence
            if row["Avg_Trend_Length"] >= self.metrics_df["Avg_Trend_Length"].quantile(0.75):
                traits.append("High trend persistence")
            elif row["Avg_Trend_Length"] <= self.metrics_df["Avg_Trend_Length"].quantile(0.25):
                traits.append("Low trend persistence")
                
            # Expansion vs Pullback Dominance
            if row["Avg_Expansion"] > (row["Avg_Pullback"] * 1.05):
                traits.append("Expansion dominated")
            elif row["Avg_Pullback"] > (row["Avg_Expansion"] * 1.05):
                traits.append("Pullback dominated")

            # Deep Pullbacks
            if row["P95_Pullback"] >= self.metrics_df["P95_Pullback"].quantile(0.75):
                traits.append("Deep extreme pullbacks")
                
            # Directional Balance
            bull_bear_diff = abs(row["Bull_%"] - row["Bear_%"])
            if bull_bear_diff < 0.5:
                traits.append("Highly balanced direction")
            elif bull_bear_diff > 2.0:
                traits.append(f"Directional bias ({'Bull' if row['Bull_%'] > row['Bear_%'] else 'Bear'})")
                
            # Liquidity & Session Concentration
            avg_vol = row["Avg_Volume"]
            peak_vol = row["Peak_Volume_Val"]
            if avg_vol > 0:
                traits.append("High liquidity (Volume verified)")
                if peak_vol > (avg_vol * 2.0):
                    traits.append("Session concentrated volume")
            else:
                traits.append("Tick-driven / Synthetic liquidity")
                
            # Volatility Clustering
            if row["ATR_Std"] >= self.metrics_df["ATR_Std"].quantile(0.75):
                traits.append("High volatility clustering")
            elif row["ATR_Std"] <= self.metrics_df["ATR_Std"].quantile(0.25):
                traits.append("Low volatility clustering")
                
            fingerprints[instr] = traits
            
        return fingerprints

    def get_strongest_correlations(self):
        """Extracts the strongest positive and negative feature correlations."""
        if self.feature_corr is None:
            return pd.Series(), pd.Series()
            
        # Get upper triangle to avoid duplicates and self-correlations
        upper_tri = self.feature_corr.where(np.triu(np.ones(self.feature_corr.shape), k=1).astype(bool))
        pairs = upper_tri.unstack().dropna()
        
        strong_pos = pairs[pairs >= 0.8].sort_values(ascending=False).head(5)
        strong_neg = pairs[pairs <= -0.8].sort_values(ascending=True).head(5)
        
        return strong_pos, strong_neg

    def execute_and_export(self):
        """Runs the comparator pipeline and outputs standard reports."""
        count = self.load_profiles()
        if count == 0:
            print(f"No DNA profiles found in {self.reports_dir}")
            return

        self.compile_metrics()
        rankings = self.generate_rankings()
        similarity = self.calculate_similarity_matrix()
        self.calculate_feature_correlation()
        fingerprints = self.generate_fingerprints()
        
        strong_pos_corr, strong_neg_corr = self.get_strongest_correlations()

        # 1. Export CSV Data
        self.metrics_df.to_csv(self.reports_dir / "dna_metrics_compiled.csv")
        self.feature_corr.to_csv(self.reports_dir / "dna_feature_correlations.csv")
        similarity.to_csv(self.reports_dir / "dna_similarity_matrix.csv")

        # 2. Export JSON
        json_output = {
            "module": "QuantForge Market DNA Comparator",
            "version": self.version,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profiles_loaded": count,
            "instrument_fingerprints": fingerprints,
            "rankings": rankings,
            "similarity_matrix": similarity.to_dict(),
            "feature_correlations": self.feature_corr.to_dict()
        }
        with open(self.reports_dir / "dna_comparison.json", "w") as f:
            json.dump(json_output, f, indent=4)

        # 3. Build TXT Report
        txt_output = [
            "================================================",
            "QUANTFORGE DNA COMPARATOR v1.1",
            "================================================",
            f"Profiles Loaded      : {count}",
            f"Most Volatile        : {self.metrics_df['Avg_ATR'].idxmax()}",
            f"Strongest Trends     : {self.metrics_df['Avg_Trend_Length'].idxmax()}",
            f"Deepest Pullbacks    : {self.metrics_df['P95_Pullback'].idxmax()}",
            f"Most Balanced Market : {abs(self.metrics_df['Bull_%'] - self.metrics_df['Bear_%']).idxmin()}",
            "",
            "INSTRUMENT FINGERPRINTS",
            "------------------------------------------------"
        ]
        
        for instr, traits in fingerprints.items():
            txt_output.append(f"{instr}:")
            for trait in traits:
                txt_output.append(f"  - {trait}")
            txt_output.append("")

        txt_output.extend([
            "STRONGEST FEATURE CORRELATIONS (Across Markets)",
            "------------------------------------------------"
        ])
        
        if not strong_pos_corr.empty:
            txt_output.append("Positive Correlations:")
            for (f1, f2), val in strong_pos_corr.items():
                txt_output.append(f"  {f1} <--> {f2} : {val:.3f}")
        
        if not strong_neg_corr.empty:
            txt_output.append("\nNegative Correlations:")
            for (f1, f2), val in strong_neg_corr.items():
                txt_output.append(f"  {f1} <--> {f2} : {val:.3f}")

        txt_output.extend([
            "",
            "FULL METRIC RANKINGS",
            "------------------------------------------------"
        ])
        
        for col, rank_dict in rankings.items():
            txt_output.append(f"\nMetric: {col}")
            for rank, instr in rank_dict.items():
                txt_output.append(f"  {rank}. {instr}")

        txt_output.extend([
            "",
            "================================================",
            "Data saved to /reports/:",
            " - dna_comparison.txt",
            " - dna_comparison.json",
            " - dna_metrics_compiled.csv",
            " - dna_similarity_matrix.csv",
            " - dna_feature_correlations.csv",
            "================================================"
        ])

        console_str = "\n".join(txt_output)
        with open(self.reports_dir / "dna_comparison.txt", "w") as f:
            f.write(console_str)

        print(console_str)

if __name__ == "__main__":
    comparator = MarketDNAComparator()
    comparator.execute_and_export()