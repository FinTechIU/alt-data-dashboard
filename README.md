# Alternative Data Dashboard

FinTech @ IU project: track a few **nontraditional signals** (news sentiment, Wikipedia attention, and more later) **next to stock prices** for companies the club follows. The goal is to explore whether attention, hiring, or sentiment tends to move before the market does.

This is a student club project with a short timeline. We prefer a **small, working version** over a large unfinished one.

## Who this is for

Club members who want to research signals, and anyone viewing the project as a public showcase / portfolio piece.

New to alternative data? Start with [Alt_Data_Simplified.md](Alt_Data_Simplified.md) — plain-language explanation of each data source and why it might matter.

## First version (planned)

- **10 tickers** locked in `config/tickers.yaml` (may be trimmed later — edit that file only)
- Daily **stock prices** (`close_price`) — Ethan + Justin
- **Wikipedia pageviews** (`wiki_pageviews`) — Kavi
- **News sentiment** — unclaimed

Frontend choice (Streamlit vs a web app) is still open. The data layer stays independent either way.

## Repo layout

```
alt-data-dashboard/
├── config/tickers.yaml     # companies we track (edit here only)
├── collectors/             # one script per signal + common.py helpers
├── data/                   # shared-format CSVs (e.g. wiki_pageviews.csv)
├── docs/                   # DATA_FORMAT.md, GUIDE_PRICES.md, …
├── analysis/               # notebooks / lead-lag experiments
├── dashboard/              # frontend (not locked in yet)
├── Alt_Data_Simplified.md  # why each data source matters (plain language)
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

That way a new signal can be added without rewriting the dashboard.

## Setup (local)

1. **Clone the repo** and open it in your terminal / editor.
2. **Create a virtual environment** (keeps project packages separate from your system Python):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows (Command Prompt), activation looks like: `.venv\Scripts\activate`

3. **Install dependencies** (list will grow as we add collectors):

   ```bash
   pip install -r requirements.txt
   ```

4. **Optional API keys:** copy `.env.example` to `.env` and fill in values if a task needs them. Never commit `.env`.

5. **Try a collector:**

   ```bash
   python collectors/wiki_pageviews.py   # working attention signal
   python collectors/prices.py           # stub — see docs/GUIDE_PRICES.md
   ```

## Timeline

- Started: Oct 8, 2026  
- Target working version: ~mid-November 2026  
- Presentation: before end of fall semester  

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md). Short version: work on a **branch**, open a **pull request**, get **one approval**, then merge. Do not push straight to `main`.

Starter work is listed in [TASKS.md](TASKS.md) (a checklist in the repo — not GitHub Issues).

## License

MIT — see [LICENSE](LICENSE).
