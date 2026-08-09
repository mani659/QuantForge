"""Validate MT5-derived M1 candle data before it enters QuantForge research."""

from __future__ import annotations

import csv
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

# Change this filename to validate another M1 dataset.
FILE_NAME = "USATECHIDXUSD_M1.csv"
INPUT_FILE = DATA_FOLDER / FILE_NAME

CHUNK_SIZE = 500_000
PREVIEW_LIMIT = 10

HEADERLESS_COLUMNS = [
    "date", "time", "open", "high", "low", "close",
    "tick_volume", "volume", "spread",
]

COLUMN_ALIASES = {
    "date": {"date"},
    "time": {"time"},
    "timestamp": {"timestamp", "datetime", "date_time", "date time"},
    "open": {"open", "o"},
    "high": {"high", "h"},
    "low": {"low", "l"},
    "close": {"close", "c"},
    "tick_volume": {"tick_volume", "tick volume", "tickvolume", "ticks"},
    "volume": {"volume", "real_volume", "real volume"},
}


def normalise_column_name(name: object) -> str:
    """Return a comparison-friendly version of a CSV column name."""

    return str(name).strip().lower().replace("-", "_")


class ValidationResult:
    """Serializable metrics produced by :class:`M1Validator`."""

    def __init__(self) -> None:
        self.file_name = ""
        self.file_size_mb = 0.0
        self.volume_column = ""

        self.total_candles = 0
        self.first_candle = None
        self.last_candle = None
        self.coverage_days = 0

        self.backward_timestamps = 0
        self.duplicate_candles = 0
        self.missing_candles = 0
        self.missing_candle_preview: list[str] = []

        self.invalid_timestamps = 0
        self.invalid_numeric_rows = 0
        self.negative_price_rows = 0
        self.zero_price_rows = 0
        self.ohlc_violations = 0

        self.average_volume = 0.0
        self.median_volume = 0.0
        self.maximum_volume = 0.0
        self.zero_volume_candles = 0

        self.average_range = 0.0
        self.median_range = 0.0
        self.range_95 = 0.0
        self.range_99 = 0.0
        self.maximum_range = 0.0

        self.pass_validation = True

    def to_dict(self) -> dict:
        """Return report-ready values with stable numeric precision."""

        report = self.__dict__.copy()
        for key in (
            "file_size_mb", "average_volume", "median_volume", "maximum_volume",
            "average_range", "median_range", "range_95", "range_99", "maximum_range",
        ):
            report[key] = round(report[key], 8)
        return report


