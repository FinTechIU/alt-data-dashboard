# Alternative Data Dashboard

FinTech @ IU project: track a few **nontraditional signals** (news sentiment, Wikipedia attention, and more later) **next to stock prices** for companies the club follows. The goal is to explore whether attention, hiring, or sentiment tends to move before the market does.

This is a student club project with a short timeline. We prefer a **small, working version** over a large unfinished one.

## Who this is for

Club members who want to research signals, and anyone viewing the project as a public showcase / portfolio piece.

## First version (planned)

- About **8–10 tickers** (list lives in `config/tickers.yaml` — easy to change)
- Daily **stock prices**
- **News sentiment**
- **Wikipedia pageviews** (attention)

Frontend choice (Streamlit vs a web app) is still open. The data layer stays independent either way.

## Repo layout

```
alt-data-dashboard/
├── config/tickers.yaml     # companies we track (edit here)
├── collectors/             # one script per signal
├── data/                   # output tables (decision TBD: commit or store elsewhere)
├── analysis/               # notebooks / lead-lag experiments
├── dashboard/              # frontend (not locked in yet)
├── .env.example            # API key names only — copy to .env for real keys
├── CONTRIBUTING.md         # how to make changes
└── requirements.txt        # Python packages
```

### Shared data format

Every collector should write rows like this (one row per date + ticker + signal):

| column  | example           |
|---------|-------------------|
| date    | `2026-10-22`      |
| ticker  | `AAPL`            |
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

5. **Try a collector stub** (they print a placeholder until implemented):

   ```bash
   python collectors/prices.py
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
