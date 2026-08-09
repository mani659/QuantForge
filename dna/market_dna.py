"""Descriptive Market DNA profiling for validated M1 candle datasets.

This module measures market characteristics only. It does not classify markets,
generate signals, score instruments, or recommend strategies.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


# ==========================================================
# Project Configuration
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data" / "m1"
REPORT_FOLDER = PROJECT_ROOT / "reports"

# Change this filename to profile another instrument.
FILE_NAME = "USATECHIDXUSD_M1.csv"
INPUT_FILE = DATA_FOLDER / FILE_NAME

ATR_PERIOD = 14
EXTREME_EVENT_COUNT = 10
MIN_TREND_STEPS = 2


def _stat_summary(values: pd.Series | np.ndarray) -> dict[str, float]:
    """Return a consistent descriptive summary for a numeric series."""

    array = np.asarray(values, dtype=np.float64)
    array = array[np.isfinite(array)]
    if not len(array):
        return {
            "mean": 0.0, "median": 0.0, "std": 0.0,
            "p95": 0.0, "p99": 0.0, "maximum": 0.0,
        }

    return {
        "mean": float(np.mean(array)),
        "median": float(np.median(array)),
        "std": float(np.std(array)),
        "p95": float(np.percentile(array, 95)),
        "p99": float(np.percentile(array, 99)),
        "maximum": float(np.max(array)),
    }


def _serialise_records(frame: pd.DataFrame) -> list[dict]:
    """Convert timestamped DataFrame rows into JSON-safe report records."""

    records: list[dict] = []
    for row in frame.to_dict(orient="records"):
        record = {}
        for key, value in row.items():
            if isinstance(value, pd.Timestamp):
                record[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, np.generic):
                record[key] = value.item()
            else:
                record[key] = value
        records.append(record)
    return records


class MarketDNAProfiler:
    """Measure core descriptive characteristics for a single M1 dataset."""

    def __init__(self, file_path: Path | str = INPUT_FILE) -> None:
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(self.file_path)

        self.instrument = self.file_path.stem.removesuffix("_M1")
        self.data: pd.DataFrame | None = None
        self.profile: dict = {}

    def _load_data(self) -> pd.DataFrame:
        """Load the standard QuantForge M1 format with lightweight aliases."""

        raw = pd.read_csv(self.file_path)
        columns = {str(column).strip().lower(): column for column in raw.columns}
        timestamp_column = columns.get("timestamp", columns.get("datetime"))
        volume_column = columns.get("volume", columns.get("tick_volume"))
        required = {"open", "high", "low", "close"}

        if timestamp_column is None or volume_column is None or not required.issubset(columns):
            raise ValueError(
                "Expected M1 columns: timestamp (or datetime), open, high, low, "
                "close, and volume (or tick_volume)."
            )

        data = pd.DataFrame({
            "timestamp": pd.to_datetime(raw[timestamp_column], errors="coerce"),
            "open": pd.to_numeric(raw[columns["open"]], errors="coerce"),
            "high": pd.to_numeric(raw[columns["high"]], errors="coerce"),
            "low": pd.to_numeric(raw[columns["low"]], errors="coerce"),
            "close": pd.to_numeric(raw[columns["close"]], errors="coerce"),
            "volume": pd.to_numeric(raw[volume_column], errors="coerce"),
        })

        invalid = data.isna().any(axis=1) | ~np.isfinite(
            data[["open", "high", "low", "close", "volume"]]
        ).all(axis=1)
        if invalid.any():
            raise ValueError(
                "The M1 input contains invalid rows. Run candle_validator.py "
                "and resolve its reported issues before profiling."
            )

        return data

    @staticmethod
    def _run_lengths(mask: pd.Series) -> np.ndarray:
        """Return lengths of consecutive True values without per-candle loops."""

        groups = mask.ne(mask.shift()).cumsum()
        lengths = mask[mask].groupby(groups[mask]).size()
        return lengths.to_numpy(dtype=np.int64)

    def _directional_legs(self, close: pd.Series) -> pd.DataFrame:
        """Build runs of same-direction close-to-close moves.

        A zero close change ends a run. A leg length is measured in close-to-close
        steps, making it independent of an instrument's price scale.
        """

        changes = np.sign(np.diff(close.to_numpy(dtype=np.float64)))
        runs = pd.DataFrame({
            "direction": changes,
            "step": np.arange(len(changes)),
        })
        runs["run_id"] = (
            (runs["direction"] != runs["direction"].shift()) |
            (runs["direction"] == 0)
        ).cumsum()
        legs = runs.loc[runs["direction"] != 0].groupby("run_id", sort=False).agg(
            direction=("direction", "first"),
            start_step=("step", "min"),
            end_step=("step", "max"),
            length=("step", "size"),
        ).reset_index(drop=True)

        close_values = close.to_numpy(dtype=np.float64)
        legs["move"] = np.abs(
            close_values[legs["end_step"].to_numpy() + 1] -
            close_values[legs["start_step"].to_numpy()]
        )
        return legs

    def _trend_profile(self, data: pd.DataFrame) -> tuple[dict, np.ndarray, np.ndarray]:
        """Measure close-direction legs, reversal pullbacks, and resumptions."""

        legs = self._directional_legs(data["close"])
        lengths = legs["length"].to_numpy(dtype=np.float64)
        distribution = (
            legs["length"].value_counts().sort_index().astype(int).to_dict()
            if not legs.empty else {}
        )

        eligible = legs.loc[legs["length"] >= MIN_TREND_STEPS].reset_index(drop=True)
        pullbacks = np.array([], dtype=np.float64)
        expansions = np.array([], dtype=np.float64)
        expansion_durations = np.array([], dtype=np.float64)

        if len(eligible) >= 3:
            first = eligible.iloc[:-2].reset_index(drop=True)
            second = eligible.iloc[1:-1].reset_index(drop=True)
            third = eligible.iloc[2:].reset_index(drop=True)
            resumed = (
                (second["direction"].to_numpy() == -first["direction"].to_numpy()) &
                (third["direction"].to_numpy() == first["direction"].to_numpy())
            )
            pullbacks = second.loc[resumed, "move"].to_numpy(dtype=np.float64)
            expansions = third.loc[resumed, "move"].to_numpy(dtype=np.float64)
            expansion_durations = third.loc[resumed, "length"].to_numpy(dtype=np.float64)

        return (
            {
                "average_trend_length": float(np.mean(lengths)) if len(lengths) else 0.0,
                "median_trend_length": float(np.median(lengths)) if len(lengths) else 0.0,
                "maximum_trend_length": int(np.max(lengths)) if len(lengths) else 0,
                "distribution": {str(key): int(value) for key, value in distribution.items()},
                "methodology": (
                    "A trend is a consecutive run of non-zero close-to-close moves "
                    "in one direction; length is measured in close-to-close steps."
                ),
            },
            pullbacks,
            np.column_stack((expansions, expansion_durations)) if len(expansions) else np.empty((0, 2)),
        )

    @staticmethod
    def _hourly_profile(data: pd.DataFrame) -> list[dict]:
        """Return the per-hour statistical fingerprint."""

        hourly = data.groupby(data["timestamp"].dt.hour).agg(
            average_range=("range", "mean"),
            average_body=("body", "mean"),
            average_atr=("atr", "mean"),
            bull_percent=("bull", "mean"),
            bear_percent=("bear", "mean"),
            average_volume=("volume", "mean"),
        )
        hourly["bull_percent"] *= 100
        hourly["bear_percent"] *= 100
        hourly.index.name = "hour"
        return _serialise_records(hourly.reset_index().round(8))

    @staticmethod
    def _weekday_profile(data: pd.DataFrame) -> list[dict]:
        """Return Monday-to-Friday descriptive statistics."""

        names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        weekdays = data.loc[data["timestamp"].dt.weekday < 5].copy()
        weekdays["day"] = weekdays["timestamp"].dt.weekday
        summary = weekdays.groupby("day").agg(
            average_range=("range", "mean"),
            bull_percent=("bull", "mean"),
            bear_percent=("bear", "mean"),
            average_volume=("volume", "mean"),
        ).reindex(range(5), fill_value=0.0)
        summary["bull_percent"] *= 100
        summary["bear_percent"] *= 100
        summary.insert(0, "day", names)
        return _serialise_records(summary.reset_index(drop=True).round(8))

    @staticmethod
    def _extreme_events(data: pd.DataFrame) -> dict[str, list[dict]]:
        """Capture timestamped top-ten candle, ATR, and volume observations."""

        return {
            "largest_candles": _serialise_records(
                data.nlargest(EXTREME_EVENT_COUNT, "range")[["timestamp", "range"]]
            ),
            "largest_atr": _serialise_records(
                data.dropna(subset=["atr"]).nlargest(EXTREME_EVENT_COUNT, "atr")[["timestamp", "atr"]]
            ),
            "largest_volumes": _serialise_records(
                data.nlargest(EXTREME_EVENT_COUNT, "volume")[["timestamp", "volume"]]
            ),
        }

    def profile_market(self) -> dict:
        """Build and export the complete descriptive profile."""

        print("=" * 60)
        print("QuantForge Market DNA Profiler v1.0.0")
        print("=" * 60)
        print(f"File : {self.file_path.name}")
        print("Loading M1 Candle Data...")

        data = self._load_data()
        self.data = data
        print(f"Profiling {len(data):,} candles...")

        data["body"] = (data["close"] - data["open"]).abs()
        data["upper_wick"] = data["high"] - data[["open", "close"]].max(axis=1)
        data["lower_wick"] = data[["open", "close"]].min(axis=1) - data["low"]
        data["range"] = data["high"] - data["low"]

        previous_close = data["close"].shift(1)
        true_range = pd.concat([
            data["range"],
            (data["high"] - previous_close).abs(),
            (data["low"] - previous_close).abs(),
        ], axis=1).max(axis=1)
        data["atr"] = true_range.ewm(
            alpha=1 / ATR_PERIOD,
            adjust=False,
            min_periods=ATR_PERIOD,
        ).mean()

        data["bull"] = data["close"] > data["open"]
        data["bear"] = data["close"] < data["open"]
        data["doji"] = data["close"] == data["open"]

        bull_streaks = self._run_lengths(data["bull"])
        bear_streaks = self._run_lengths(data["bear"])
        trend_profile, pullbacks, expansion_data = self._trend_profile(data)

        candle_structure = {
            "body_size": _stat_summary(data["body"]),
            "upper_wick": _stat_summary(data["upper_wick"]),
            "lower_wick": _stat_summary(data["lower_wick"]),
            "full_range": _stat_summary(data["range"]),
        }
        bull_bear = {
            "bullish_candles": int(data["bull"].sum()),
            "bearish_candles": int(data["bear"].sum()),
            "doji_candles": int(data["doji"].sum()),
            "bull_percent": float(data["bull"].mean() * 100),
            "bear_percent": float(data["bear"].mean() * 100),
            "average_bullish_body": (
                float(data.loc[data["bull"], "body"].mean())
                if data["bull"].any() else 0.0
            ),
            "average_bearish_body": (
                float(data.loc[data["bear"], "body"].mean())
                if data["bear"].any() else 0.0
            ),
            "longest_bullish_streak": int(bull_streaks.max()) if len(bull_streaks) else 0,
            "longest_bearish_streak": int(bear_streaks.max()) if len(bear_streaks) else 0,
        }

        atr_values = data["atr"].dropna()
        range_summary = _stat_summary(data["range"])
        volatility = {
            "average_range": range_summary["mean"],
            "median_range": range_summary["median"],
            "maximum_range": range_summary["maximum"],
            "range_95": range_summary["p95"],
            "range_99": range_summary["p99"],
            "range_std": range_summary["std"],
            "coefficient_of_variation": (
                range_summary["std"] / range_summary["mean"]
                if range_summary["mean"] else 0.0
            ),
        }
        atr_profile = _stat_summary(atr_values)
        expansion_sizes = expansion_data[:, 0] if len(expansion_data) else np.array([])
        expansion_durations = expansion_data[:, 1] if len(expansion_data) else np.array([])

        self.profile = {
            "module": "QuantForge Market DNA Profiler",
            "version": "1.0.0",
            "dataset_information": {
                "instrument": self.instrument,
                "total_candles": int(len(data)),
                "first_candle": data.iloc[0]["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                "last_candle": data.iloc[-1]["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                "coverage_days": int((data.iloc[-1]["timestamp"] - data.iloc[0]["timestamp"]).days),
            },
            "candle_structure": candle_structure,
            "bull_bear_statistics": bull_bear,
            "volatility_profile": volatility,
            "atr_profile": {"period": ATR_PERIOD, **atr_profile},
            "trend_persistence": trend_profile,
            "pullback_statistics": _stat_summary(pullbacks),
            "expansion_statistics": {
                "size": _stat_summary(expansion_sizes),
                "duration_steps": _stat_summary(expansion_durations),
                "methodology": (
                    "A pullback is the opposite directional leg following a trend "
                    "leg of at least two close-to-close steps. Expansion is the "
                    "next leg when it resumes the original trend direction."
                ),
            },
            "intraday_activity": self._hourly_profile(data),
            "day_of_week_profile": self._weekday_profile(data),
            "volume_profile": {
                "average_volume": float(data["volume"].mean()),
                "median_volume": float(data["volume"].median()),
                "maximum_volume": float(data["volume"].max()),
                "volume_95": float(data["volume"].quantile(0.95)),
                "zero_volume_candles": int((data["volume"] == 0).sum()),
            },
            "extreme_events": self._extreme_events(data),
        }

        self.export_reports()
        self.print_summary()
        return self.profile

    def export_reports(self) -> None:
        """Write TXT, CSV, and JSON reports in the project reports folder."""

        REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
        base = self.instrument
        txt_file = REPORT_FOLDER / f"{base}_dna_profile.txt"
        csv_file = REPORT_FOLDER / f"{base}_dna_profile.csv"
        json_file = REPORT_FOLDER / f"{base}_dna_profile.json"

        with txt_file.open("w", encoding="utf-8") as report_file:
            report_file.write("QUANTFORGE MARKET DNA PROFILE\n")
            report_file.write("=" * 60 + "\n\n")
            report_file.write(json.dumps(self.profile, indent=2, default=str))
            report_file.write("\n")

        flat_report = {
            "instrument": self.instrument,
            "total_candles": self.profile["dataset_information"]["total_candles"],
            "coverage_days": self.profile["dataset_information"]["coverage_days"],
            "bull_percent": self.profile["bull_bear_statistics"]["bull_percent"],
            "bear_percent": self.profile["bull_bear_statistics"]["bear_percent"],
            "average_range": self.profile["volatility_profile"]["average_range"],
            "average_atr": self.profile["atr_profile"]["mean"],
            "average_trend_length": self.profile["trend_persistence"]["average_trend_length"],
            "average_pullback": self.profile["pullback_statistics"]["mean"],
            "average_expansion": self.profile["expansion_statistics"]["size"]["mean"],
            "hourly_fingerprint": json.dumps(self.profile["intraday_activity"]),
            "weekday_profile": json.dumps(self.profile["day_of_week_profile"]),
        }
        pd.DataFrame([flat_report]).to_csv(csv_file, index=False)

        with json_file.open("w", encoding="utf-8") as report_file:
            json.dump(self.profile, report_file, indent=2, default=str)

    def print_summary(self) -> None:
        """Print the concise measurement-only console summary."""

        profile = self.profile
        hourly = pd.DataFrame(profile["intraday_activity"])
        highest_volatility_hour = int(hourly.loc[hourly["average_range"].idxmax(), "hour"])
        highest_volume_hour = int(hourly.loc[hourly["average_volume"].idxmax(), "hour"])
        events = profile["extreme_events"]

        print("\n" + "=" * 48)
        print("MARKET DNA PROFILE")
        print("=" * 48)
        print(f"Instrument              : {self.instrument}")
        print(f"Coverage Days           : {profile['dataset_information']['coverage_days']}")
        print(f"Bull %                  : {profile['bull_bear_statistics']['bull_percent']:.2f}")
        print(f"Bear %                  : {profile['bull_bear_statistics']['bear_percent']:.2f}")
        print(f"Average Range           : {profile['volatility_profile']['average_range']:.8f}")
        print(f"Average ATR             : {profile['atr_profile']['mean']:.8f}")
        print(f"Average Trend Length    : {profile['trend_persistence']['average_trend_length']:.2f}")
        print(f"Average Pullback        : {profile['pullback_statistics']['mean']:.8f}")
        print(f"Average Expansion       : {profile['expansion_statistics']['size']['mean']:.8f}")
        print(f"Highest Volatility Hour : {highest_volatility_hour:02d}:00")
        print(f"Highest Volume Hour     : {highest_volume_hour:02d}:00")
        print(f"Longest Trend           : {profile['trend_persistence']['maximum_trend_length']}")
        print(f"Largest Candle          : {events['largest_candles'][0]['range']:.8f}")
        print(f"Largest ATR             : {events['largest_atr'][0]['atr']:.8f}")
        print(f"Largest Volume          : {events['largest_volumes'][0]['volume']:.2f}")
        print("=" * 48)


def main() -> None:
    """Profile the M1 file configured near the top of this module."""

    MarketDNAProfiler().profile_market()


if __name__ == "__main__":
    main()
