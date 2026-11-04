"""
Streamlit dashboard prototype.

First page: pick a ticker → close price on top, Wikipedia pageviews below,
aligned by date. Fake prices are labeled clearly until Ethan + Justin land
real close_price data.

Run from the repo root:
  streamlit run dashboard/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow importing collectors.common for the ticker dropdown labels.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "collectors"))
sys.path.insert(0, str(REPO_ROOT / "dashboard"))

from common import load_tickers  # noqa: E402
from data import filter_series, load_all_signals  # noqa: E402
from fake_data import build_fake_close_rows  # noqa: E402

st.set_page_config(page_title="FinTech @ IU — Alt Data", layout="wide")


@st.cache_data(show_spinner=False)
def _cached_tickers() -> list[dict]:
    return load_tickers()


@st.cache_data(show_spinner=False)
def _cached_signals() -> pd.DataFrame:
    """Combine real CSVs with in-memory fake prices when real closes are missing."""
    real = load_all_signals()
    has_real_closes = (
        not real.empty
        and ((real["signal"] == "close_price") & (real["source"] != "fake")).any()
    )

    if has_real_closes:
        return real

    # No real prices yet: merge wiki (and anything else) with generated fakes.
    fake_rows = build_fake_close_rows()
    fake_df = pd.DataFrame(fake_rows)
    fake_df["date"] = pd.to_datetime(fake_df["date"])
    if real.empty:
        return fake_df
    return pd.concat([real, fake_df], ignore_index=True)


def _chart_or_empty(series: pd.DataFrame, title: str, y_label: str) -> None:
    st.subheader(title)
    if series.empty:
        st.info("No data yet for this ticker / signal.")
        return
    plot_df = series.set_index("date")[["value"]].rename(columns={"value": y_label})
    st.line_chart(plot_df, height=280)


def main() -> None:
    st.title("Alternative Data Dashboard")
    st.caption("FinTech @ IU — prices beside attention signals (prototype)")

    tickers = _cached_tickers()
    labels = {
        t["symbol"]: f"{t['symbol']} — {t['name']}"
        + ("  (research)" if t.get("group") == "research_coverage" else "")
        for t in tickers
    }
    symbols = [t["symbol"] for t in tickers]

    df = _cached_signals()

    using_fake = (
        not df.empty
        and ((df["signal"] == "close_price") & (df["source"] == "fake")).any()
        and not ((df["signal"] == "close_price") & (df["source"] != "fake")).any()
    )
    if using_fake:
        st.warning(
            "**Fake prices** are shown until the real prices collector lands "
            "(Ethan + Justin). Wikipedia pageviews below are real when present."
        )

    choice = st.selectbox("Company", symbols, format_func=lambda s: labels.get(s, s))
    meta = next((t for t in tickers if t["symbol"] == choice), {})
    if meta.get("listed_since"):
        st.caption(
            f"Listed since {meta['listed_since']} — earlier dates intentionally empty "
            "(short history, not a bug)."
        )

    prices = filter_series(df, choice, "close_price")
    wiki = filter_series(df, choice, "wiki_pageviews")

    _chart_or_empty(prices, "Close price", "Close ($)")
    if not prices.empty:
        src = ", ".join(sorted(prices["source"].astype(str).unique()))
        st.caption(f"Price source: `{src}`")

    _chart_or_empty(wiki, "Wikipedia pageviews (attention)", "Pageviews")
    if not wiki.empty:
        st.caption("Pageviews source: `wikimedia`")


if __name__ == "__main__":
    main()
