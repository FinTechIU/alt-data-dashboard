"""
Shared helpers for every collector.

Why this file exists
--------------------
Beginners (and future-you) should not copy-paste the same YAML / CSV logic
into every script. Import these helpers instead:

    from common import load_tickers, write_rows

Run collectors from the **repo root**, for example:

    python collectors/wiki_pageviews.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

# Repo root = parent of the collectors/ folder.
REPO_ROOT = Path(__file__).resolve().parents[1]
TICKERS_PATH = REPO_ROOT / "config" / "tickers.yaml"
DATA_DIR = REPO_ROOT / "data"

# Columns every collector must write. Keep this list in sync with docs/DATA_FORMAT.md.
REQUIRED_COLUMNS = ["date", "ticker", "signal", "value", "source"]


def load_tickers() -> list[dict]:
    """
    Read config/tickers.yaml and return a list of ticker dicts.

    Each dict has at least: symbol, name, group, wikipedia.
    Some rows may also have listed_since (ISO date string).
    """
    with TICKERS_PATH.open(encoding="utf-8") as f:
        payload = yaml.safe_load(f)

    tickers = payload.get("tickers") if isinstance(payload, dict) else None
    if not tickers:
        raise ValueError(f"No tickers found in {TICKERS_PATH}")

    # YAML may turn bare dates into datetime.date; keep strings for beginners.
    cleaned: list[dict] = []
    for row in tickers:
        item = dict(row)
        if "listed_since" in item and item["listed_since"] is not None:
            item["listed_since"] = str(item["listed_since"])
        cleaned.append(item)
    return cleaned


def write_rows(rows: list[dict], signal_name: str) -> Path:
    """
    Write rows to data/<signal_name>.csv in the shared tidy format.

    Re-runs are safe: we merge with any existing file and keep one row per
    (date, ticker, signal). Newer rows win when there is a duplicate.

    Parameters
    ----------
    rows:
        List of dicts with keys date, ticker, signal, value, source.
    signal_name:
        Used for the output filename, e.g. "close_price" -> data/close_price.csv

    Returns
    -------
    Path to the CSV that was written.
    """
    if not rows:
        raise ValueError("write_rows received no rows — nothing to save.")

    new_df = pd.DataFrame(rows)

    missing = [c for c in REQUIRED_COLUMNS if c not in new_df.columns]
    if missing:
        raise ValueError(f"Rows are missing required columns: {missing}")

    # Keep only the shared columns, in a stable order.
    new_df = new_df[REQUIRED_COLUMNS].copy()
    new_df["date"] = new_df["date"].astype(str)
    new_df["value"] = pd.to_numeric(new_df["value"], errors="coerce")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DATA_DIR / f"{signal_name}.csv"

    if out_path.exists():
        old_df = pd.read_csv(out_path)
        # Older files might have extra columns; keep only the shared ones.
        old_df = old_df[[c for c in REQUIRED_COLUMNS if c in old_df.columns]]
        combined = pd.concat([old_df, new_df], ignore_index=True)
    else:
        combined = new_df

    # Last occurrence wins so a re-run can refresh values for the same day.
    combined = combined.drop_duplicates(subset=["date", "ticker", "signal"], keep="last")
    combined = combined.sort_values(["ticker", "date"]).reset_index(drop=True)
    combined.to_csv(out_path, index=False)

    print(f"Wrote {len(combined)} rows to {out_path}")
    return out_path
