# Contributing

Thanks for helping with the Alternative Data Dashboard. You do **not** need to know the whole codebase to contribute. Most work is small and isolated (one collector script, one notebook, one dashboard page).

If you get stuck, ask in the team chat. There are no dumb questions.

## Golden rules

1. **Never push straight to `main`.** Always use a branch + pull request.
2. **Never commit secrets.** Put keys in a local `.env` file (gitignored). Document key *names* in `.env.example` only.
3. **Keep changes small.** One PR = one clear task when you can.
4. **Read tickers from `config/tickers.yaml`.** Do not hard-code company lists in scripts.
5. **Respect data source rules** (rate limits, terms of use). Do not scrape around blocked APIs.

## How to make a change (step by step)

### 1. Update your local copy

```bash
git checkout main
git pull
```

### 2. Create a branch

Name it after what you are doing, for example:

```bash
git checkout -b add-wiki-pageviews
```

Good names: `fix-prices-cache`, `docs-readme-setup`, `proto-dashboard-fake-data`

### 3. Make your changes

- Prefer one folder / one script for your task.
- Add a short docstring at the top of new Python files explaining what the file does and how to run it.
- If you add a Python package, add it to `requirements.txt`.

### 4. Commit

```bash
git add .
git status          # double-check you are not adding .env or secrets
git commit -m "Add Wikipedia pageviews collector stub"
```

Write a short commit message that says **what** you did.

### 5. Push your branch and open a pull request

```bash
git push -u origin HEAD
```

Then on GitHub: open a **Pull Request** into `main`.

In the PR description, write:

- What you changed
- How to test it (commands or clicks)

### 6. Get one review

Someone else on the team should approve. After approval, merge the PR (or ask the coordinator if you are unsure).

## Shared data format (important)

If your work writes data, use these columns:

| column | meaning |
|--------|---------|
| `date` | ISO date, e.g. `2026-10-22` |
| `ticker` | e.g. `AAPL` |
| `signal` | name of the signal, e.g. `wiki_pageviews` |
| `value` | numeric value |
| `source` | where it came from, e.g. `wikimedia` |

Ask before inventing a different shape — the whole project depends on this staying consistent.

## Good first tasks

See [TASKS.md](TASKS.md) for the starter checklist. Claim a task in the team chat (or put your name in that file) so two people do not do the same work.

Beginner-friendly areas:

- Research / clean ticker metadata
- Validate output CSVs
- Notebooks in `analysis/`
- Docs and presentation drafts

## Questions?

- **Code / “how do I…?”** → team chat or a PR comment  
- **Scope / “should we build X?”** → ask Kavi (coordinator) or Gabriel (Director of Technology) for bigger product questions  
