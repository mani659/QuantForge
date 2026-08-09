"""
=========================================================
QuantForge Framework
Module : Tick Validator
Version: 1.1.0
=========================================================

Validates MT5 tick datasets before conversion to M1.

Outputs
-------
Console Report
TXT Report
CSV Report
JSON Report
"""

from pathlib import Path
import json
import math

import numpy as np
import pandas as pd


# ==========================================================
# Project Configuration
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FOLDER = PROJECT_ROOT / "data" / "tick"

REPORT_FOLDER = PROJECT_ROOT / "reports"

REPORT_FOLDER.mkdir(exist_ok=True)

FILE_NAME = "USATECHIDXUSD_mt5_ticks.csv"

INPUT_FILE = DATA_FOLDER / FILE_NAME

CHUNK_SIZE = 200000
QUANTILE_SAMPLE_SIZE = 250000


EXPECTED_COLUMNS = [

    "date",
    "time",
    "bid",
    "ask",
    "last",
    "volume"

]


# ==========================================================
# Validation Result
# ==========================================================

class ValidationResult:

    def __init__(self):

        self.file_name = ""
        self.file_size_mb = 0

        self.total_rows = 0

        self.first_tick = None
        self.last_tick = None

        self.coverage_days = 0

        self.backward_timestamps = 0
        self.duplicate_rows = 0

        self.invalid_timestamps = 0
        self.invalid_numeric_rows = 0

        self.largest_gap_seconds = 0
        self.weekend_gap = False

        self.missing_trading_days = []

        self.negative_prices = 0
        self.zero_prices = 0
        self.ask_less_than_bid = 0

        self.average_spread = 0
        self.median_spread = 0
        self.spread_95 = 0
        self.spread_99 = 0
        self.maximum_spread = 0

        self.average_ticks_per_minute = 0
        self.median_ticks_per_minute = 0
        self.min_ticks_per_minute = 0
        self.max_ticks_per_minute = 0
        self.tick95 = 0

        self.quantile_sample_size = 0
        self.quantiles_are_estimated = False

        self.multi_tick_seconds = 0
        self.average_ticks_per_second = 0
        self.maximum_ticks_per_second = 0

        self.pass_validation = True

    def to_dict(self):

        return self.__dict__


# ==========================================================
# Tick Validator
# ==========================================================

