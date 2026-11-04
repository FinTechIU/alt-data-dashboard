# Team tasks (updated Nov 3, 2026)

Claim work in the **team chat** (or put your name below). We use this file instead of GitHub Issues to avoid notification noise for the wider org.

Workflow reminder: **branch → PR → 1 review**. Do not push straight to `main`.

**Target:** working v1 (prices + Wikipedia pageviews on a basic dashboard) by **early next week**. Presentation date still pending from Gabriel.

---

## Status overview

| Status | Task | Owner |
|--------|------|--------|
| ✅ | Ticker list: **14** (incl. research-group companies) | Team + Gabriel |
| ✅ | Shared data format (`docs/DATA_FORMAT.md`) | — |
| ✅ | Data sources guide (`docs/DATA_SOURCES.md`) | — |
| ✅ | Shared helpers (`collectors/common.py`) | — |
| 🔄 | Prices collector (`collectors/prices.py`) | **Ethan + Justin** — session **Nov 7–8**; see `docs/GUIDE_PRICES.md` |
| 🔄 | Wikipedia pageviews collector | **Kavi** |
| 🔄 | Dashboard prototype (Streamlit) | **Kavi** |
| ⬜ | News sentiment collector | Next after v1 (Kavi interested) |
| ⬜ | Lead/lag analysis | Ethan interested (after prices) |
| ⬜ | Company-specific signals for 2–3 featured names | Later (candidates: COIN/HOOD, NVDA, research-group names) |
| ⬜ | Job postings / app ranking snapshots | Stretch |
| ⬜ | Reddit / Google Trends | On hold — need approval |

**Ava Donaldson** and **Ricky Rivas** — no tasks claimed yet. Good first options:

- Check collector CSV output against `docs/DATA_FORMAT.md`
- Research one research-group company (KLAR, CAT, SOFI, or RMD) for likely signals
- Help verify dashboard charts look sane once prices land

---

## Details

### ✅ Ticker list (14)

`GS, JPM, BLK, HOOD, COIN, PYPL, NVDA, SPCX, MSFT, AMD, KLAR, CAT, SOFI, RMD`

- Edit **only** `config/tickers.yaml`.
- `group: research_coverage` = companies club research groups follow (from Gabriel).
- Short histories (no fake zeros): **KLAR** from **2025-09-10**, **SPCX** from **2026-06-12**.

### 🔄 Prices — Ethan + Justin (Nov 7–8)

- Implement the stub; follow **`docs/GUIDE_PRICES.md`**.
- Justin is newer to Python — pair and keep code short/commented.

### 🔄 Wikipedia pageviews — Kavi

- `python collectors/wiki_pageviews.py` → `data/wiki_pageviews.csv`

### 🔄 Dashboard prototype — Kavi (Streamlit)

```bash
streamlit run dashboard/app.py
```

- Uses real wiki pageviews when present; **fake prices** until the prices PR merges.
- Framework choice for v1: **Streamlit** (fastest for a beginner team). Can revisit later.

### ⬜ After v1

1. Merge prices PR → swap fake prices for real ones.
2. News sentiment (FinBERT).
3. Lead/lag view.
4. Featured-company story for the presentation.
5. Deploy / link from `ft-iu-site` (decide with Gabriel).
