"""
Generate realistic *fake* close_price rows for every ticker in config.

Why this exists
---------------
The prices collector is Ethan's + Justin's weekend task. Until real
data/close_price.csv exists, the dashboard still needs something to chart.
Fake rows use source="fake" so the UI can label them clearly.

Run from the repo root (optional — the Streamlit app can generate on the fly):

    python dashboard/fake_data.py
"""

from __future__ import annotations

import math
import random
import sys
from datetime import date, timedelta
from pathlib import Path

# Import shared helpers the same way collectors do.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "collectors"))

from common import load_tickers, write_rows  # noqa: E402

# Match collector history window. Short-history tickers start at listed_since.
HISTORY_START = date(2025, 1, 1)
HISTORY_END = date.today() - timedelta(days=1)

# Rough starting levels so charts look different per name (not real prices).
SEED_PRICES = {
    "GS": 480.0,
    "JPM": 220.0,
    "BLK": 900.0,
    "HOOD": 25.0,
    "COIN": 200.0,
    "PYPL": 70.0,
    "NVDA": 130.0,
    "SPCX": 90.0,
    "MSFT": 420.0,
    "AMD": 160.0,
    "KLAR": 40.0,
    "CAT": 350.0,
    "SOFI": 15.0,
    "RMD": 230.0,
}


def _parse_iso(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(str(value)[:10])


def _business_days(start: date, end: date) -> list[date]:
    """Weekdays only — markets are closed on weekends."""
    days: list[date] = []
    cur = start
    while cur <= end:
        if cur.weekday() < 5:
            days.append(cur)
        cur += timedelta(days=1)
    return days


def build_fake_close_rows(
    start: date = HISTORY_START,
    end: date = HISTORY_END,
    seed: int = 42,
) -> list[dict]:
    """
    Random-walk daily closes for all tickers in tickers.yaml.

    Respects listed_since so KLAR / SPCX do not get fake pre-IPO prices.
    """
    rng = random.Random(seed)
    rows: list[dict] = []

    for ticker in load_tickers():
        symbol = ticker["symbol"]
        listed = _parse_iso(ticker.get("listed_since"))
        series_start = max(start, listed) if listed else start
        if series_start > end:
            continue

        price = SEED_PRICES.get(symbol, 100.0)
        for d in _business_days(series_start, end):
            # Mild daily drift + noise; keep price positive.
            shock = rng.gauss(0.0005, 0.015)
            price = max(1.0, price * (1.0 + shock))
            # Tiny seasonal wiggle so charts aren't boring flat noise.
            wiggle = 1.0 + 0.01 * math.sin(d.toordinal() / 20.0)
            rows.append(
                {
                    "date": d.isoformat(),
                    "ticker": symbol,
                    "signal": "close_price",
                    "value": round(price * wiggle, 2),
                    "source": "fake",
                }
            )

    return rows


def main() -> None:
    rows = build_fake_close_rows()
    path = write_rows(rows, "close_price_fake")
    print(f"Fake prices ready at {path} (source=fake). Do not treat as real.")


if __name__ == "__main__":
    main()
