# Data Sources: What We Track and Why

This page explains, in plain language, every data source the dashboard uses or might use: what it measures, why it could matter for a stock, how we get it, and what it *can't* tell us.

If you're new to the project, start here. You don't need to understand the code to understand the idea.

---

## The big idea

A stock price reflects what investors think a company is worth. Before investors react, other things often change first:

- **Attention:** more people start looking a company up.
- **Sentiment:** news coverage turns more positive or negative.
- **Activity:** the company hires more, or more people download its app.

These are called **alternative data**: signals that aren't in a company's financial statements. Our dashboard puts these signals next to the stock price so we can ask one question:

> **Does the signal move *before* the price does?**

If it does, consistently, that's interesting. If it doesn't, that's also a real finding.

---

## Quick summary

| Source | Measures | Status | Cost |
|---|---|---|---|
| Stock prices | What the market thinks | ✅ Building now | Free |
| Wikipedia pageviews | Public attention | ✅ Building now | Free |
| News sentiment | Tone of coverage | ⬜ Next up | Free |
| SEC filings | Official company events | ⬜ Optional | Free |
| Job postings | Company growth plans | ⬜ Stretch | Free, no history |
| App rankings | Customer engagement | ⬜ Stretch | Free, no history |
| Reddit | Retail investor chatter | ⏸ Needs approval | Free if approved |
| Google Trends | Search interest | ⏸ Needs approval | Unclear |
| Web traffic | Site visitors | ❌ Skipped | Paid only |

---

## 1. Stock prices (the baseline)

**What it is:** each company's daily closing price.

**Why it matters:** this is what everything else is compared against. Without prices there's nothing to "lead."

**How we get it:** `yfinance`, a free Python library that reads Yahoo Finance data. No key needed.

**Keep in mind:**
- `yfinance` is unofficial and can break or slow down if we send too many requests. We download once a day and save results.
- **SpaceX (SPCX)** only started trading on June 12, 2026, so its chart will be shorter than the others.

---

## 2. Wikipedia pageviews (attention)

**What it is:** how many people viewed each company's Wikipedia article each day. Wikimedia, the nonprofit that runs Wikipedia, publishes these totals for free. No personal data is involved.

**Why it matters:** when people suddenly look up a company, something is usually happening: news, hype, a scandal, or retail investors getting curious. Pageviews are a simple measure of **how much attention** a company is getting.

**How we get it:** Wikimedia's official pageviews API. Each company's article title is stored in `config/tickers.yaml` (e.g. `NVDA` → `Nvidia`).

**Keep in mind:**
- It shows *how much* attention, not whether it's good or bad. That's what news sentiment adds.
- Spikes can have nothing to do with the stock (e.g. SpaceX launch days).
- Big companies always get steady traffic, so **sudden changes** matter more than the raw number.

---

## 3. News sentiment (tone)

**What it is:** a score for whether news headlines about a company are positive, negative, or neutral, averaged per day.

**Why it matters:** markets react to news. If coverage turns negative a day or two before the price drops, that's exactly the pattern we're looking for.

**How we get it:** collect headlines from a free news source (such as GDELT), then score each one with a sentiment model. FinBERT is a free model trained on financial text; an LLM is an option if we get a budget.

**Keep in mind:**
- Headlines are short and sometimes misleading, so scores are noisy.
- We store **scores**, not the article text, because the repo is public.

---

## 4. SEC filings (official events), optional

**What it is:** documents companies must file with the government, such as earnings reports and insider stock sales.

**Why it matters:** filings are official and dated, so they're useful markers on the chart ("earnings came out here").

**How we get it:** SEC EDGAR, the government's free database. It requires a contact email in each request and allows up to 10 requests per second.

**Keep in mind:** filings are public the moment they're released, so they rarely *lead* the price. They're better for context than prediction.

---

## 5. Job postings (growth plans), stretch goal

**What it is:** how many open jobs a company lists over time.

**Why it matters:** companies hire before they grow. A jump in engineering roles at NVIDIA, for example, could hint at expansion before it shows up in earnings.

**How we get it:** daily snapshots of public job listings.

**Keep in mind:** there's **no free history**. If we want this signal, we have to start collecting daily **as early as possible**, or there will be nothing to chart by presentation day.

---

## 6. App rankings (engagement), stretch goal

**What it is:** where a company's app ranks in the App Store or Google Play each day.

**Why it matters:** for Robinhood and Coinbase, app usage *is* the business. A ranking jump means more people trading, which can mean more revenue.

**How we get it:** daily snapshots of public chart rankings.

**Keep in mind:** same as job postings: no free history, so start early or skip it.

---

## 7. Reddit (retail chatter), on hold

**What it is:** how much, and how positively, people on Reddit talk about a company.

**Why it matters:** retail investors move stocks like HOOD and COIN, and Reddit is where they talk.

**Status:** Reddit closed free self-service API access in November 2025. New access now needs manual approval, which reportedly takes weeks. **We won't build around it unless approval comes through.** We don't scrape around their rules.

---

## 8. Google Trends (search interest), on hold

**What it is:** how often people search a company's name on Google.

**Why it matters:** similar to Wikipedia pageviews, it measures attention.

**Status:** the popular free library (`pytrends`) was archived in 2025 and no longer works reliably, and Google's official API is invite-only. **Wikipedia pageviews are our stand-in.**

---

## 9. Web traffic, skipped

**What it is:** how many people visit a company's website.

**Status:** there's no good free source, so it's out of scope.

---

## How it all fits together

Every source produces data in the **same simple format**, one row per company, per day, per signal:

| date | ticker | signal | value | source |
|---|---|---|---|---|
| 2026-10-21 | COIN | close_price | 248.10 | yfinance |
| 2026-10-21 | COIN | wiki_pageviews | 31000 | wikimedia |
| 2026-10-21 | COIN | news_sentiment | 0.42 | finbert |

Because every source looks the same, the dashboard can display any signal without special code, and anyone can add a new source without breaking the others. See `docs/DATA_FORMAT.md` for details.

---

## A note on honesty

Alternative data is noisy. A few months of data across 10 companies won't prove that a signal predicts prices. Our goal is to **explore and show patterns clearly**, and to be upfront about what each signal can and can't tell us.
