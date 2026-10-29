# Team tasks (updated Oct 29, 2026)

Claim work in the **team chat** (or put your name below). We use this file instead of GitHub Issues to avoid notification noise for the wider org.

Workflow reminder: **branch → PR → 1 review**. Do not push straight to `main`.

---

## Status overview

| Status | Task | Owner |
|--------|------|--------|
| ✅ | Ticker list locked (10 names in `config/tickers.yaml`) | Team |
| ✅ | Shared data format documented (`docs/DATA_FORMAT.md`) | — |
| ✅ | Shared helpers (`collectors/common.py`) | — |
| 🔄 | Prices collector (`collectors/prices.py`) | **Ethan Thang** + **Justin Brown** — see `docs/GUIDE_PRICES.md` |
| 🔄 | Wikipedia pageviews collector (`collectors/wiki_pageviews.py`) | **Kavi** (+ partner TBD) |
| ⬜ | News sentiment collector | Unclaimed (Kavi interested) |
| ⬜ | Dashboard prototype with fake data | Unclaimed — frontend not decided (Streamlit vs web app) |
| ⬜ | Lead/lag analysis method | Ethan interested (after prices) |
| ⬜ | Daily snapshots for job postings / app rankings | Unclaimed (stretch) |
| ⬜ | Reddit / Google Trends access applications | Stretch — both need approval |

**Ava Donaldson** and **Ricky Rivas** have not claimed tasks yet. Good first options:

- Dashboard prototype with fake data
- Helping verify collector CSV output against `docs/DATA_FORMAT.md`
- Research / cleanup of company metadata

---

## Details

### ✅ Ticker list (locked)

`GS, JPM, BLK, HOOD, COIN, PYPL, NVDA, SPCX, MSFT, AMD`

- Edit **only** `config/tickers.yaml` — no hard-coded ticker lists in scripts.
- SPCX listed on Nasdaq **2026-06-12** (shorter price history; not a placeholder).
- List may be trimmed later; keep everything config-driven.

### 🔄 Prices collector — Ethan + Justin

- Implement `collectors/prices.py` using `load_tickers()` + `write_rows(..., "close_price")`.
- Follow **`docs/GUIDE_PRICES.md`** (explains the task without giving the full solution).
- Justin is newer to Python — pair and keep the code short/commented.

### 🔄 Wikipedia pageviews — Kavi (+ partner TBD)

- `collectors/wiki_pageviews.py` pulls daily `all-access` / `user` views from Wikimedia.
- Output: `data/wiki_pageviews.csv` with `signal=wiki_pageviews`, `source=wikimedia`.

### ⬜ News sentiment (unclaimed)

- Likely GDELT + a simple score; FinBERT later if time/budget.
- Same shared CSV format as other collectors.

### ⬜ Dashboard with fake data (unclaimed)

- One page: price vs one signal using sample rows.
- Do **not** lock the team into Streamlit vs a web app yet — treat as a prototype.

### ⬜ Lead/lag analysis (after prices)

- Align signal vs returns; lagged correlations; honest about noise.
- Natural follow-on for Ethan once `close_price` exists.

### ⬜ Stretch

- Job postings / app ranking **daily snapshots** (little free history — start early if we care).
- Reddit API and Google Trends access both need approval — do not scrape around them.
