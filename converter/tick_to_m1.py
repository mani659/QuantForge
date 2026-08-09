"""Convert validated MT5 tick data into M1 OHLCV candles."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


# ==========================================================
# Project Configuration
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TICK_FOLDER = PROJECT_ROOT / "data" / "tick"
M1_FOLDER = PROJECT_ROOT / "data" / "m1"

# Change these settings to convert another symbol or price source.
TICK_FILE_NAME = "USATECHIDXUSD_mt5_ticks.csv"
M1_FILE_NAME = "USATECHIDXUSD_M1.csv"
PRICE_SOURCE = "bid"  # Supported values: bid, ask, last, mid

INPUT_FILE = TICK_FOLDER / TICK_FILE_NAME
OUTPUT_FILE = M1_FOLDER / M1_FILE_NAME

CHUNK_SIZE = 500_000
TICK_COLUMNS = ["date", "time", "bid", "ask", "last", "volume"]
NUMERIC_COLUMNS = ["bid", "ask", "last", "volume"]


class TickToM1Converter:
    """Stream a validated MT5 tick CSV into one-minute OHLCV candles."""

    def __init__(
        self,
        input_file: Path | str = INPUT_FILE,
        output_file: Path | str = OUTPUT_FILE,
        price_source: str = PRICE_SOURCE,
    ) -> None:
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.price_source = price_source.lower()

        if self.price_source not in {"bid", "ask", "last", "mid"}:
            raise ValueError(
                "PRICE_SOURCE must be one of: bid, ask, last, mid."
            )
        if not self.input_file.exists():
            raise FileNotFoundError(self.input_file)

        self.previous_timestamp: pd.Timestamp | None = None
        self.pending_bar: pd.DataFrame | None = None
        self.total_ticks = 0
        self.total_candles = 0
        self._has_written_output = False

    def _prepare_chunk(self, raw_chunk: pd.DataFrame) -> pd.DataFrame:
        """Parse and validate one source chunk before candle aggregation."""

        chunk = raw_chunk.copy()
        chunk[NUMERIC_COLUMNS] = chunk[NUMERIC_COLUMNS].apply(
            pd.to_numeric,
            errors="coerce",
        )
        chunk["timestamp"] = pd.to_datetime(
            chunk["date"] + " " + chunk["time"],
            format="%Y%m%d %H:%M:%S",
            errors="coerce",
        )

        invalid_timestamp = chunk["timestamp"].isna()
        invalid_numeric = ~np.isfinite(chunk[NUMERIC_COLUMNS]).all(axis=1)
        if invalid_timestamp.any() or invalid_numeric.any():
            raise ValueError(
                "The tick input contains invalid values. Run tick_validator.py "
                "and resolve its reported issues before conversion."
            )

        if self.price_source == "mid":
            chunk["price"] = (chunk["bid"] + chunk["ask"]) / 2
        else:
            chunk["price"] = chunk[self.price_source]

        comparison = chunk["timestamp"]
        if self.previous_timestamp is not None:
            comparison = pd.concat(
                [pd.Series([self.previous_timestamp]), comparison],
                ignore_index=True,
            )

        if (comparison.diff().dt.total_seconds() < 0).any():
            raise ValueError(
                "The tick input is not chronologically ordered. Run "
                "tick_validator.py and resolve backward timestamps first."
            )

        self.previous_timestamp = chunk.iloc[-1]["timestamp"]
        return chunk

    @staticmethod
    def _aggregate_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
        """Build one OHLCV bar per populated minute without empty-minute rows."""

        bars = chunk.groupby(
            chunk["timestamp"].dt.floor("min"),
            sort=False,
        ).agg(
            open=("price", "first"),
            high=("price", "max"),
            low=("price", "min"),
            close=("price", "last"),
            volume=("volume", "sum"),
        )
        bars.index.name = "timestamp"
        return bars

    @staticmethod
    def _merge_bars(previous: pd.DataFrame, current: pd.DataFrame) -> pd.DataFrame:
        """Merge two partial bars for the same minute in chronological order."""

        merged = previous.copy()
        merged.iloc[0, merged.columns.get_loc("high")] = max(
            previous.iloc[0]["high"], current.iloc[0]["high"]
        )
        merged.iloc[0, merged.columns.get_loc("low")] = min(
            previous.iloc[0]["low"], current.iloc[0]["low"]
        )
        merged.iloc[0, merged.columns.get_loc("close")] = current.iloc[0]["close"]
        merged.iloc[0, merged.columns.get_loc("volume")] = (
            previous.iloc[0]["volume"] + current.iloc[0]["volume"]
        )
        return merged

    def _write_bars(self, bars: pd.DataFrame, temporary_file: Path) -> None:
        """Append completed bars to the temporary output file."""

        if bars.empty:
            return

        bars.to_csv(
            temporary_file,
            mode="a",
            header=not self._has_written_output,
            index=True,
        )
        self._has_written_output = True
        self.total_candles += len(bars)

    def _process_bars(self, bars: pd.DataFrame, temporary_file: Path) -> None:
        """Write completed minutes and retain only the current final minute."""

        if self.pending_bar is not None:
            if bars.index[0] == self.pending_bar.index[0]:
                bars = bars.copy()
                bars.iloc[0] = self._merge_bars(
                    self.pending_bar,
                    bars.iloc[[0]],
                ).iloc[0]
            else:
                self._write_bars(self.pending_bar, temporary_file)

        self._write_bars(bars.iloc[:-1], temporary_file)
        self.pending_bar = bars.iloc[[-1]].copy()

    def convert(self) -> Path:
        """Convert the configured tick file and atomically publish the M1 CSV."""

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        temporary_file = self.output_file.with_suffix(
            self.output_file.suffix + ".tmp"
        )

        if temporary_file.exists():
            temporary_file.unlink()

        print("=" * 60)
        print("QuantForge Tick-to-M1 Converter v1.0.0")
        print("=" * 60)
        print(f"Input        : {self.input_file.name}")
        print(f"Output       : {self.output_file.name}")
        print(f"Price Source : {self.price_source}")
        print("Converting Tick Data...")

        try:
            for raw_chunk in pd.read_csv(
                self.input_file,
                names=TICK_COLUMNS,
                sep=r"\s+|,",
                engine="python",
                chunksize=CHUNK_SIZE,
                dtype={"date": str, "time": str},
            ):
                self.total_ticks += len(raw_chunk)
                chunk = self._prepare_chunk(raw_chunk)
                self._process_bars(self._aggregate_chunk(chunk), temporary_file)
                print(f"Processed {self.total_ticks:,} ticks", end="\r")

            if self.pending_bar is not None:
                self._write_bars(self.pending_bar, temporary_file)

            if not self._has_written_output:
                raise ValueError("The tick input did not contain any convertible rows.")

            temporary_file.replace(self.output_file)
        finally:
            if temporary_file.exists():
                temporary_file.unlink()

        print("\n" + "=" * 60)
        print("M1 CONVERSION COMPLETE")
        print("=" * 60)
        print(f"Ticks Processed : {self.total_ticks:,}")
        print(f"M1 Candles      : {self.total_candles:,}")
        print(f"Saved           : {self.output_file.relative_to(PROJECT_ROOT)}")
        print("=" * 60)
        return self.output_file


def main() -> None:
    """Convert the configured tick file into the configured M1 file."""

    TickToM1Converter().convert()


if __name__ == "__main__":
    main()
