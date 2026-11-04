"""
Collector: daily stock prices (close).

Reads tickers from config/tickers.yaml via load_tickers() and writes rows in
the shared data format (see docs/DATA_FORMAT.md).

This file is intentionally a STUB. Ethan Thang + Justin Brown are implementing
it (working session Nov 7–8, 2026). Follow docs/GUIDE_PRICES.md — explain,
don't paste a full solution here.

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
    #   Expect 14 companies (banks, fintech, tech, research_coverage).
    #   Each item has at least: symbol, name, group, wikipedia
    #   Short history (listed_since):
    #     KLAR -> "2025-09-10"
    #     SPCX -> "2026-06-12"

    # TODO 2: For each ticker, download daily close prices.
    #   Suggested library: yfinance
    #   Suggested start date: 2025-01-01
    #   Missing earlier dates for KLAR / SPCX is OK — do NOT invent zeros
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

    # TODO 5: Print a short summary (how many rows, which file, which
    #   tickers succeeded) so reviewers can tell the run worked.

    _ = (load_tickers, write_rows)  # keep imports used until you fill in TODOs
    print("prices collector: not implemented yet")
    print("See docs/GUIDE_PRICES.md for the step-by-step task.")
    print(f"Config currently has {len(load_tickers())} tickers.")


if __name__ == "__main__":
    main()
