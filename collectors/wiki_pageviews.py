"""
Collector: Wikipedia pageviews (attention signal).

For each company in config/tickers.yaml, download daily English Wikipedia
pageviews and write them in the shared tidy format.

API (Wikimedia Analytics / pageviews per article):
  https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/
      {project}/{access}/{agent}/{article}/{granularity}/{start}/{end}

We use: en.wikipedia / all-access / user / daily

Run from the repo root:
  python collectors/wiki_pageviews.py
"""

from __future__ import annotations

import sys
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

import requests

# So `from common import ...` works when running: python collectors/wiki_pageviews.py
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_tickers, write_rows  # noqa: E402

# --- Config -----------------------------------------------------------------
# How far back to pull. Same default window as the prices guide so charts line up.
START_DATE = date(2025, 1, 1)

# Wikimedia often lags ~1 day; yesterday is safer than "today".
END_DATE = date.today() - timedelta(days=1)

# Be polite: pause between tickers so we do not hammer the free API.
SLEEP_SECONDS = 0.25

# Wikimedia requires a descriptive User-Agent with a way to contact the project.
USER_AGENT = (
    "FinTechIU-alt-data-dashboard/0.1 "
    "(https://github.com/FinTechIU/alt-data-dashboard; FinTech @ IU student club)"
)

API_TEMPLATE = (
    "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    "en.wikipedia/all-access/user/{article}/daily/{start}/{end}"
)

SIGNAL_NAME = "wiki_pageviews"
SOURCE_NAME = "wikimedia"


def _ymd_compact(d: date) -> str:
    """Format a date as YYYYMMDD for the pageviews API path."""
    return d.strftime("%Y%m%d")


def _timestamp_to_iso(timestamp: str) -> str:
    """
    Convert API timestamps like '2026102100' to '2026-10-21'.

    The trailing '00' is an hour placeholder on daily granularity.
    """
    day = timestamp[:8]
    return f"{day[0:4]}-{day[4:6]}-{day[6:8]}"


def fetch_pageviews(article_title: str, start: date, end: date) -> list[dict]:
    """
    Call the Wikimedia pageviews API for one article.

    Returns a list of {"date": ISO, "views": int} dicts.
    Raises requests.HTTPError on hard failures (caller may catch per ticker).
    """
    # Article titles in our YAML use underscores (Goldman_Sachs). The API
    # accepts that; quote() keeps odd characters safe without turning "_" into %xx.
    encoded = quote(article_title, safe="_")
    url = API_TEMPLATE.format(
        article=encoded,
        start=_ymd_compact(start),
        end=_ymd_compact(end),
    )

    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    rows: list[dict] = []
    for item in payload.get("items", []):
        rows.append(
            {
                "date": _timestamp_to_iso(str(item["timestamp"])),
                "views": float(item["views"]),
            }
        )
    return rows


def collect_all() -> list[dict]:
    """
    Walk every ticker, fetch pageviews, and build shared-format rows.

    Errors are logged per ticker so one bad article does not stop the run.
    """
    tickers = load_tickers()
    all_rows: list[dict] = []

    for i, ticker in enumerate(tickers):
        symbol = ticker["symbol"]
        article = ticker.get("wikipedia")
        if not article:
            print(f"Skipping {symbol}: no wikipedia title in tickers.yaml")
            continue

        print(f"Fetching pageviews for {symbol} ({article})...")
        try:
            daily = fetch_pageviews(article, START_DATE, END_DATE)
        except requests.HTTPError as exc:
            # 404 usually means the title is wrong or has no views in range.
            print(f"  ERROR for {symbol}: {exc}")
            continue
        except requests.RequestException as exc:
            print(f"  NETWORK ERROR for {symbol}: {exc}")
            continue

        for day in daily:
            all_rows.append(
                {
                    "date": day["date"],
                    "ticker": symbol,
                    "signal": SIGNAL_NAME,
                    "value": day["views"],
                    "source": SOURCE_NAME,
                }
            )
        print(f"  got {len(daily)} days")

        # Sleep after each request except the last one.
        if i < len(tickers) - 1:
            time.sleep(SLEEP_SECONDS)

    return all_rows


def main() -> None:
    rows = collect_all()
    if not rows:
        print("No rows collected — check errors above and wikipedia titles.")
        return

    out_path = write_rows(rows, SIGNAL_NAME)
    print(f"Done. Open {out_path} and confirm columns match docs/DATA_FORMAT.md.")


if __name__ == "__main__":
    main()
