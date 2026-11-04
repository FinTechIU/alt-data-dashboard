# Guide: prices collector (for Ethan & Justin)

This guide explains **what to build** in `collectors/prices.py`. It does **not** give you the finished code — that is your task. You are pairing on this over **Nov 7–8, 2026**. Ask in the team chat when stuck.

Read these first:

1. [CONTRIBUTING.md](../CONTRIBUTING.md) — branch → PR → 1 review  
2. [DATA_FORMAT.md](DATA_FORMAT.md) — the CSV columns every collector must write  
3. [DATA_SOURCES.md](DATA_SOURCES.md) — why prices matter next to alt signals  
4. `collectors/common.py` — helpers you should import (do not re-implement)

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
# If your run wrote data/close_price.csv and the team is committing data/, add that too:
# git add data/close_price.csv
git status   # make sure .env is NOT listed
git commit -m "Add daily close prices collector"
git push -u origin HEAD
```

Then open a **Pull Request** into `main` on GitHub. In the PR description, write how to run your script and what file it creates.

Someone else reviews and approves (1 approval). Do **not** push straight to `main`.

---

## 3. What `collectors/prices.py` must do

### Goal

For every ticker in `config/tickers.yaml` (**14 companies** right now), download **daily closing prices** and save them with the shared helper.

Current symbols (do **not** hard-code this list — always call `load_tickers()`):

`GS, JPM, BLK, HOOD, COIN, PYPL, NVDA, SPCX, MSFT, AMD, KLAR, CAT, SOFI, RMD`

### Required steps

1. **Import helpers** from `common.py`: `load_tickers` and `write_rows`.
2. **Call `load_tickers()`** — never hard-code symbols. The list can change; config is the single source of truth.
3. **Fetch daily closes** for each ticker.
   - Suggested library: **`yfinance`** (already in `requirements.txt`).
   - Suggested history start: **`2025-01-01`**.
   - **Short histories (normal, not bugs):**
     - **KLAR** (Klarna) listed **2025-09-10** → no rows before that
     - **SPCX** (SpaceX) listed **2026-06-12** → no rows before that  
     Do **not** invent zeros or forward-fill fake prices for missing dates. Skip missing days.
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
2. For each ticker, download history from `2025-01-01` (you may start at `listed_since` when present to avoid empty requests)
3. Turn each close into a row dict — **omit** dates with no real close
4. `write_rows(all_rows, "close_price")`
5. Print how many rows you wrote / which file path (and maybe how many tickers succeeded)

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
- [ ] You see all **14** tickers from the YAML (including KLAR, CAT, SOFI, RMD)
- [ ] **KLAR** rows (if any) start on or after `2025-09-10`
- [ ] **SPCX** rows (if any) start on or after `2026-06-12`
- [ ] No fake `0.0` prices for pre-IPO dates

Compare against [DATA_FORMAT.md](DATA_FORMAT.md) and `data/example_signals.csv`.

---

## 6. Done when

- Running `python collectors/prices.py` from the repo root writes `data/close_price.csv`
- Tickers come only from `load_tickers()`
- Columns match the shared format
- Short-history tickers do not crash the script
- PR opened with a short test note for the reviewer

Good luck — ask Kavi or the team chat if the imports / YAML path confuse you. That is a normal first hurdle, not a failure.
