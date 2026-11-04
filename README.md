# Alternative Data Dashboard

FinTech @ IU project: track a few **nontraditional signals** (news sentiment, Wikipedia attention, and more later) **next to stock prices** for companies the club follows. The goal is to explore whether attention, hiring, or sentiment tends to move before the market does.

This is a student club project with a short timeline. We prefer a **small, working version** over a large unfinished one.

## Who this is for

Club members who want to research signals, and anyone viewing the project as a public showcase / portfolio piece.

**Start here if you're new:**

- [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) — plain-language guide to each data source and why it might matter  
- [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md) — the shared CSV columns every collector writes  
- [TASKS.md](TASKS.md) — who is doing what  

(`Alt_Data_Simplified.md` redirects to `docs/DATA_SOURCES.md`.)

## First version (this week)

- **14 tickers** in `config/tickers.yaml` (may be trimmed later — edit that file only)
- Daily **stock prices** — Ethan + Justin (session Nov 7–8; see `docs/GUIDE_PRICES.md`)
- **Wikipedia pageviews** — Kavi (collector live)
- **Streamlit dashboard** — Kavi (prototype; fake prices until real closes exist)

## Repo layout

```
alt-data-dashboard/
├── config/tickers.yaml     # companies we track (edit here only)
├── collectors/             # one script per signal + common.py helpers
├── data/                   # shared-format CSVs (e.g. wiki_pageviews.csv)
├── docs/                   # DATA_SOURCES, DATA_FORMAT, GUIDE_PRICES, …
├── dashboard/              # Streamlit app + data loaders
├── analysis/               # notebooks / lead-lag experiments
├── .env.example            # API key names only — copy to .env for real keys
├── TASKS.md                # who is doing what
├── CONTRIBUTING.md         # how to make changes
└── requirements.txt        # Python packages
```

### Shared data format

Full spec: [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md). Short version — every collector writes:

| column  | example           |
|---------|-------------------|
| date    | `2026-10-22`      |
| ticker  | `NVDA`            |
| signal  | `wiki_pageviews`  |
| value   | `48211`           |
| source  | `wikimedia`       |

## Setup (local)

1. **Clone the repo** and open it in your terminal / editor.
2. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows (Command Prompt): `.venv\Scripts\activate`

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Optional API keys:** copy `.env.example` to `.env` and fill in values if a task needs them. Never commit `.env`.

5. **Run collectors / dashboard:**

   ```bash
   python collectors/wiki_pageviews.py   # attention signal → data/wiki_pageviews.csv
   python collectors/prices.py           # stub — see docs/GUIDE_PRICES.md
   streamlit run dashboard/app.py        # dashboard prototype
   ```

## Timeline

- Started: Oct 8, 2026  
- Target working v1: early next week (prices + wiki on the dashboard)  
- Presentation date: pending from Gabriel  

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md). Short version: work on a **branch**, open a **pull request**, get **one approval**, then merge. Do not push straight to `main`.

Work is listed in [TASKS.md](TASKS.md) (not GitHub Issues).

## License

MIT — see [LICENSE](LICENSE).
