# Starter tasks

Team checklist for the first version. **Claim a task in the team chat** (or edit this file and put your name next to it) so two people do not do the same work.

These are **not** GitHub Issues on purpose — we keep planning here to avoid noisy notifications for the wider org.

---

## 1. Pull daily prices for the tracked tickers

**Goal:** Implement `collectors/prices.py` so it pulls daily closing prices for every ticker in `config/tickers.yaml`.

**Why:** Prices are the baseline every other signal sits next to.

**Suggested approach:**
- Read tickers from `config/tickers.yaml`
- Fetch daily closes (start with `yfinance`; Finnhub optional later)
- Cache results under `data/`
- Write the shared format: `date, ticker, signal, value, source`

**Done when:**
- [ ] `python collectors/prices.py` writes a file under `data/`
- [ ] Output uses the shared columns
- [ ] Tickers come from config (not hard-coded)

**Claimed by:** _nobody yet_

---

## 2. Define and document the shared data format

**Goal:** Short team reference for the tidy columns, plus a tiny example CSV.

**Shared format (starting point):**

| column | type | example |
|--------|------|---------|
| date | ISO date | 2026-10-22 |
| ticker | string | AAPL |
| signal | string | wiki_pageviews |
| value | float | 48211 |
| source | string | wikimedia |

**Done when:**
- [ ] README (or a short doc) explains the format with examples
- [ ] Example file in `data/` (e.g. `data/example_signals.csv`) with a few fake rows
- [ ] Agreed signal name strings for v1 (`price`, `news_sentiment`, `wiki_pageviews`, …)

**Claimed by:** _nobody yet_

---

## 3. Prototype one collector (news sentiment **or** Wikipedia pageviews)

**Goal:** Working prototype of either `collectors/news_sentiment.py` or `collectors/wiki_pageviews.py`.

**Why:** We need at least one alternative signal next to price for the first demo.

**Options:**
1. Wikipedia pageviews — Wikimedia API, free, “attention” signal
2. News sentiment — e.g. GDELT + a simple score (FinBERT later if time)

**Done when:**
- [ ] Reads tickers from config
- [ ] Writes shared columns
- [ ] Runnable as `python collectors/<name>.py`
- [ ] Short note in the PR/README on how to run it

**Do not** scrape Reddit or Google Trends for v1 (stretch only).

**Claimed by:** _nobody yet_

---

## 4. Prototype a dashboard page with fake data

**Goal:** Tiny page that charts price vs one signal using **fake/sample data**.

**Why:** Lets us try Streamlit vs a web app with something visible before locking in.

**Done when:**
- [ ] One page: ticker + price series + one fake signal
- [ ] README note on how to run locally
- [ ] Uses shared column names so real CSVs can drop in later
- [ ] Treated as a prototype (not a final frontend decision)

**Claimed by:** _nobody yet_

---

## 5. Draft the lead/lag analysis method

**Goal:** Notebook or short doc asking: does a signal move before price?

**Suggested approach:**
- Align signal values and returns by date
- Lagged correlations: signal at t vs return at t+1 … t+k
- Show a table/chart; note limitations (noise, correlation ≠ causation)

**Done when:**
- [ ] Something in `analysis/` a teammate can open and follow
- [ ] Works on the shared format / example CSV
- [ ] Explains the output in plain language

**Claimed by:** _nobody yet_

---

## 6. Start daily snapshots for job postings / app rankings

**Goal:** If we want these later, start saving dated snapshots early (little free history).

**Lower priority** than price + one attention/sentiment signal.

**Done when:**
- [ ] Document which free source(s) are realistic
- [ ] Small script that saves a dated snapshot under `data/`
- [ ] Notes on rate limits / terms of use

**Claimed by:** _nobody yet_