class TickValidator:

    def __init__(self, file_path=INPUT_FILE):

        self.file_path = Path(file_path)

        if not self.file_path.exists():

            raise FileNotFoundError(self.file_path)

        self.result = ValidationResult()

        self.result.file_name = self.file_path.name

        self.result.file_size_mb = (
            self.file_path.stat().st_size
            / (1024 * 1024)
        )

        self.previous_timestamp = None

        self.spread_sum = 0.0
        self.spread_count = 0
        self.spread_maximum = 0.0
        self.spread_sample = np.empty(0, dtype=np.float64)
        self.spread_priorities = np.empty(0, dtype=np.float64)

        self.pending_minute = None
        self.pending_minute_ticks = 0
        self.active_minute_count = 0
        self.total_minute_ticks = 0
        self.minimum_ticks_per_minute = None
        self.minute_sample = np.empty(0, dtype=np.float64)
        self.minute_priorities = np.empty(0, dtype=np.float64)

        self.random_generator = np.random.default_rng(20260712)

        self.pending_second = None
        self.pending_second_ticks = 0
        self.active_second_count = 0
        self.total_second_ticks = 0

        self.all_trading_days = set()

        print("=" * 60)
        print("QuantForge Tick Validator v1.1.0")
        print("=" * 60)
        print()
        print("File :", self.file_path.name)
        print()
        print("Reading Tick Data...")

    def validate(self):

        for chunk in pd.read_csv(

                self.file_path,

                names=EXPECTED_COLUMNS,

                sep=",",

                engine="c",

                chunksize=CHUNK_SIZE,

                dtype={
                    "date": str,
                    "time": str
                }

        ):

            self.result.total_rows += len(chunk)

            numeric_cols = [

                "bid",
                "ask",
                "last",
                "volume"

            ]

            chunk[numeric_cols] = chunk[numeric_cols].apply(

                pd.to_numeric,

                errors="coerce"

            )

            # ==========================================
            # Timestamp Conversion
            # ==========================================

            chunk["timestamp"] = pd.to_datetime(

                chunk["date"] + " " + chunk["time"],

                format="%Y%m%d %H:%M:%S",

                errors="coerce"

            )

            invalid_ts = chunk["timestamp"].isna()

            self.result.invalid_timestamps += int(
                invalid_ts.sum()
            )

            chunk = chunk.loc[~invalid_ts].copy()

            if len(chunk) == 0:
                continue

            # ==========================================
            # Invalid Numeric Detection
            # ==========================================

            invalid_numeric = (

                ~np.isfinite(
                    chunk[numeric_cols]
                )

            ).any(axis=1)

            self.result.invalid_numeric_rows += int(
                invalid_numeric.sum()
            )

            chunk = chunk.loc[
                ~invalid_numeric
            ].copy()

            if len(chunk) == 0:
                continue

            # ==========================================
            # First / Last Tick
            # ==========================================

            if self.result.first_tick is None:

                self.result.first_tick = chunk.iloc[0]["timestamp"]

            self.result.last_tick = chunk.iloc[-1]["timestamp"]

            # ==========================================
            # Duplicate Full Row Detection
            # ==========================================

            self.result.duplicate_rows += int(

                chunk.duplicated().sum()

            )

            # ==========================================
            # Vectorized Timestamp Validation
            # ==========================================

            ts = chunk["timestamp"]

            self._update_tick_second_statistics(ts)

            diff = ts.diff().dt.total_seconds()

            if self.previous_timestamp is not None:

                boundary_gap = (

                    ts.iloc[0] - self.previous_timestamp

                ).total_seconds()

                if boundary_gap < 0:

                    self.result.backward_timestamps += 1

                if boundary_gap > self.result.largest_gap_seconds:

                    self.result.largest_gap_seconds = float(boundary_gap)

            self.result.backward_timestamps += int(

                (diff < 0).sum()

            )

            max_gap = diff.max()

            if pd.notna(max_gap):

                if max_gap > self.result.largest_gap_seconds:

                    self.result.largest_gap_seconds = float(max_gap)

            self.previous_timestamp = ts.iloc[-1]

            # ==========================================
            # Weekend Gap Detection
            # ==========================================

            if (

                self.result.largest_gap_seconds >

                60 * 60 * 36

            ):

                self.result.weekend_gap = True

            # ==========================================
            # Trading Day Collection
            # ==========================================

            self.all_trading_days.update(

                ts.dt.normalize()

            )

            # ==========================================
            # Price Validation
            # ==========================================

            self.result.negative_prices += int(

                (

                    (chunk.bid < 0)

                    |

                    (chunk.ask < 0)

                ).sum()

            )

            self.result.zero_prices += int(

                (

                    (chunk.bid == 0)

                    |

                    (chunk.ask == 0)

                ).sum()

            )

            self.result.ask_less_than_bid += int(

                (

                    chunk.ask < chunk.bid

                ).sum()

            )

            # ==========================================
            # Spread Collection
            # ==========================================

            spread = chunk.ask - chunk.bid

            spread_values = spread.to_numpy(dtype=np.float64, copy=False)
            self.spread_sum += float(spread_values.sum())
            self.spread_count += len(spread_values)
            self.spread_maximum = max(
                self.spread_maximum,
                float(spread_values.max())
            )
            self._update_quantile_sample("spread", spread_values)

            # ==========================================
            # Tick Density
            # ==========================================

            self._update_tick_minute_statistics(ts)

            print(

                f"Processed {self.result.total_rows:,} rows",

                end="\r"

            )

        print()

        self._finalize_tick_second_statistics()
        self._finalize_tick_minute_statistics()

        # ==========================================================
        # Coverage
        # ==========================================================

        if (
            self.result.first_tick is not None
            and
            self.result.last_tick is not None
        ):

            self.result.coverage_days = (

                self.result.last_tick -
                self.result.first_tick

            ).days

        # ==========================================================
        # Missing Trading Days
        # ==========================================================

        if len(self.all_trading_days) > 0:

            trading_days = sorted(self.all_trading_days)

            full_range = pd.date_range(

                trading_days[0],
                trading_days[-1],
                freq="D"

            )

            for d in full_range:

                if d.weekday() >= 5:
                    continue

                if d not in self.all_trading_days:

                    self.result.missing_trading_days.append(

                        d.strftime("%Y-%m-%d")

                    )

        # ==========================================================
        # Spread Statistics
        # ==========================================================

        if self.spread_count:

            self.result.average_spread = (
                self.spread_sum / self.spread_count
            )
            self.result.median_spread = float(
                np.median(self.spread_sample)
            )
            self.result.spread_95 = float(
                np.percentile(self.spread_sample, 95)
            )
            self.result.spread_99 = float(
                np.percentile(self.spread_sample, 99)
            )
            self.result.maximum_spread = self.spread_maximum

        # ==========================================================
        # Tick Density Statistics
        # ==========================================================

        if self.active_minute_count:

            self.result.average_ticks_per_minute = (
                self.total_minute_ticks / self.active_minute_count
            )
            self.result.median_ticks_per_minute = float(
                np.median(self.minute_sample)
            )
            self.result.min_ticks_per_minute = int(
                self.minimum_ticks_per_minute
            )
            self.result.max_ticks_per_minute = int(
                self.result.max_ticks_per_minute
            )
            self.result.tick95 = float(
                np.percentile(self.minute_sample, 95)
            )

        self.result.quantile_sample_size = int(
            max(len(self.spread_sample), len(self.minute_sample))
        )
        self.result.quantiles_are_estimated = (
            self.spread_count > QUANTILE_SAMPLE_SIZE or
            self.active_minute_count > QUANTILE_SAMPLE_SIZE
        )

        # ==========================================================
        # PASS / FAIL
        # ==========================================================

        self.result.pass_validation = True

        fail_conditions = [

            self.result.backward_timestamps,

            self.result.invalid_timestamps,

            self.result.invalid_numeric_rows,

            self.result.ask_less_than_bid,

            self.result.negative_prices

        ]

        if any(x > 0 for x in fail_conditions):

            self.result.pass_validation = False

        # ==========================================================
        # Export Reports
        # ==========================================================

        self.export_reports()

        self.print_summary()

        return self.result

    def _update_quantile_sample(self, sample_name, values):
        """Maintain a bounded uniform sample for percentile estimates."""

        values = np.asarray(values, dtype=np.float64)
        if not len(values):
            return

        current_values = getattr(self, f"{sample_name}_sample")
        current_priorities = getattr(self, f"{sample_name}_priorities")
        new_priorities = self.random_generator.random(len(values))

        combined_values = np.concatenate((current_values, values))
        combined_priorities = np.concatenate(
            (current_priorities, new_priorities)
        )

        if len(combined_values) > QUANTILE_SAMPLE_SIZE:
            selected = np.argpartition(
                combined_priorities,
                QUANTILE_SAMPLE_SIZE - 1
            )[:QUANTILE_SAMPLE_SIZE]
            combined_values = combined_values[selected]
            combined_priorities = combined_priorities[selected]

        setattr(self, f"{sample_name}_sample", combined_values)
        setattr(self, f"{sample_name}_priorities", combined_priorities)

    def _record_minute_counts(self, counts):
        """Accumulate completed minute buckets without a growing dictionary."""

        if counts.empty:
            return

        values = counts.to_numpy(dtype=np.float64)
        self.active_minute_count += len(values)
        self.total_minute_ticks += int(values.sum())

        current_minimum = int(values.min())
        if self.minimum_ticks_per_minute is None:
            self.minimum_ticks_per_minute = current_minimum
        else:
            self.minimum_ticks_per_minute = min(
                self.minimum_ticks_per_minute,
                current_minimum
            )

        self.result.max_ticks_per_minute = max(
            self.result.max_ticks_per_minute,
            int(values.max())
        )
        self._update_quantile_sample("minute", values)

    def _update_tick_minute_statistics(self, timestamps):
        """Stream minute density statistics across chunk boundaries."""

        counts = (
            timestamps.dt.floor("min")
            .value_counts(sort=False)
            .sort_index()
        )

        if self.pending_minute is not None:
            if counts.index[0] == self.pending_minute:
                counts = counts.copy()
                counts.iloc[0] += self.pending_minute_ticks
            else:
                self._record_minute_counts(
                    pd.Series([self.pending_minute_ticks])
                )

        self._record_minute_counts(counts.iloc[:-1])
        self.pending_minute = counts.index[-1]
        self.pending_minute_ticks = int(counts.iloc[-1])

    def _finalize_tick_minute_statistics(self):
        """Flush the final pending minute after the last input chunk."""

        if self.pending_minute is not None:
            self._record_minute_counts(
                pd.Series([self.pending_minute_ticks])
            )
            self.pending_minute = None
            self.pending_minute_ticks = 0

    def _record_second_counts(self, counts):

        if counts.empty:
            return

        self.active_second_count += len(counts)
        self.total_second_ticks += int(counts.sum())

        self.result.multi_tick_seconds += int(
            (counts > 1).sum()
        )

        self.result.maximum_ticks_per_second = max(
            self.result.maximum_ticks_per_second,
            int(counts.max())
        )

    def _update_tick_second_statistics(self, timestamps):

        counts = (
            timestamps.dt.floor("s")
            .value_counts(sort=False)
            .sort_index()
        )

        if self.pending_second is not None:

            if counts.index[0] == self.pending_second:

                counts = counts.copy()
                counts.iloc[0] += self.pending_second_ticks

            else:

                self._record_second_counts(
                    pd.Series([self.pending_second_ticks])
                )

        self._record_second_counts(counts.iloc[:-1])

        self.pending_second = counts.index[-1]
        self.pending_second_ticks = int(counts.iloc[-1])

    def _finalize_tick_second_statistics(self):

        if self.pending_second is not None:

            self._record_second_counts(
                pd.Series([self.pending_second_ticks])
            )

            self.pending_second = None
            self.pending_second_ticks = 0

        if self.active_second_count:

            self.result.average_ticks_per_second = (
                self.total_second_ticks /
                self.active_second_count
            )

    # ==========================================================
    # Export Reports
    # ==========================================================

    def export_reports(self):

        report = self.result.to_dict()

        base = self.file_path.stem

        txt_file = REPORT_FOLDER / f"{base}_validation.txt"
        csv_file = REPORT_FOLDER / f"{base}_validation.csv"
        json_file = REPORT_FOLDER / f"{base}_validation.json"

        # TXT
        with open(txt_file, "w", encoding="utf-8") as f:

            f.write("=" * 60 + "\n")
            f.write("QUANTFORGE TICK VALIDATION REPORT\n")
            f.write("=" * 60 + "\n\n")

            for k, v in report.items():

                if isinstance(v, list):

                    f.write(f"{k}\n")

                    if len(v):

                        for item in v:
                            f.write(f"   {item}\n")

                    else:

                        f.write("   None\n")

                else:

                    f.write(f"{k:30}: {v}\n")

        # CSV

        pd.DataFrame([report]).to_csv(

            csv_file,

            index=False

        )

        # JSON

        with open(json_file, "w", encoding="utf-8") as f:

            json.dump(

                report,

                f,

                indent=4,

                default=str

            )

    # ==========================================================
    # Console Summary
    # ==========================================================

    def print_summary(self):

        r = self.result

        print()
        print("=" * 70)
        print("QUANTFORGE TICK VALIDATION REPORT")
        print("=" * 70)

        print(f"File                  : {r.file_name}")
        print(f"File Size (MB)        : {r.file_size_mb:.2f}")
        print(f"Rows                  : {r.total_rows:,}")

        print()

        print(f"First Tick            : {r.first_tick}")
        print(f"Last Tick             : {r.last_tick}")
        print(f"Coverage Days         : {r.coverage_days}")

        print()

        print(f"Backward Timestamps   : {r.backward_timestamps}")
        print(f"Duplicate Rows        : {r.duplicate_rows}")

        print()

        print(f"Invalid Timestamps    : {r.invalid_timestamps}")
        print(f"Invalid Numeric Rows  : {r.invalid_numeric_rows}")

        print()

        print(f"Largest Gap (sec)     : {r.largest_gap_seconds:.0f}")
        print(f"Weekend Gap           : {r.weekend_gap}")

        print()

        print(f"Negative Prices       : {r.negative_prices}")
        print(f"Zero Prices           : {r.zero_prices}")
        print(f"Ask < Bid             : {r.ask_less_than_bid}")

        print()

        print("Spread Statistics")
        print("------------------------------")

        print(f"Average               : {r.average_spread:.8f}")
        print(f"Median                : {r.median_spread:.8f}")
        print(f"95 Percentile         : {r.spread_95:.8f}")
        print(f"99 Percentile         : {r.spread_99:.8f}")
        print(f"Maximum               : {r.maximum_spread:.8f}")

        print()

        print("Tick Density (/Minute)")
        print("------------------------------")

        print(f"Average               : {r.average_ticks_per_minute:.2f}")
        print(f"Median                : {r.median_ticks_per_minute:.2f}")
        print(f"Minimum               : {r.min_ticks_per_minute}")
        print(f"Maximum               : {r.max_ticks_per_minute}")
        print(f"95 Percentile         : {r.tick95:.2f}")

        if r.quantiles_are_estimated:
            print(
                f"Quantile Sample       : {r.quantile_sample_size:,} values"
            )

        print()

        print("Tick Activity (/Second)")
        print("------------------------------")

        print(f"Multi-Tick Seconds    : {r.multi_tick_seconds:,}")
        print(f"Average               : {r.average_ticks_per_second:.2f}")
        print(f"Maximum               : {r.maximum_ticks_per_second}")

        print()

        print("Missing Trading Days")
        print("------------------------------")

        if len(r.missing_trading_days):

            print(f"Count : {len(r.missing_trading_days)}")

            preview = r.missing_trading_days[:10]

            for d in preview:

                print(" ", d)

            if len(r.missing_trading_days) > 10:

                print(" ...")

        else:

            print("None")

        print()

        if r.pass_validation:

            print("STATUS : PASS")

        else:

            print("STATUS : FAIL")

        print("=" * 70)
        
        # ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("QuantForge Framework")
    print("Tick Validator v1.1.0")
    print("=" * 60)
    print()

    validator = TickValidator(INPUT_FILE)

    result = validator.validate()

    print()
    print("=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)

    if result.pass_validation:
        print("Dataset Status : PASS")
    else:
        print("Dataset Status : FAIL")

    print()
    print("Reports Saved To")
    print("----------------")
    print(REPORT_FOLDER)

    print()
    print("Generated Files")
    print("----------------")
    print(f"{INPUT_FILE.stem}_validation.txt")
    print(f"{INPUT_FILE.stem}_validation.csv")
    print(f"{INPUT_FILE.stem}_validation.json")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
