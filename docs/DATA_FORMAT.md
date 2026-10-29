# Shared data format

Every collector writes the **same columns**. The dashboard and analysis notebooks only need to know this shape — not how each signal was fetched.

## Columns

| column | type | example |
|--------|------|---------|
| `date` | ISO date (`YYYY-MM-DD`) | `2026-10-22` |
| `ticker` | string, from `config/tickers.yaml` | `NVDA` |
| `signal` | string, snake_case | `close_price`, `wiki_pageviews` |
| `value` | float | `48211` |
| `source` | string | `yfinance`, `wikimedia` |

## Why “long / tidy” format?

One row = one measurement for one ticker on one date.

That means:

- Adding a new signal (e.g. `news_sentiment`) only means writing more rows — **no dashboard rewrite**.
- Filtering is easy: `signal == "wiki_pageviews"` or `ticker == "GS"`.
- Lead/lag analysis can join on `date` + `ticker` without reshaping wide tables.

## Agreed signal names (v1)

| signal | meaning | typical source |
|--------|---------|----------------|
| `close_price` | Daily closing price (USD) | `yfinance` |
| `wiki_pageviews` | Daily English Wikipedia views | `wikimedia` |
| `news_sentiment` | Daily headline sentiment score (later) | TBD |

## Example CSV (3 rows)

Also saved as `data/example_signals.csv`:

```csv
date,ticker,signal,value,source
2026-10-20,NVDA,wiki_pageviews,5277.0,wikimedia
2026-10-21,NVDA,wiki_pageviews,4992.0,wikimedia
2026-10-21,NVDA,close_price,185.42,yfinance
```

## Writing data from Python

Use the shared helper so every collector behaves the same:

```python
from common import load_tickers, write_rows

rows = [
    {
        "date": "2026-10-21",
        "ticker": "NVDA",
        "signal": "wiki_pageviews",
        "value": 4992.0,
        "source": "wikimedia",
    }
]
write_rows(rows, "wiki_pageviews")  # -> data/wiki_pageviews.csv
```

`write_rows` merges with any existing file and de-duplicates on `(date, ticker, signal)`, so re-running a collector is safe.
