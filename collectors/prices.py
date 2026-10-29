"""
Collector: daily stock prices (close).

Reads tickers from config/tickers.yaml via load_tickers() and writes rows in
the shared data format (see docs/DATA_FORMAT.md).

This file is intentionally a STUB. Ethan Thang + Justin Brown are implementing
it — follow docs/GUIDE_PRICES.md (explain, don't paste a full solution here).

Run from the repo root:
  python collectors/prices.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# So `from common import ...` works when running: python collectors/prices.py
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_tickers, write_rows  # noqa: E402


def main() -> None:
    # TODO 1: Load the ticker list. Do NOT hard-code symbols.
    #   tickers = load_tickers()
    #   Each item is a dict with at least: symbol, name, group, wikipedia
    #   SPCX may also have listed_since = "2026-06-12"

    # TODO 2: For each ticker, download daily close prices.
    #   Suggested library: yfinance
    #   Suggested start date: 2025-01-01
    #   SPCX only has history from 2026-06-12 — missing earlier dates is OK
    #   Be polite: small sleep between tickers; cache via CSV (write_rows)

    # TODO 3: Build a list of row dicts, one per date per ticker:
    #   {
    #       "date": "YYYY-MM-DD",
    #       "ticker": "NVDA",
    #       "signal": "close_price",
    #       "value": 185.42,
    #       "source": "yfinance",
    #   }

    # TODO 4: Save with the shared helper:
    #   write_rows(rows, "close_price")
    #   -> creates/updates data/close_price.csv

    # TODO 5: Print a short summary (how many rows, which file) so reviewers
    #   can tell the run worked without opening Python.

    _ = (load_tickers, write_rows)  # keep imports used until you fill in TODOs
    print("prices collector: not implemented yet")
    print("See docs/GUIDE_PRICES.md for the step-by-step task.")


if __name__ == "__main__":
    main()