class M1Validator:
    """Chunked validator for large MT5-derived one-minute candle CSV files."""

    def __init__(self, file_path: Path | str = INPUT_FILE) -> None:
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(self.file_path)

        self.result = ValidationResult()
        self.result.file_name = self.file_path.name
        self.result.file_size_mb = self.file_path.stat().st_size / (1024 * 1024)

        self.previous_timestamp: pd.Timestamp | None = None
        self.volume_chunks: list[np.ndarray] = []
        self.range_chunks: list[np.ndarray] = []

        self.csv_separator, self.read_options, self.column_map = self._detect_schema()
        self.result.volume_column = self.column_map["volume"]

    def _detect_schema(self) -> tuple[str, dict, dict[str, str]]:
        """Detect a common MT5 header format or fall back to the standard layout."""

        with self.file_path.open("r", encoding="utf-8-sig", newline="") as source:
            first_line = source.readline()

        separator = ";" if first_line.count(";") > first_line.count(",") else ","
        first_row = next(csv.reader([first_line], delimiter=separator), [])
        normalised = {normalise_column_name(column): column for column in first_row}

        column_map: dict[str, str] = {}
        for canonical, aliases in COLUMN_ALIASES.items():
            for alias in aliases:
                if alias in normalised:
                    column_map[canonical] = normalised[alias]
                    break

        headered = all(key in column_map for key in ("open", "high", "low", "close"))
        headered = headered and (
            "timestamp" in column_map or
            ("date" in column_map and "time" in column_map)
        )

        if not headered:
            column_map = {
                "date": "date", "time": "time", "open": "open", "high": "high",
                "low": "low", "close": "close", "volume": "tick_volume",
            }
            return separator, {"header": None, "names": HEADERLESS_COLUMNS}, column_map

        if "tick_volume" in column_map:
            column_map["volume"] = column_map["tick_volume"]
        elif "volume" not in column_map:
            raise ValueError("The candle file must include tick volume or volume.")

        return separator, {"header": 0}, column_map

    def _prepare_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """Parse timestamps and numeric fields, preserving invalid-row counts."""

        if "timestamp" in self.column_map:
            timestamp_text = chunk[self.column_map["timestamp"]].astype(str)
        else:
            timestamp_text = (
                chunk[self.column_map["date"]].astype(str) + " " +
                chunk[self.column_map["time"]].astype(str)
            )

        chunk = pd.DataFrame({
            "timestamp": pd.to_datetime(timestamp_text, errors="coerce"),
            "open": pd.to_numeric(chunk[self.column_map["open"]], errors="coerce"),
            "high": pd.to_numeric(chunk[self.column_map["high"]], errors="coerce"),
            "low": pd.to_numeric(chunk[self.column_map["low"]], errors="coerce"),
            "close": pd.to_numeric(chunk[self.column_map["close"]], errors="coerce"),
            "volume": pd.to_numeric(chunk[self.column_map["volume"]], errors="coerce"),
        })

        invalid_timestamp = chunk["timestamp"].isna()
        self.result.invalid_timestamps += int(invalid_timestamp.sum())
        return chunk.loc[~invalid_timestamp].copy()

    def _record_missing_minutes(
        self, previous: pd.Timestamp, current: pd.Timestamp
    ) -> None:
        """Count weekday minutes strictly between two chronologically ordered candles."""

        start = previous + pd.Timedelta(minutes=1)
        end = current - pd.Timedelta(minutes=1)

        while start.normalize() <= end.normalize():
            day_end = min(end, start.normalize() + pd.Timedelta(days=1) - pd.Timedelta(minutes=1))
            if start.weekday() < 5:
                minutes = int((day_end - start).total_seconds() // 60) + 1
                self.result.missing_candles += minutes

                remaining = PREVIEW_LIMIT - len(self.result.missing_candle_preview)
                if remaining > 0:
                    preview_end = min(day_end, start + pd.Timedelta(minutes=remaining - 1))
                    preview = pd.date_range(start, preview_end, freq="min")
                    self.result.missing_candle_preview.extend(
                        timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        for timestamp in preview
                    )
            start = start.normalize() + pd.Timedelta(days=1)

    def _validate_timestamps(self, timestamps: pd.Series) -> None:
        """Check order, duplicate minute stamps, and weekday gaps across chunks."""

        comparison = timestamps
        if self.previous_timestamp is not None:
            comparison = pd.concat(
                [pd.Series([self.previous_timestamp]), timestamps],
                ignore_index=True,
            )

        differences = comparison.diff().dt.total_seconds()
        self.result.backward_timestamps += int((differences < 0).sum())
        self.result.duplicate_candles += int((differences == 0).sum())

        gap_positions = np.flatnonzero((differences > 60).to_numpy())
        for position in gap_positions:
            self._record_missing_minutes(
                comparison.iloc[position - 1], comparison.iloc[position]
            )

        self.previous_timestamp = timestamps.iloc[-1]

    def validate(self) -> ValidationResult:
        """Run all M1 validations, export reports, and return the result."""

        print("=" * 60)
        print("QuantForge M1 Validator v1.0.0")
        print("=" * 60)
        print(f"File : {self.file_path.name}")
        print("Reading M1 Candle Data...")

        for raw_chunk in pd.read_csv(
            self.file_path,
            sep=self.csv_separator,
            chunksize=CHUNK_SIZE,
            **self.read_options,
        ):
            self.result.total_candles += len(raw_chunk)
            chunk = self._prepare_chunk(raw_chunk)
            if chunk.empty:
                continue

            numeric_columns = ["open", "high", "low", "close", "volume"]
            finite_rows = np.isfinite(chunk[numeric_columns]).all(axis=1)
            self.result.invalid_numeric_rows += int((~finite_rows).sum())
            chunk = chunk.loc[finite_rows].copy()
            if chunk.empty:
                continue

            if self.result.first_candle is None:
                self.result.first_candle = chunk.iloc[0]["timestamp"]
            self.result.last_candle = chunk.iloc[-1]["timestamp"]

            self._validate_timestamps(chunk["timestamp"])

            prices = chunk[["open", "high", "low", "close"]]
            self.result.negative_price_rows += int((prices < 0).any(axis=1).sum())
            self.result.zero_price_rows += int((prices == 0).any(axis=1).sum())

            ohlc_invalid = (
                (chunk["high"] < chunk["open"]) |
                (chunk["high"] < chunk["close"]) |
                (chunk["low"] > chunk["open"]) |
                (chunk["low"] > chunk["close"]) |
                (chunk["high"] < chunk["low"])
            )
            self.result.ohlc_violations += int(ohlc_invalid.sum())

            self.result.zero_volume_candles += int((chunk["volume"] == 0).sum())
            self.volume_chunks.append(chunk["volume"].to_numpy(dtype=np.float64, copy=True))
            self.range_chunks.append(
                (chunk["high"] - chunk["low"]).to_numpy(dtype=np.float64, copy=True)
            )

            print(f"Processed {self.result.total_candles:,} candles", end="\r")

        print()
        self._calculate_statistics()
        self._set_pass_fail_status()
        self.export_reports()
        self.print_summary()
        return self.result

    def _calculate_statistics(self) -> None:
        """Calculate exact volume and candle-range statistics after streamed parsing."""

        if self.result.first_candle is not None and self.result.last_candle is not None:
            self.result.coverage_days = (
                self.result.last_candle - self.result.first_candle
            ).days

        if self.volume_chunks:
            volume = np.concatenate(self.volume_chunks)
            self.result.average_volume = float(volume.mean())
            self.result.median_volume = float(np.median(volume))
            self.result.maximum_volume = float(volume.max())

        if self.range_chunks:
            candle_range = np.concatenate(self.range_chunks)
            self.result.average_range = float(candle_range.mean())
            self.result.median_range = float(np.median(candle_range))
            self.result.range_95 = float(np.percentile(candle_range, 95))
            self.result.range_99 = float(np.percentile(candle_range, 99))
            self.result.maximum_range = float(candle_range.max())

    def _set_pass_fail_status(self) -> None:
        """Apply the M1 validation rules; missing candles remain warnings."""

        failures = (
            self.result.backward_timestamps,
            self.result.duplicate_candles,
            self.result.ohlc_violations,
            self.result.invalid_timestamps,
            self.result.invalid_numeric_rows,
            self.result.negative_price_rows,
            self.result.zero_price_rows,
        )
        self.result.pass_validation = not any(failures)

    def export_reports(self) -> None:
        """Write TXT, CSV, and JSON validation reports into the project reports folder."""

        REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
        report = self.result.to_dict()
        base = self.file_path.stem

        txt_file = REPORT_FOLDER / f"{base}_m1_validation.txt"
        csv_file = REPORT_FOLDER / f"{base}_m1_validation.csv"
        json_file = REPORT_FOLDER / f"{base}_m1_validation.json"

        with txt_file.open("w", encoding="utf-8") as report_file:
            report_file.write("=" * 60 + "\n")
            report_file.write("QUANTFORGE M1 VALIDATION REPORT\n")
            report_file.write("=" * 60 + "\n\n")
            for key, value in report.items():
                if isinstance(value, list):
                    report_file.write(f"{key}:\n")
                    report_file.writelines(f"  {item}\n" for item in value)
                else:
                    report_file.write(f"{key}: {value}\n")

        pd.DataFrame([report]).to_csv(csv_file, index=False)
        with json_file.open("w", encoding="utf-8") as report_file:
            json.dump(report, report_file, indent=4, default=str)

    def print_summary(self) -> None:
        """Print the compact M1 validation report."""

        result = self.result
        print("\n" + "=" * 60)
        print("QUANTFORGE M1 VALIDATION REPORT")
        print("=" * 60)
        print(f"File                 : {result.file_name}")
        print(f"File Size (MB)       : {result.file_size_mb:.2f}")
        print(f"Volume Column        : {result.volume_column}")
        print(f"Candles              : {result.total_candles:,}")
        print(f"First Candle         : {result.first_candle}")
        print(f"Last Candle          : {result.last_candle}")
        print(f"Coverage Days        : {result.coverage_days}")
        print(f"Backward Timestamps  : {result.backward_timestamps}")
        print(f"Duplicate Candles    : {result.duplicate_candles}")
        print(f"Missing Candles      : {result.missing_candles:,} (warning)")
        print(f"Missing Preview      : {result.missing_candle_preview or 'None'}")
        print(f"Invalid Timestamps   : {result.invalid_timestamps}")
        print(f"Invalid Numeric Rows : {result.invalid_numeric_rows}")
        print(f"Negative Price Rows  : {result.negative_price_rows}")
        print(f"Zero Price Rows      : {result.zero_price_rows}")
        print(f"OHLC Violations      : {result.ohlc_violations}")
        print(f"Average Volume       : {result.average_volume:.2f}")
        print(f"Median Volume        : {result.median_volume:.2f}")
        print(f"Maximum Volume       : {result.maximum_volume:.2f}")
        print(f"Zero-Volume Candles  : {result.zero_volume_candles:,}")
        print(f"Average Range        : {result.average_range:.8f}")
        print(f"Median Range         : {result.median_range:.8f}")
        print(f"95% Range            : {result.range_95:.8f}")
        print(f"99% Range            : {result.range_99:.8f}")
        print(f"Maximum Range        : {result.maximum_range:.8f}")
        print("STATUS               : " + ("PASS" if result.pass_validation else "FAIL"))
        print("=" * 60)


def main() -> None:
    """Run validation for the configured M1 input file."""

    M1Validator(INPUT_FILE).validate()


if __name__ == "__main__":
    main()
