# Guide: prices collector (for Ethan & Justin)

This guide explains **what to build** in `collectors/prices.py`. It does **not** give you the finished code — that is your task. Pair on it; ask in the team chat when stuck.

Read these first:

1. [CONTRIBUTING.md](../CONTRIBUTING.md) — branch → PR → 1 review  
2. [DATA_FORMAT.md](DATA_FORMAT.md) — the CSV columns every collector must write  
3. `collectors/common.py` — helpers you should import (do not re-implement)

---

## 1. Environment setup

From your terminal:

```bash
# Clone (if you have not already) and enter the repo
git clone https://github.com/FinTechIU/alt-data-dashboard.git
cd alt-data-dashboard

# Create and activate a virtual environment (keeps packages separate)
python3 -m venv .venv
source .venv/bin/activate
# Windows (Command Prompt): .venv\Scripts\activate

# Install project packages
pip install -r requirements.txt
```

Quick sanity check that Python and packages work:

```bash
python -c "import yaml, pandas, yfinance, requests; print('ok')"
```

When you run `python collectors/prices.py`, the stub already adds the `collectors/` folder to `sys.path` so `from common import load_tickers, write_rows` works — same pattern as `wiki_pageviews.py`.

---

## 2. Git workflow (short version)

```bash
git checkout main
git pull
git checkout -b ethan-justin/prices-collector   # use your names / topic

# ... edit collectors/prices.py, test it ...

git add collectors/prices.py
git status   # make sure .env is NOT listed
git commit -m "Add daily close prices collector"
git push -u origin HEAD
```

Then open a **Pull Request** into `main` on GitHub. In the PR description, write how to run your script and what file it creates.

Someone else reviews and approves (1 approval). Do **not** push straight to `main`.

---

## 3. What `collectors/prices.py` must do

### Goal

For every ticker in `config/tickers.yaml`, download **daily closing prices** and save them with the shared helper.

### Required steps

1. **Import helpers** from `common.py`: `load_tickers` and `write_rows`.
2. **Call `load_tickers()`** — never hard-code `["GS", "JPM", ...]`. The list can change; config is the single source of truth.
3. **Fetch daily closes** for each ticker.
   - Suggested library: **`yfinance`** (already in `requirements.txt`).
   - Suggested history start: **`2025-01-01`**.
   - **SPCX** only started trading on **2026-06-12** (`listed_since` in the YAML). Expect missing rows before that date — that is normal, not a bug.
4. **Build a list of row dicts**, one per date per ticker:

   ```python
   {
       "date": "2026-10-21",      # YYYY-MM-DD string
       "ticker": "NVDA",          # from tickers.yaml symbol
       "signal": "close_price",   # exact name; do not invent another
       "value": 185.42,           # float close price
       "source": "yfinance",
   }
   ```

5. **Save with** `write_rows(rows, "close_price")`  
   That creates / updates `data/close_price.csv` and de-duplicates on `(date, ticker, signal)`.

### Important notes about `yfinance`

- It is **unofficial** and can rate-limit or break without notice.
- **Cache by writing to CSV** (the `write_rows` helper does that). Prefer re-using existing dates over re-downloading everything every time if you add that logic later.
- Do **not** loop aggressively (no tight `for` loops with zero delay across many symbols/dates). Be polite; a small `time.sleep` between tickers is fine.
- Finnhub is an optional fallback later if the team has a free API key — skip it for v1 unless you finish early.

---

## 4. Suggested function sketch (fill these in)

The stub in `collectors/prices.py` already has TODO comments that match this list:

1. `load_tickers()`
2. For each ticker, download history from `2025-01-01` (or from `listed_since` if you want to be fancy)
3. Turn each close into a row dict
4. `write_rows(all_rows, "close_price")`
5. Print how many rows you wrote / which file path

Keep functions **short** and add a one-line comment when something is non-obvious.

---

## 5. How to check your output

```bash
python collectors/prices.py
```

Then open `data/close_price.csv` and confirm:

- [ ] Header is exactly: `date,ticker,signal,value,source`
- [ ] `signal` is always `close_price`
- [ ] `source` is always `yfinance` (for this collector)
- [ ] Dates look like `2026-10-21` (not timestamps with hours)
- [ ] You see multiple tickers from the YAML (GS, JPM, …), not hard-coded leftovers
- [ ] SPCX rows (if any) start on or after `2026-06-12`

Compare against [DATA_FORMAT.md](DATA_FORMAT.md) and `data/example_signals.csv`.

---

## 6. Done when

- Running `python collectors/prices.py` from the repo root writes `data/close_price.csv`
- Tickers come only from `load_tickers()`
- Columns match the shared format
- PR opened with a short test note for the reviewer

Good luck — ask Kavi or the team chat if the imports / YAML path confuse you. That is a normal first hurdle, not a failure.
