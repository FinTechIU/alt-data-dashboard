"""
Framework-agnostic data loading for the dashboard.

Reads every CSV in data/ that uses the shared tidy format
(date, ticker, signal, value, source) and returns one combined table.

Why a separate module?
----------------------
Streamlit (or a future web app) should not care how CSVs were produced.
Collectors write files; this module only reads them.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
REQUIRED_COLUMNS = ["date", "ticker", "signal", "value", "source"]


def load_all_signals(data_dir: Path | None = None) -> pd.DataFrame:
    """
    Load and stack every shared-format CSV under data/.

    Skips example_signals.csv (demo rows mixed across signals) and any file
    that is missing required columns. Returns an empty DataFrame with the
    right columns when nothing usable is found.
    """
    folder = data_dir or DATA_DIR
    frames: list[pd.DataFrame] = []

    if not folder.exists():
        return _empty()

    for path in sorted(folder.glob("*.csv")):
        # Example file mixes signals for docs; skip so real signal files win.
        if path.name == "example_signals.csv":
            continue
        try:
            df = pd.read_csv(path)
        except Exception as exc:  # beginner-friendly: one bad file shouldn't crash UI
            print(f"Skipping {path.name}: {exc}")
            continue

        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            print(f"Skipping {path.name}: missing columns {missing}")
            continue

        piece = df[REQUIRED_COLUMNS].copy()
        piece["date"] = pd.to_datetime(piece["date"], errors="coerce")
        piece["value"] = pd.to_numeric(piece["value"], errors="coerce")
        piece = piece.dropna(subset=["date", "ticker", "signal", "value"])
        frames.append(piece)

    if not frames:
        return _empty()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.drop_duplicates(subset=["date", "ticker", "signal"], keep="last")
    return combined.sort_values(["ticker", "signal", "date"]).reset_index(drop=True)


def filter_series(
    df: pd.DataFrame,
    ticker: str,
    signal: str,
) -> pd.DataFrame:
    """Return rows for one ticker + signal, sorted by date (may be empty)."""
    if df.empty:
        return _empty()
    out = df[(df["ticker"] == ticker) & (df["signal"] == signal)].copy()
    return out.sort_values("date").reset_index(drop=True)


def available_tickers(df: pd.DataFrame) -> list[str]:
    """Unique tickers present in the loaded data (sorted)."""
    if df.empty:
        return []
    return sorted(df["ticker"].astype(str).unique().tolist())


def available_signals(df: pd.DataFrame, ticker: str | None = None) -> list[str]:
    """Unique signals, optionally for one ticker."""
    if df.empty:
        return []
    subset = df if ticker is None else df[df["ticker"] == ticker]
    if subset.empty:
        return []
    return sorted(subset["signal"].astype(str).unique().tolist())


def _empty() -> pd.DataFrame:
    return pd.DataFrame(columns=REQUIRED_COLUMNS)
