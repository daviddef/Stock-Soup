# Stock-Soup Report Template

Fill ALL `[PLACEHOLDER]` tokens with values from the current run before passing to email-builder.py.

---

Save to `/Users/daviddefranceski/Claude/Projects/Share / Stock Trading/hourly-stock-watch.md` (OVERWRITE each run).

---

# 📈 Hourly Stock Watch — [TIME AEST] | [DATE]

> *[One sentence: ASX session status. US market: [open/closed/holiday] per Finnhub market-status API.]*

---

## 🗂️ At a Glance

| | |
|---|---|
| **Market** | [ASX bias + US open/closed from Finnhub + VIX level] |
| **🇦🇺 ASX ⚡ Day** | **[ASX_DAY_TICKER]** — A$[price] ([%]) — [reason <8 words] — Entry A$X → Target A$X · [N] signals |
| **🇦🇺 ASX 📅 Week** | **[ASX_WEEK_TICKER]** — A$[price] ([%]) — [reason <8 words] — Entry A$X → Target A$X |
| **🇦🇺 ASX 📈 Long** | **[ASX_LONG_TICKER]** — A$[price] — [reason <10 words] |
| **🌏 Global ⚡ Day** | **[GLB_DAY_TICKER]** ([Exchange]) — $[price] ([%]) — [reason <8 words] — Entry $X → Target $X · [N] signals |
| **🌏 Global 📅 Week** | **[GLB_WEEK_TICKER]** ([Exchange]) — $[price] ([%]) — [reason <8 words] — Entry $X → Target $X |
| **🌏 Global 📈 Long** | **[GLB_LONG_TICKER]** ([Exchange]) — $[price] — [reason <10 words] |
| **ASX 200** | [level] ([%]) |
| **AUD/USD** | [rate from EODHD AUDUSD.FOREX — STEP 0B] |
| **Gold** | USD $[X]/oz · AUD $[X]/oz |

---

## 🔍 Candidates Assessed — [Current Session]

> *This section is MANDATORY and must appear before every picks section. It proves that picks emerged from a broad, signal-first market scan — not from the fixed watchlist. Readers see exactly what was scanned, how many candidates each source contributed, and how each was scored before any pick was selected.*

### Source Breakdown (fill every row — use 0 if source returned no candidates)

| Source | Market | Candidates Found | Leading Signal Type | Notes |
|--------|--------|-----------------|--------------------|----|
| ASX Volume Leaders (smallcaps volume-stocks) | ASX | [N] | VOL / NONE | Top movers by volume today |
| FMP Screener (STEP 0F-iii-B) | ASX / GLOBAL | [N] | FMP Screen / FMP+Vol | New candidate discovery — not watchlist-constrained |
| ASX Announcements (price-sensitive) | ASX | [N] | ASX ANN / DEAL | Material anns today — pre-move opportunities |
| News feeds — SDU / Motley Fool / LiveWire | ASX | [N] | UPGRADE / COVERAGE | Broker calls, article tickers extracted |
| FMP News (STEP 0F-iii-C) | GLOBAL / ASX | [N] | FMP NEWS | Fresh articles last 2h on picks and candidates |
| Sector macro — FMP Economic Calendar (STEP 0F-iii-E) | GLOBAL | [N] | SECTOR / MACRO EVENT | High-impact macro releases today |
| US movers — Alpha Vantage TOP_GAINERS_LOSERS | GLOBAL | [N] | AV TOP MOVER | US stocks ≥5% move with ASX equivalent exposure |
| Mediastack global news (AU business + keyword scan) | ASX / GLOBAL | [N] | Mediastack Lead | International stories ahead of AU feeds |
| SimplyWallSt community narratives | ASX | [N] | SWS Community Pick | Retail conviction + DCF signals |
| TradingView Ideas (technical community) | GLOBAL / ASX | [N] | TV Community | Chart setups published last 24h |
| yfinance historical signals (STEP 0F-i) | ASX / GLOBAL | cached | SMA trend / vol ratio | Daily compute — RSI trend, SMA position, vol_ratio_20d |
| Twelve Data advanced technicals (STEP 0F-ii) | ASX | cached daily | Supertrend / ADX | 1×/day max — Supertrend direction + ADX strength |
| FMP Analyst Grades (STEP 0F-iii-D) | ASX / GLOBAL | [N] | Analyst consensus | Buy/Hold/Sell consensus for globe-flagged stocks |
| Discovery Alert headlines (Feed 1B) | ASX | [N] | PRE-MOVE / DEAL | ASX small cap catalyst alerts — headline + ticker extraction |
| Reddit r/ausfinance (Feed 28) | ASX | [N] | REDDIT HOT / COVERAGE | Retail conviction signals >50 upvotes on ASX tickers |
| Reddit r/stocks + r/investing (Feed 29) | GLOBAL | [N] | REDDIT HOT / DD | Global retail sentiment — DD posts, upvoted tickers |
| Investing.com AU RSS (Feed 30) | ASX / GLOBAL | [N] | MACRO / SECTOR | Macro news: RBA, AUD/USD, commodity prices, global risk |
| watchlist.json + eToro tickers (fetched in STEP 0A) | ASX / GLOBAL | [N] | Various | Watchlist stocks assessed INDEPENDENTLY in this pool |
| **TOTAL ASX candidates** | **ASX** | **[N]** | — | Entering ASX scoring pool (→ 3 picks) |
| **TOTAL GLOBAL candidates** | **GLOBAL** | **[N]** | — | Entering Global scoring pool (→ 3 picks) |

> ⚠️ Watchlist stocks are entered into the pool like any other candidate and must earn their score — they receive no priority over signals from other sources.

### Full Scored Candidate Pool (STEP 0E output — all candidates ranked before pick selection)

| Ticker | Source | Price | RSI | vs SMA50 | Vol | Leading Signal | Score | Decision |
|--------|---------|-------|-----|----------|-----|----------------|-------|----------|
| [TKR] | Vol/Ann/News/Watch | $X | XX | ↑/↓ | ⚡ Xx / — | ASX ANN / DEAL / UPGRADE / VOL / NONE | X/5 | ⚡ DAY / 📅 WEEK / 📈 LONG / Monitor / Skip |

*Show two tables — ASX and GLOBAL — matching the STEP 0E dual candidate pool. Scores use the leading-indicator model: base 1–5 by catalyst type + bonuses (yfinance trend, Twelve Data Supertrend/ADX, FMP grades, multi-source, SMA, SWS) + penalties. The top 3 ASX become ASX picks; top 3 Global become Global picks.*

---

## 💼 Portfolio Watch (held — not new picks)

*[VTM, IEL, TLX, NTU watchlist — always included; report current price, RSI, SMA position, and 24h outlook. See 👁️ Watchlist section below for full detail.]*

| Ticker | Price | 1D% | RSI | vs SMA50 | vs SMA200 | Note |
|--------|-------|-----|-----|----------|-----------|------|
| VTM | $X | X% | X | ↑/↓ | ↑/↓ | [1 sentence] |
| IEL | $X | X% | X | ↑/↓ | ↑/↓ | [1 sentence] |
| TLX | $X | X% | X | ↑/↓ | ↑/↓ | [1 sentence] |
| NTU | $X | X% | X | ↑/↓ | ↑/↓ | [1 sentence] |
| PLTR | $X | X% | — | — | — | [1 sentence] |

---

## 🎯 New Picks — [DATE e.g. Monday 23 Jun]

### 🇦🇺 ASX Picks

| Type | Ticker | Name | Entry | Target | Stop | Signals | Conviction | Catalyst |
|---|---|---|---|---|---|---|---|---|
| ⚡ Day | [ASX_DAY_TICKER] | [Company] | A$X–A$X | A$X–A$X | A$X | [N sources] | ⭐⭐⭐⭐⭐ | [<8 word catalyst] |
| 📅 Week | [ASX_WEEK_TICKER] | [Company] | A$X–A$X | A$X–A$X | -X% | [N sources] | ⭐⭐⭐⭐ | [<8 word catalyst] |
| 📈 Long | [ASX_LONG_TICKER] | [Company] | A$X–A$X | A$X–A$X | A$X | [N sources] | ⭐⭐⭐ | [<8 word catalyst] |

> If fewer than 3 ASX candidates score ≥ 3.5: write "No ASX [timeframe] pick this run — insufficient signal strength."

### 🌏 Global Picks

| Type | Ticker | Exchange | Name | Entry | Target | Stop | Signals | Conviction | Catalyst |
|---|---|---|---|---|---|---|---|---|---|
| ⚡ Day | [GLB_DAY_TICKER] | NYSE/NASDAQ | [Company] | $X–$X | $X–$X | $X | [N sources] | ⭐⭐⭐⭐⭐ | [<8 word catalyst] |
| 📅 Week | [GLB_WEEK_TICKER] | NYSE/NASDAQ | [Company] | $X–$X | $X–$X | -X% | [N sources] | ⭐⭐⭐⭐ | [<8 word catalyst] |
| 📈 Long | [GLB_LONG_TICKER] | NYSE/NASDAQ | [Company] | $X–$X | $X–$X | $X | [N sources] | ⭐⭐⭐ | [<8 word catalyst] |

> If fewer than 3 Global candidates score ≥ 3.5: write "No Global [timeframe] pick this run — insufficient signal strength."
> **DIVERSITY RULE:** If the top scorer would fill all 3 slots, it takes ONLY the highest-conviction slot (usually Day). The next-best distinct ticker takes the second slot, third-best takes the third. Label runner-ups clearly.
> **Runner-up format:** Row ticker + "(Runner-up ⚠️ lower conviction)" in Name column. Still provide entry/target/stop.

*Signals = number of independent sources confirming the thesis (1 src=⭐, 3=⭐⭐⭐, 5+=⭐⭐⭐⭐⭐). Earnings risk: flag ⚠️ in Catalyst column if earnings within 5 days.*
*[Add footnotes for any price uncertainty, e.g. "* verify at open"]*

---

## 📊 Prior Picks — Performance

| Timeframe | Market | Ticker | Entry Price | Current | Move | Result |
|-----------|--------|--------|-------------|---------|------|--------|
| ⚡ Day | 🇦🇺 ASX | [ASX_DAY_TICKER] | A$X | A$X | +/-X% | ✅/❌/📊 [1 sentence] |
| 📅 Week | 🇦🇺 ASX | [ASX_WEEK_TICKER] | A$X | A$X | +/-X% | ✅/❌/📊 [1 sentence] |
| 📈 Long | 🇦🇺 ASX | [ASX_LONG_TICKER] | A$X | A$X | +/-X% | ✅/❌/📊 [1 sentence] |
| ⚡ Day | 🌏 Global | [GLB_DAY_TICKER] | $X | $X | +/-X% | ✅/❌/📊 [1 sentence] |
| 📅 Week | 🌏 Global | [GLB_WEEK_TICKER] | $X | $X | +/-X% | ✅/❌/📊 [1 sentence] |
| 📈 Long | 🌏 Global | [GLB_LONG_TICKER] | $X | $X | +/-X% | ✅/❌/📊 [1 sentence] |

*If no prior data: "First run — no prior picks to track."*

---

## 🎯 PRIMARY RECOMMENDATIONS

> ⚠️ This section contains 6 detailed pick cards — 3 ASX and 3 Global. Each card follows the same format below. Write all 6 in order: ASX Day → ASX Week → ASX Long → Global Day → Global Week → Global Long.

---

## 🇦🇺 ASX PRIMARY RECOMMENDATIONS

### ⚡ ASX Day Trade Pick (0–24 hours)

**[ASX_DAY_TICKER] — [Company Name] (ASX)**

| | |
|---|---|
| **Price / Move** | $X (+X%) [smallcaps.com.au if ASX] |
| **Entry** | $X |
| **Target** | $X (+X%) |
| **Stop** | $X (−X%) |
| **RSI / SMA Signal** | [From smallcaps if ASX: RSI [X] — [below/above] 50-day SMA $X] |
| **Volume** | [Today vs avg — spike = conviction] |
| **Finnhub Signal** | [For US picks: sentiment, recommendation, or news headline] |
| **Why today** | [Specific catalyst — concise] |
| **Time sensitivity** | [Why today not tomorrow] |
| **Risk** | [Key risk] |

---

### 📅 Weekly Pick (2–10 days)

**[TICKER] — [Company Name] ([Exchange])**

| | |
|---|---|
| **Price / Move** | $X (+X%) |
| **Entry** | $X–$X |
| **Target** | $X (+X%) |
| **Stop** | $X (−X%) |
| **RSI / SMA Signal** | [smallcaps RSI + SMA context for ASX picks] |
| **5-Day Performance** | [smallcaps 5D % — trend confirmation] |
| **Finnhub Signal** | [Analyst consensus, price target, or sentiment from Finnhub if US pick] |
| **Why this week** | [Swing setup / catalyst] |
| **Catalyst to watch** | [Upcoming event — check Finnhub earnings calendar] |
| **Risk** | [Key risk] |

---

### 📈 Long Term Pick (1–12 months)

**[TICKER] — [Company Name] ([Exchange])**

| | |
|---|---|
| **Price** | $X |
| **Analyst Target** | Mean $X · High $X · Low $X (Finnhub / web search) |
| **Consensus** | [Strong Buy / Buy / Hold breakdown from Finnhub] |
| **Upside to Mean** | +X% |
| **200-Day SMA** | $X [above/below — structural trend signal] |
| **Investment thesis** | [2–3 sentences] |
| **Entry strategy** | [Buy now / accumulate / wait for dip] |
| **Risk** | [Key risk — flag earnings date if within 30 days] |

---

## 👁️ Watchlist

### ASX:VTM — Victory Metals

| Field | Data |
|-------|------|
| **Price / % Move** | [From smallcaps.com.au — label "Live" if ASX open, "Close" if after hours] |
| **Day Range** | [smallcaps High – Low] |
| **52-Week Range** | [smallcaps 52wk Low – 52wk High] |
| **Volume** | [Today's volume] vs [10D avg] — [⚡ spike if >2x avg] |
| **Value Traded** | [$X — liquidity indicator] |
| **Bid / Ask** | [$X × qty / $X × qty — note if spread >1%] |
| **RSI-14** | [From smallcaps — Overbought >70 / Neutral / Oversold <30] |
| **50-Day SMA** | [$X — price is [above/below] → [bullish/bearish] trend] |
| **200-Day SMA** | [$X — price is [above/below] → [bull/bear] market structure] |
| **Performance** | 1D: [X%] · 5D: [X%] · 13W: [X%] · YTD: [X%] |
| **Market Cap** | $[X]M |
| **Fundamentals** | [North Stanmore HREE project context. PFS status. Any financing news.] |
| **Recent Headlines** | [Top 3 smallcaps.com.au headlines — title + author] |
| **24–48h Outlook** | [Bullish / Bearish / Neutral + reason] |
| **Catalyst / Risk** | [Specific trigger — e.g. PFS release, drill results, JORC update] |

### NYSE:PLTR — Palantir Technologies

| Field | Data |
|-------|------|
| **Price / % Move** | [Finnhub `c` / `dp`% — definitive source] |
| **Day Range** | [Finnhub `l` – `h`] |
| **Prev Close** | [Finnhub `pc`] |
| **Analyst Consensus** | [From Finnhub recommendations: e.g. "Strong Buy: 8 / Buy: 12 / Hold: 5 / Sell: 1" — period [YYYY-MM]] |
| **Price Targets** | [Finnhub: Mean $X · Median $X · High $X · Low $X (as of [date])] |
| **News Sentiment** | [Finnhub: Bullish X% / Bearish X% · X articles this week · Score: X] |
| **Insider Sentiment** | [Finnhub MSPR: positive = net buying, negative = net selling] |
| **Recent Headlines** | [Top 3 Finnhub headlines with source + datetime] |
| **RSI-14** | [smallcaps.com.au if fetched, else —] |
| **Technicals** | [Key levels, trend, volume context] |
| **24–48h Outlook** | [Bullish / Bearish / Neutral + reason incorporating Finnhub data] |
| **Catalyst / Risk** | [Earnings date from Finnhub calendar if within 14 days, else key risk] |

---

## 🇦🇺 ASX Deep Dive

| Ticker | Name | Price | Move | RSI | 50D SMA | Vol vs Avg | Timeframe | Catalyst |
|--------|------|-------|------|-----|---------|------------|-----------|---------|
| [TKR] | [Name] | $X | +X% | [X] | [↑/↓$X] | [Xx] | Day/Week/Long | [1 sentence] |
| [TKR] | [Name] | $X | +X% | [X] | [↑/↓$X] | [Xx] | Day/Week/Long | [1 sentence] |
| [TKR] | [Name] | $X | +X% | [X] | [↑/↓$X] | [Xx] | Day/Week/Long | [1 sentence] |

*RSI and SMA from smallcaps.com.au. Price above 50D SMA (↑) = bullish. Volume ratio = today/10D avg.*

**Sector spotlight:** [ASX sectors leading/lagging — 2 sentences]

---

## 📰 News Pulse

*Sources: fool.com.au · livewiremarkets.com · morningstar.com.au · stocksdownunder.com*

### ⭐ Watchlist Mentions
[If VTM / PDN / DYL / PLTR appear in today's news feeds — list with source, headline, 1-sentence summary. If none: "No watchlist mentions in today's feeds."]

### 🔥 Stocks Down Under — Top Stories
| Time | Ticker | Headline | Signal |
|------|--------|----------|--------|
| [Xh ago] | [ASX:TKR or —] | [Article title] | [Buy/Watch/Avoid/Info] |
| [Xh ago] | [ASX:TKR or —] | [Article title] | [Buy/Watch/Avoid/Info] |
| [Xh ago] | [ASX:TKR or —] | [Article title] | [Buy/Watch/Avoid/Info] |

*(Top 4–5 items from stocksdownunder.com — prioritise articles with ASX ticker codes)*

### 📋 Broker Notes & Movers (Motley Fool)
- **[Category tag]:** [Headline] — *[Key takeaway: broker, rating, target — from sub-link if fetched]*
- **[Category tag]:** [Headline] — *[Key takeaway]*
- **[Category tag]:** [Headline] — *[Key takeaway]*

*(Top 4–5 items from fool.com.au/category/share-market-news + /latest-asx-200-chart-price-news)*

### 💡 Fund Manager Insights (LiveWire)
- **[Date]:** [Article title] — [Author, Firm] — *[Key stock call or theme in 1 sentence]*
- **[Date]:** [Article title] — [Author, Firm] — *[Key stock call or theme in 1 sentence]*

*(Top 3–4 items — prioritise Buy Hold Sell episodes with specific ticker calls)*

### 📐 Morningstar — Analyst Picks
- **[Date]:** [Article title] — *[Fair value signal: undervalued/overvalued + ticker if named]*
- **[Date]:** [Article title] — *[Fair value signal]*

*(Top 3 items from morningstar.com.au/insights/stocks)*

### 🔍 Themes Spotted Today
- *[Recurring theme across feeds — e.g. "Uranium coverage strengthening — 2 articles"]*
- *[Sector trend — e.g. "Broker upgrades concentrated in energy sector"]*
- *[Macro signal — e.g. "RBA rate hold commentary dominating"]*


---

## 🌏 Global Markets Spotlight

**US Market Status:** [Open / Closed / Holiday name — from Finnhub market-status API]

**US Top Gainers (from web search):**
- [TICKER]: $X (+X%) — [catalyst] — *Day/Week*

**Global movers:**
- **[TICKER] ([Exchange]):** $X (+X%) — [catalyst] — *Day/Week/Long*

(list 3–5 total)

---

## 📡 Data Sources Summary

| Metric | [Active Global pick] | VTM (ASX) | PDN (ASX) | DYL (ASX) |
|--------|------------|-----------|-----------|-----------|
| Price Source | Finnhub | smallcaps.com.au | smallcaps.com.au | smallcaps.com.au |
| Price / Move | $[c] ([dp]%) | $[X] ([X]%) | $[X] ([X]%) | $[X] ([X]%) |
| RSI-14 | — | [X] | [X] | [X] |
| 50-Day SMA | — | $[X] | $[X] | $[X] |
| 200-Day SMA | — | $[X] | $[X] | $[X] |
| Vol vs Avg | — | [Xx] | [Xx] | [Xx] |
| Analyst Consensus | [X]B/[X]H/[X]S (Finnhub) | — | — | — |
| Mean Price Target | $[X] (Finnhub) | — | — | — |
| News Sentiment | [X]% Bullish (Finnhub) | smallcaps.com.au | smallcaps.com.au | smallcaps.com.au |
| Insider Buying | MSPR [X] (Finnhub) | — | — | — |
| Earnings Date | [X or "None <30d"] | — | — | — |

---

## ⚠️ Market Context & Macro

- **US Indices:** S&P 500: [X] ([X%]) | Nasdaq: [X] ([X%]) | Dow: [X] ([X%])
- **US Market:** [Open / Closed — Finnhub confirmed]
- **ASX 200:** [X] ([X%])
- **VIX:** [X] — [Low/Moderate/Elevated]
- **Gold (USD/oz):** $[X] | **AUD/USD:** [from EODHD — STEP 0B]
- **Macro:** [2–3 sentences: Fed, rates, China, geopolitics]
- **Session bias:** [Bullish / Bearish / Mixed — one sentence]

---

## 🧠 Section 15 — Decision Logic & Research Trail

*This section shows exactly how picks were selected this run — the data inputs, signals considered, and reasoning chain. Produced every run.*

### 15.A — Candidate Pool Brief

*Write this paragraph FIRST, before the table. It gives the reader a human-readable summary of how this run's candidate pool was assembled — what sources fired, how many tickers were identified, what signals dominated, and what was filtered out. Example format below:*

> **How this run's pool was built:**
> This run scanned **[N] sources** and surfaced **[N] initial tickers** before filtering. The pool was drawn from:
> - 📊 **Volume scan** (smallcaps.com.au/volume-stocks): [N] candidates from top-20 ASX by volume — [top tickers by move, e.g. "XYZ +8%, ABC +5%"]
> - 📰 **News extraction** (SDU / Motley Fool / LiveWire / smallcaps): [N] tickers extracted from headlines — [dominant theme, e.g. "uranium coverage strengthening: PDN, DYL"]
> - 📣 **ASX Announcements** (Feed 13): [N] price-sensitive announcements — [e.g. "EOS signed EU defence contract; DRO trading halt lifted"]
> - 📈 **Alpha Vantage US movers** (once/day): [N] qualifying US movers — [e.g. "NVDA +3.1%, LMT +1.8%"]
> - 🌐 **Mediastack global news** (once/day): [N] articles — [e.g. "uranium supply story from Reuters, rare earths tariff article"]
> - 👁️ **Fixed watchlist**: VTM, IEL, TLX, NTU, PDN, DYL, PLTR — included every run
> - 🏅 **SWS quality filter**: [N] tickers carried SWS Undervalued/High Growth tags
>
> **Dominant signal type this run:** [ASX ANN / VOL / COVERAGE / SECTOR / EARNINGS]
>
> **Filtered out before scoring:** [N] tickers removed because: [list reasons — e.g. "no live price (2)", "RSI >70 overbought (3)", "stale news >7d (1)", "already up >15% (1)"]
>
> **Entered scoring:** [N] tickers → final candidate pool below

---

### 15.A — Candidate Pool (all tickers evaluated)

| Ticker | Entry Source | Price | RSI | vs SMA50 | Vol Ratio | News Catalyst | SWS/Signal | Score | Decision |
|--------|-------------|-------|-----|----------|-----------|---------------|-----------|-------|----------|
| [TKR] | [Vol / News / Ann / Watch / AV Mover / Mediastack] | $[X] | [X] | ↑/↓ | [X]x [⚡ if >2x] | [Y/N — source name] | [SWS Undervalued ✅ / PRE-MOVE ✅ / —] | [X]/5 | [Day/Week/Long/Skip — reason] |

*Total evaluated: [N] tickers · Sources: [N] · Pre-filter removed: [N] · Final pool: [N]*

### 15.B — Pick Selection Reasoning (6 picks — ASX pool then Global pool)

**🇦🇺 ASX ⚡ Day Pick: [ASX_DAY_TICKER]**
- Signals fired: [e.g. "Vol 3x ⚡ (smallcaps)", "RSI 44 neutral", "FMP+Vol double-confirmed", "yf rsi_trend=rising", "TD Supertrend=up ADX=32"]
- Signals considered but not met: [e.g. "below 50D SMA — counter-trend risk"]
- Why over ASX runner-up [RUNNER_UP]: [1 sentence]
- Confidence: [High / Medium / Low]

**🇦🇺 ASX 📅 Week Pick: [ASX_WEEK_TICKER]**
- Signals fired: [list each]
- Key differentiator: [what made this the best ASX week candidate]
- Why over ASX runner-up [RUNNER_UP]: [1 sentence]
- Confidence: [High / Medium / Low]

**🇦🇺 ASX 📈 Long Pick: [ASX_LONG_TICKER]**
- Signals fired: [list each — FMP analyst grades, SWS tag, fundamental thesis]
- Investment thesis summary: [2 sentences]
- Confidence: [High / Medium / Low]

**🌏 Global ⚡ Day Pick: [GLB_DAY_TICKER]**
- Signals fired: [e.g. "AV TOP MOVER +8%", "RSI 52 rising", "Finnhub 12B/3H/1S consensus", "above both SMAs", "FMP fresh news"]
- Why over Global runner-up [RUNNER_UP]: [1 sentence]
- Confidence: [High / Medium / Low]

**🌏 Global 📅 Week Pick: [GLB_WEEK_TICKER]**
- Signals fired: [list each]
- Key differentiator: [what made this the best Global week candidate]
- Why over Global runner-up [RUNNER_UP]: [1 sentence]
- Confidence: [High / Medium / Low]

**🌏 Global 📈 Long Pick: [GLB_LONG_TICKER]**
- Signals fired: [list each — Finnhub consensus, FMP grades, upside pct]
- Investment thesis summary: [2 sentences]
- Confidence: [High / Medium / Low]

### 15.C — Data Source Registry & This-Run Status

The definitive source of truth for every data source in the system. Every source appears here — including those not used this run, those with known limitations, and those parked for future activation. Update Status column each run.

**Legend:** ✅ Fetched & used · ⚠️ Partial/JS-blocked/degraded · ❌ Blocked/403/unavailable · 🔒 Local only (can't run in scheduled task) · ⏸ Parked (known issue) · 📅 Once/day (cached) · ⛔ Deprecated (confirmed broken — do not use)

---

**API Data Sources**

| Source | Tier / Key | Status | What it provides | This-run value |
|---|---|---|---|---|
| EODHD — ASX live prices (batch) | Free · `6a3c6b9cf3a1a7.93438421` | ✅ | ASX quotes: close, change%, volume | [Tickers fetched] |
| EODHD — AUD/USD (`AUDUSD.FOREX`) | Free | ✅ | Live FX rate — primary source | [rate e.g. 0.6903] |
| EODHD — ASX news + sentiment | Free | ✅ | Per-ticker articles + polarity score | [Tickers with news] |
| EODHD — EOD history (`/eod`) | Free (255 days) | ✅ | Prior closes, 5D/13W perf, manual SMA | [Used for: X] |
| EODHD — [active US pick].US cross-check | Free | ✅ | US stock price verification (active global pick only) | $[X] |
| EODHD — intraday | ❌ Paid | ⏸ | Tick data — not on free tier | — |
| EODHD — technical indicators API | ❌ Paid | ⏸ | RSI/SMA via API — use smallcaps instead | — |
| EODHD — fundamentals API | ❌ Paid | ⏸ | Earnings, balance sheet | — |
| EODHD — gold (XAUUSD.FOREX) | ❌ NA (free) | ⏸ | Returns all NA — use web search | — |
| Finnhub — [active Global picks] quotes | Free · `d8qb92pr01qr03ngsk0gd8qb92pr01qr03ngsk10` | ✅ | Live price for all scored Global candidates | [TICKER] $[c] ([dp]%) |
| Finnhub — [top Global finalist] consensus | Free | ✅ | strongBuy/buy/hold/sell/strongSell + period | [X]SB [X]B [X]H [X]S [X]SS |
| Finnhub — [top Global finalist] financials | Free | ✅ | 52wHigh/Low, beta, PE, revenue growth | 52wH=$[X] 52wL=$[X] β=[X] |
| Finnhub — [top Global finalist] insider | Free | ✅ | MSPR — net insider buying/selling signal | MSPR=[X] |
| Finnhub — [top Global finalist] news | Free | ✅ | Recent articles — scan for catalyst quality | [N] articles — [tone] |
| Finnhub — [top Global finalist] earnings | Free | ✅ | EPS actual vs estimate (4 quarters) | Q[X]: [X] vs est [X] = [X]% beat |
| Finnhub — BTC risk signal | Free | ✅ | BTC/USD — risk-on/off gauge | BTC $[X] ([dp]%) [risk-on/off] |
| Finnhub — US market status | Free | ✅ | Open/closed/holiday | [Open/Closed] |
| Finnhub — earnings calendar | Free | ✅ | Upcoming earnings — flag picks at risk | [N] upcoming; picks flagged: [X] |
| Finnhub — general news | Free | ✅ | 100 articles — macro signal scan | [Key signals] |
| Finnhub — price target (any ticker) | ❌ 403 Paid | ⏸ | Analyst mean/high/low targets | Use AV OVERVIEW instead |
| Finnhub — news sentiment score | ❌ 403 Paid | ⏸ | Bullish/bearish % score | Use manual headline read |
| Finnhub — forex rates | ❌ 403 Paid | ⏸ | FX data | Use EODHD AUDUSD.FOREX |
| Finnhub — economic calendar | ❌ 403 Paid | ⏸ | Rate decisions, macro events | — |
| Finnhub — ASX tickers | ❌ Wrong data | ⛔ Never use | Returns wrong US company for ASX symbols | — |
| Alpha Vantage — [top US candidate] OVERVIEW | Free · `9OBSWEYSQPZ6AI8Z` · 25/day | 📅 Once/day | PE, analyst target, 52w range for whoever scores highest | AnalystTarget=$[X] PE=[X] (cached) |
| Alpha Vantage — [top US candidate] SMA-50 | Free · 25/day | 📅 Once/day | 50-day moving average | SMA-50=$[X] (cached) |
| Alpha Vantage — [top US candidate] SMA-200 | Free · 25/day | 📅 Once/day | 200-day moving average | SMA-200=$[X] (cached) |
| Alpha Vantage — TOP_GAINERS_LOSERS | Free · 25/day | 📅 Once/day | US market movers — recommendation candidates | [N] candidates added to pool |
| Alpha Vantage — EARNINGS_CALENDAR | Free · 25/day | 📅 Once/day | Next 3 months US earnings (CSV) | [Picks cross-checked] |
| Alpha Vantage — ASX tickers | ❌ Not covered | ⛔ Never use | AV does not cover ASX | — |
| Mediastack — news (`/v1/news`) | Free · `1bc16cc5ed37b75a27e54735e5b88060` · **100 calls/month · 30min delay** | 📅 Once/day | Global news from 7,500+ sources — proactive candidate discovery (country=au + keywords for sectors); 30min delayed on free tier; no custom headers needed | [N] AU business articles, [N] candidates, [N] sector signals |
| eToro API — watchlist/rates | 🔒 Local Python only | ⏸ Parked | Requires custom headers; not usable in scheduled tasks | — |
| eToro API — feed endpoints | ❌ 403 (key type) | ⏸ Parked | Needs trading account key (not developer portal key). To activate: etoro.com → Settings → Trading → API Key Management | — |
| eToro — web pages | ❌ 403 bot-block | ⏸ Expected | etoro.com/discover and /news blocked | eToro web: 403 (expected — skipped) |
| Google Finance — ASX prices | ⛔ STALE DATA | ⛔ Deprecated | Returned April 2026 data on June 25 runs | NEVER USE |
| Google Finance — AUD/USD | ⛔ STALE DATA | ⛔ Deprecated | 0.7137 (April) vs actual 0.6903 (June) | NEVER USE |
| Google Finance — macro cross-check | ⚠️ JS-rendered | Optional | Index levels only if JS partially renders | [Level or "JS-blocked"] |

---

**Web-Fetch News Feeds**

| Feed | Source | Status | Key contribution |
|---|---|---|---|
| Feed 1 | Stocks Down Under | [✅/⚠️/❌] | [Key signal or "no watchlist mentions"] |
| Feed 2 | Motley Fool recent headlines | [✅/⚠️/❌] | [Key signal] |
| Feed 3 | Motley Fool ASX 200 Today | [✅/⚠️/❌] | [5 things to watch / market recap] |
| Feed 4 | Motley Fool Resources sector | [✅/⚠️/❌] | [Resources signals — uranium, rare earths] |
| Feed 5 | Motley Fool Tech & Defence | [✅/⚠️/❌] | DRO articles this week: [N] · [tech signals] |
| Feed 6 | Motley Fool Industrials | [✅/⚠️/❌] | [Industrials signals] |
| Feed 7 | Motley Fool IPOs | [✅/⚠️/❌] | IPO market: [ACTIVE/QUIET] |
| Feed 8 | Motley Fool Reporting Calendar | [✅/⚠️/❌] | [Earnings risk status for picks] |
| Feed 9 | LiveWire Markets | [✅/⚠️/❌] | [Buy/Hold/Sell calls or "no mentions"] |
| Feed 10 | Morningstar Australia | [✅/⚠️/❌] | [Fair value signals or blocked] |
| Feed 11 | SimplyWallSt Investing Ideas | [✅/⚠️ JS/❌] | [SWS quality tags found or JS-blocked] |
| Feed 12 | SimplyWallSt Community Narratives | [✅/⚠️ JS/❌] | [Community narratives + discount %] |
| Feed 13A | ASX Announcements (smallcaps.com.au) | [✅/⚠️/❌] | [Announcement catalysts for watched tickers] |
| Feed 13B | ASX Announcements (asx.com.au JSON) | [✅/⚠️ JS/❌] | [Supplementary — use if 13A incomplete] |
| Feed 14 | Smallcaps Hot Topics | [✅/⚠️/❌] | [Trending stories, sector heat] |
| Feed 15 | Smallcaps Latest News | [✅/⚠️/❌] | [Breaking company news] |
| Feed 16 | Smallcaps Upcoming Dividends | [✅/⚠️/❌] | [Ex-div flags for picks or none] |
| Feed 17 | Smallcaps Upcoming IPOs | [✅/⚠️/❌] | [IPO pipeline — risk-on/off gauge] |
| Feed 18 | Smallcaps Weekly Wrap & Fundie Picks | [✅/⚠️/❌] | [Fundie picks: [N] · market outlook] |
| Feed 19A | Smallcaps Mining sector | [✅/⚠️/❌] | [Mining signals: drill results, MRE] |
| Feed 19B | Smallcaps Energy sector | [✅/⚠️/❌] | [Energy signals] |
| Feed 19C | Smallcaps Technology sector | [✅/⚠️/❌] | [Tech signals: contracts, AI] |
| Feed 20 | SeekingAlpha Stocks on the Move | [✅/⚠️/❌] | [US movers visible before paywall] |
| Feed 21 | eToro API | ⏸ Parked | Blocked: web_fetch can't send auth headers; feed endpoints need trading account key — instrument IDs preserved |
| Feed 22 | Google Finance macro | ⚠️ JS-rendered | Index levels only — NOT for ASX prices (deprecated/stale) |
| Feed 23 | Sydney Morning Herald Markets | [✅/⚠️/❌] | [Australian journalism macro signals] |
| Feed 24 | PPAM Insights | [✅/⚠️/❌] | [Fund manager views or unavailable] |
| Feed 25 | Market Index Market Wraps | [✅/⚠️/❌] | [ASX daily recap, top movers] |
| Feed 26 | Moomoo Live News | [✅/⚠️ JS/❌] | [Live headlines or JS-blocked — always attempt] |
| Feed 27 | TradingView Ideas | [✅/⚠️ JS/❌] | [Chart setups, community conviction] |

---

**Smallcaps Tools & Web**

| Tool / Source | Status | Contribution |
|---|---|---|
| smallcaps.com.au/volume-stocks | [✅/⚠️] | [N] candidates from top-20 volume scan |
| smallcaps.com.au/stocks/asx-[ticker] | [✅/⚠️] | Price, RSI-14, SMA-50, SMA-200, news for [N] tickers |
| smallcaps.com.au/announcements | [✅/⚠️/❌] | [Catalysts found / none] |
| smallcaps.com.au/upcoming-dividends | [✅/⚠️/❌] | [Ex-div flags or none] |
| smallcaps.com.au/upcoming-ipos | [✅/⚠️/❌] | [IPO pipeline or none] |
| smallcaps.com.au/article/weekly-wrap | [✅/⚠️/❌] | [Fundie picks or unavailable] |
| WebSearch (x8 macro queries) | ✅ | VIX=[X] · Gold=$[X]USD · S&P=[X] · ASX200=[X] · gainers |
| Gold AUD (calculated) | ✅ Calculated | Gold(AUD) = Gold(USD) ÷ EODHD AUD/USD |
| stock-watch-log.md (prior picks) | ✅ | [Day/Week/Long tickers] → perf: [✅/❌/📊] |

---

**⚠️ Rules for this table:**
- Every source must appear here — ✅ means used, ⏸ means parked (still document), ⛔ means permanently deprecated
- Fewer than 35 rows means the research is incomplete
- Google Finance for prices/FX is permanently ⛔ — never promote back to active
- eToro remains ⏸ Parked until trading account user key is generated

### 15.D — What Was Ruled Out & Why

| Ticker | Why evaluated | Why rejected |
|--------|--------------|-------------|
| [TKR] | [Source that flagged it] | [Reason: below both SMAs / RSI >70 / no live price / earnings risk / low volume] |

### 15.E — Scoring Methodology (reference)

> **Philosophy: catch the move BEFORE it happens.** Catalysts score first; volume and price momentum are confirming signals, not primary filters.

| Score | Catalyst Requirement | Typical Pick |
|-------|---------------------|--------------|
| 5/5 | Fresh leading catalyst (ASX ANN / DEAL / UPGRADE) fired TODAY + stock NOT yet moved >10% | Day/Week |
| 4/5 | Known upcoming catalyst within 1 week (EARNINGS / SECTOR policy) OR vol spike + confirmed news catalyst | Day/Week |
| 3/5 | Strong fundamental thesis (analyst Buy, SDU coverage) but no imminent catalyst, OR catalyst but RSI extreme | Long / Watch |
| 2/5 | Volume move with no identifiable catalyst, OR catalyst stale >7 days, OR mixed signals | Monitor |
| 1/5 | Pure price momentum, no thesis, RSI >70 overbought, OR below both SMAs with no catalyst | Skip |

**Leading Signal badges (shown on each pick):**
`ASX ANN` — material announcement today · `DEAL` — signed supply/offtake/JV · `UPGRADE` — broker initiation/upgrade today · `EARNINGS` — date within 5 days · `SECTOR` — macro/policy catalyst · `COVERAGE` — 3+ sources in 24h · `VOL` — volume only (lowest conviction) · `PRE-MOVE` — catalyst fired, price not yet moved >5%

*Bonuses (max +2.0): +1.0 PRE-MOVE ASX ANN · +1.0 analyst upgrade today · +0.5 earnings within 5 days · +0.5 sector macro catalyst · +0.5 3+ sources in 24h · +0.5 SWS Undervalued+Growth · +0.5 SDU/MF thesis <48h · +0.5 eToro top-10 + RSI<70 · +0.5 TV Editors Pick · +0.5 above both SMAs*
*Penalties: −1.0 already up >15% today · −0.5 RSI>70 · −0.5 stale catalyst >7d · −0.5 target already hit · −0.5 capital raise · −0.5 below both SMAs · −0.5 VOL signal only*

---

## 🔭 Section 16 — Opportunity Pipeline & Decision Flow

*Render this every run as a visual summary of how opportunities were identified, scored, and priced. Fill in the [PLACEHOLDER] values from this run's data.*

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║          STOCK WATCH OPPORTUNITY PIPELINE — [TIME AEST] | [DATE]                   ║
╠══════════════╦═══════════════════╦═══════════════════╦══════════════╦══════════════╣
║  DATA IN     ║   SCAN PHASES     ║  CANDIDATE POOL   ║  SCORING     ║  PICKS       ║
╠══════════════╬═══════════════════╬═══════════════════╬══════════════╬══════════════╣
║ EODHD        ║ 1. Volume top-20  ║ [N] tickers in    ║ Base: 1–5    ║ ⚡ DAY       ║
║ (ASX prices  ║    ASX by volume  ║                   ║              ║  [TICKER]    ║
║  AUD/USD     ║                   ║ Sources:          ║ Bonuses:     ║  $[PRICE]    ║
║  news/sent.) ║ 2. News extract   ║ • Vol scan: [N]   ║ +1.0 PRE-MV  ║  Entry: $[X] ║
║              ║    27 web feeds   ║ • News:    [N]    ║ +1.0 UPGRDE  ║  Tgt:   $[X] ║
║ Finnhub      ║                   ║ • Ann:     [N]    ║ +0.5 EARN    ║  Stop:  $[X] ║
║ (Global pick ║ 3. ASX Ann scan   ║ • AV movers:[N]  ║ +0.5 SECTOR  ║  R:R ~[X]:1  ║
║  consensus   ║    (Feed 13)      ║ • Mediastack:[N] ║ +0.5 COVERG  ║              ║
║  insider     ║                   ║ • Watchlist: 7   ║ +0.5 SWS     ║ 📅 WEEK      ║
║  BTC signal) ║ 4. Sector macro   ║                   ║              ║  [TICKER]    ║
║              ║    (Feeds 4–6)    ║ Filtered out:     ║ Penalties:   ║  $[PRICE]    ║
║ Alpha Vantage║                   ║ No price:  [N]    ║ −1.0 UP>15%  ║  Entry: $[X] ║
║ (top cand.   ║ 5. Quality filter ║ RSI>70:    [N]    ║ −0.5 RSI>70  ║  Tgt:   $[X] ║
║  target      ║    (SWS tags)     ║ Stale news:[N]    ║ −0.5 STALE   ║  Stop:  $[X] ║
║  US movers   ║                   ║ Up>15%:    [N]    ║ −0.5 BLW SMA ║  R:R ~[X]:1  ║
║  once/day)   ║ 6. AV US movers   ║ Cap raise: [N]    ║ −0.5 VOL-ONL ║              ║
║              ║    (once/day)     ║                   ║              ║ 📈 LONG      ║
║ Mediastack   ║                   ║ ═══════════════   ║ ═══════════  ║  [TICKER]    ║
║ (global news ║ 7. Mediastack     ║ Final pool: [N]   ║ Top score:   ║  $[PRICE]    ║
║  once/day    ║    global news    ║ tickers scored    ║ [TICKER]=[X] ║  Entry: $[X] ║
║  30min delay)║    (once/day)     ║                   ║ Runner-up:   ║  Tgt:   $[X] ║
║              ║                   ║                   ║ [TICKER]=[X] ║  Stop:  $[X] ║
║ smallcaps    ║ 8. Watchlist pull ║                   ║ 3rd:         ║  R:R ~[X]:1  ║
║ (RSI/SMA     ║    (VTM IEL TLX   ║                   ║ [TICKER]=[X] ║              ║
║  vol scan    ║     NTU PDN DYL   ║                   ║              ║              ║
║  news)       ║     watchlist)    ║                   ║              ║              ║
╚══════════════╩═══════════════════╩═══════════════════╩══════════════╩══════════════╝
```

---

### 16.A — Pricing Methodology

*How entry, target, and stop levels are set for each pick type:*

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PRICING METHODOLOGY                               │
├──────────────┬──────────────────────────────────────────────────────────┤
│  ENTRY ZONE  │ • PRE-MOVE: below current ask (market hasn't priced it)  │
│              │ • Momentum: at ask or 0.5–1% above if volume confirmed   │
│              │ • Swing/Long: at or below key support / 50D SMA          │
│              │ • Use LIMIT orders — never chase with market orders       │
├──────────────┼──────────────────────────────────────────────────────────┤
│  TARGET      │ • Day: prior resistance / 3–5% above entry               │
│              │ • Week: analyst target / measured pattern move            │
│              │ • Long: consensus analyst target (AV AnalystTargetPrice)  │
│              │ • If no analyst target: 20–30% above entry minimum        │
├──────────────┼──────────────────────────────────────────────────────────┤
│  STOP LOSS   │ • Day: 1.5–2% below entry / below intraday low           │
│              │ • Week: below recent swing low / -5 to -8% from entry    │
│              │ • Long: below 200D SMA / -10 to -15% from entry          │
│              │ • NEVER use a stop below prior log entry zone price       │
├──────────────┼──────────────────────────────────────────────────────────┤
│  R:R MINIMUM │ • Day picks: minimum 2:1 (risk $1 to make $2)            │
│              │ • Week picks: minimum 2.5:1                              │
│              │ • Long picks: minimum 3:1                                │
│              │ • If R:R < minimum → widen target or tighten stop        │
│              │   before publishing. Never force a pick with poor R:R.   │
├──────────────┼──────────────────────────────────────────────────────────┤
│  CONVICTION  │ ⭐ = 1 source · ⭐⭐⭐ = 3 sources · ⭐⭐⭐⭐⭐ = 5+ sources  │
│  STARS       │ Scores ≥4.5 with PRE-MOVE signal = maximum conviction    │
│              │ Scores <3.5 = monitor only, not a published pick         │
└──────────────┴──────────────────────────────────────────────────────────┘
```

### 16.B — Signal Hierarchy (earliest → latest)

```
  SIGNAL TIMING                    WHAT IT MEANS
  ─────────────────────────────────────────────────────────────────
  🟢 PRE-MOVE  ←── BEST           Catalyst fired, price NOT moved >5%
     ASX ANN                      Material announcement — market catching up
     DEAL                         Signed contract/offtake/JV
     UPGRADE                      Broker initiation or upgrade TODAY
     ↑ Catch the move BEFORE it   Entry window: 0–4 hours after announcement
  ──────────────────────────────────────────────────────────────────
  🟡 UPCOMING                     Known catalyst within 1 week
     EARNINGS                     EPS date flagged — position ahead
     SECTOR                       Policy/macro event benefits whole sector
     ↑ Position AHEAD of event    Entry window: 1–5 trading days before
  ──────────────────────────────────────────────────────────────────
  🟠 BUILDING                     Conviction accumulating from multiple sources
     COVERAGE                     3+ independent sources, same thesis, 24h
     ↑ Still early but visible    Entry window: 1–3 days while thesis builds
  ──────────────────────────────────────────────────────────────────
  🔴 CONFIRMING  ←── LATE         Price and volume already moving
     VOL                          Volume spike only, no identifiable catalyst
     ↑ Hardest entry, widest stop Entry: only if RSI not overbought + R:R ≥2:1
  ─────────────────────────────────────────────────────────────────
```

### 16.C — This Run at a Glance

| Pipeline Stage | Count | Top Result |
|---|---|---|
| Sources scanned | [N] | EODHD, Finnhub, [N] web feeds, AV movers, Mediastack |
| Initial tickers surfaced | [N] | [Top ticker by signal strength] |
| Tickers scored | [N] | After pre-filter (no price / RSI extreme / stale) |
| Dominant signal type | [ASX ANN / VOL / COVERAGE / SECTOR] | [Brief reason] |
| Day pick score | [X]/5 | [TICKER] — [leading signal badge] |
| Week pick score | [X]/5 | [TICKER] — [leading signal badge] |
| Long pick score | [X]/5 | [TICKER] — [leading signal badge] |
| Tickers ruled out | [N] | [Top reason for rejections] |
| AUD/USD (EODHD) | [rate] | Used for all AUD conversions this run |
| US market | [Open/Closed] | [Holiday if any] |
| BTC risk signal | [risk-on/off] | BTC $[X] ([dp]%) |

---

## ⚠️ Disclaimer

*This report is generated by an automated research process for personal investment research only. It is not financial advice. All prices are indicative and should be verified before acting. Past pick performance does not guarantee future results. Always do your own research and consider your risk tolerance before entering any trade.*

---

## 📌 How Picks Are Chosen — Methodology Note

> This report uses a **leading-indicator scoring model** — recommendations are designed to identify opportunities *before* price and volume confirm the move, not after.
>
> **Why this matters:** By the time a stock shows a volume spike and is already up 10%, you've often missed the best entry. The scoring system prioritises catalysts that precede price movement: ASX announcements (government grants, supply deals, resource upgrades), analyst upgrades published today, and sector-wide policy shifts. Volume and price momentum are used as *confirming* signals, not primary triggers.
>
> **Signal hierarchy (earliest to latest):**
> 1. 🟢 `ASX ANN` / `DEAL` / `UPGRADE` — announcement or deal fires before market prices it in *(best entry window)*
> 2. 🟡 `EARNINGS` / `SECTOR` — known upcoming catalyst or sector-wide policy trigger *(position ahead of event)*
> 3. 🟠 `COVERAGE` — 3+ independent sources converging on same thesis *(building conviction)*
> 4. 🔴 `VOL` — volume spike only, no identified catalyst *(lowest conviction, widest stop)*
>
> A pick marked `PRE-MOVE` means the catalyst has fired but the stock has not yet moved >5% — this is the highest-conviction entry window. Watch for volume pickup as market confirmation.

---

## 📊 Section 15 — Motley Fool Sector Intelligence (STEP 0I output)

*Only populated when Feeds 4-8 surface meaningful signals.*

### 15.1 Sector Heat Map
| Sector | Articles This Week | Heat | Top Ticker Mentioned |
|---|---|---|---|
| Resources / Critical Minerals | [N] | HIGH/MED/LOW | [TICKER] |
| Tech & Defence | [N] | HIGH/MED/LOW | [TICKER] |
| Industrials | [N] | HIGH/MED/LOW | [TICKER] |

### 15.2 Reporting Season Cross-Reference
| Ticker | Reported | Result | Impact on Current Picks |
|---|---|---|---|
| IEL | Feb 26 2026 | +12% upgraded FY26 guidance | ✅ Validates Day pick thesis |
| [Next ticker] | [Date] | [Result] | [Impact] |

*Upcoming: Next ASX reporting season August 2026 — no earnings cliff risk for current picks.*

### 15.3 Resources Sector Signals
*Top signals from fool.com.au/category/sector/resources-shares:*
- [Broker/headline] — [Ticker] — [Signal type: upgrade / price target / article bullish]

### 15.4 Tech & Defence Signals
*DroneShield (DRO) article count this week: [N]*
| Date | Event | Signal |
|---|---|---|
| [Date] | [Event] | [Bullish/Neutral/Risk] |

### 15.5 Industrials Signals
*Top signals from fool.com.au/category/sector/industrials-shares:*
- [Headline] — [Ticker] — [Signal]

### 15.6 IPO Risk Appetite
*Source: fool.com.au/category/share-market-news/ipos/*
IPO market: **[ACTIVE/QUIET]** — [risk-on/neutral] backdrop for growth picks.

### 15.7 Runners-Up (did not make Section 3 top 3)
*Section 3 New Picks now carries Signals + Conviction columns — cross-source synthesis is embedded there.*
*List any additional candidates here that narrowly missed the cut:*
| Ticker | Timeframe | Signals | Why not top 3 |
|---|---|---|---|
| [TICKER] | Day/Week/Long | [N] | [reason] |

### 15.8 Source Status
| Source | Status | Key Extract |
|---|---|---|
| fool.com.au/recent-headlines | ✅ | [Top signal] |
| fool.com.au/category/sector/resources-shares | ✅ | [Top signal] |
| fool.com.au/category/sector/tech-shares | ✅ | [Top signal] |
| fool.com.au/category/sector/industrials-shares | ✅ | [Top signal] |
| fool.com.au/category/share-market-news/ipos | ✅ | [Top signal] |
| fool.com.au/asx-reporting-season-calendar | ✅ | [Earnings risk status] |
| simplywall.st/discover/au/investing-ideas | ✅/⚠️ | [Quality tags found / unavailable] |
| simplywall.st/community/narratives/au | ✅/⚠️ | [Community narratives found / unavailable] |
| smallcaps.com.au/announcements | ✅/⚠️ | [Announcement catalyst for watched tickers / unavailable] |
| moomoo.com/news/main/live | [✅/⚠️ JS-blocked/❌] | [Live headlines found / JS-blocked — attempted] |
| simplywall.st/community/narratives/au | ✅/⚠️ JS-blocked | [Mandatory Step 0C.5 — log result every run] |
| asx.com.au/markets/trade-our-cash-market/todays-announcements | ✅/⚠️ JS-blocked | [Supplemented by asx.com.au JSON API + smallcaps] |

---

## 📡 Appendix — Data Sources Status

*Status of every data source fetched this run. Verify before trading on any flagged source.*

### Price & Market Data

| Source | Asset | Status | Value Fetched | Notes |
|--------|-------|--------|---------------|-------|
| smallcaps.com.au | ASX:VTM | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · SMA50 $[X] · Vol [Xx] |
| smallcaps.com.au | ASX:[PICK1] | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · SMA50 $[X] · Vol [Xx] |
| smallcaps.com.au | ASX:[PICK2] | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · SMA50 $[X] · Vol [Xx] |
| smallcaps.com.au | ASX:[PICK3] | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · SMA50 $[X] · Vol [Xx] |
| smallcaps.com.au | ASX:TLX | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · [above/below] both SMAs |
| smallcaps.com.au | ASX:IEL | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · [above/below] both SMAs |
| smallcaps.com.au | ASX:NTU | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · [above/below] both SMAs |
| smallcaps.com.au | ASX:PDN | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · [note] |
| smallcaps.com.au | ASX:DYL | [✅/⚠️/❌] | $[X] ([X]%) | RSI [X] · [note] |
| smallcaps.com.au/volume-stocks | ASX Volume Leaders | ✅ Fetched | Top 20 scanned | [N] candidates identified |
| Finnhub | NYSE:[GLB_DAY_TICKER] | [✅/⚠️/❌] | $[X] ([X]%) | Consensus [X]B/[X]H/[X]S · Target $[X] |
| EODHD (AUDUSD.FOREX) | AUD/USD | [✅/⚠️] | [rate] | ⛔ Google Finance deprecated for FX |

*For each skipped volume leader: add a row with ❌ Skipped and reason.*

### News Feeds

| Feed | URL | Status | Key Extract |
|------|-----|--------|-------------|
| Stocks Down Under | stocksdownunder.com/articles | [✅/⚠️/❌] | [Top signal or "No watchlist mentions"] |
| Motley Fool Headlines | fool.com.au/recent-headlines | [✅/⚠️/❌] | [Top signal] |
| Motley Fool ASX 200 | fool.com.au/latest-asx-200-chart-price-news | [✅/⚠️/❌] | [Top signal] |
| Motley Fool Resources | fool.com.au/category/sector/resources-shares | [✅/⚠️/❌] | [Top signal] |
| Motley Fool Tech/Defence | fool.com.au/category/sector/tech-shares | [✅/⚠️/❌] | [Top signal or DRO count] |
| Motley Fool Industrials | fool.com.au/category/sector/industrials-shares | [✅/⚠️/❌] | [Top signal] |
| Motley Fool IPOs | fool.com.au/category/share-market-news/ipos | [✅/⚠️/❌] | IPO market: [ACTIVE/QUIET] |
| Motley Fool Reporting Calendar | fool.com.au/asx-reporting-season-calendar | [✅/⚠️/❌] | [Earnings risk status] |
| LiveWire Markets | livewiremarkets.com/shares | [✅/⚠️/❌] | [Top signal or "No watchlist mentions"] |
| Morningstar AU | morningstar.com.au/insights/stocks | [✅/⚠️/❌] | [Top signal] |
| SimplyWallSt Investing Ideas | simplywall.st/discover/au/investing-ideas | [✅/⚠️/❌] | [Quality tags found / unavailable] |
| SimplyWallSt Community | simplywall.st/community/narratives/au | [✅/⚠️/❌] | [Community narratives found / unavailable] |
| ASX Announcements | smallcaps.com.au/announcements | [✅/⚠️/❌] | [Announcement catalysts for watched tickers / none found] |
| SeekingAlpha Stock Ideas | seekingalpha.com/stock-ideas | [✅/⚠️ paywalled/❌] | [Tickers/themes visible before paywall / blocked] |
| Google Finance | google.com/finance/beta | [✅/⚠️ JS-blocked/❌] | [Index levels if visible / blocked] |
| SMH Markets | smh.com.au/business/markets | [✅/⚠️/❌] | [Top headline or macro signal] |
| PPAM Insights | ppam.com.au/news-insights | [✅/⚠️/❌] | [Fund manager view or unavailable] |
| Market Index Wraps | marketindex.com.au/news/category/market-wraps | [✅/⚠️/❌] | [ASX daily recap top movers / unavailable] |
| eToro Popular Stocks | etoro.com/discover/markets/stocks/popular | [✅/403 expected] | [Top-10 tickers / 403 bot-detection (expected — skipped)] |
| eToro News & Analysis | etoro.com/au/news-and-analysis | [✅/⚠️/❌] | [Headlines + tickers / blocked] |
| Moomoo Live News | moomoo.com/news/main/live (full URL with params) | [✅/⚠️ JS/❌] | [Live headlines / JS-blocked] |

### Macro Sources

| Data Point | Source | Value | Status |
|------------|--------|-------|--------|
| ASX 200 | Web search | [X] ([X]%) | ✅ |
| S&P 500 | Web search | [X] ([X]% prev close) | ✅ |
| VIX | Web search | [X] | [✅ / ⚠️ stale — note date] |
| WTI Oil | Web search | $[X] | ✅ |
| Gold (USD) | Web search | $[X]/oz | ✅ |
| Gold (AUD) | Calculated | $[X]/oz | [✅ / ⚠️ based on stale AUD/USD] |
| US Market Status | Finnhub API | [Open/Closed] | ✅ |

### Delivery

| Step | Status | Detail |
|------|--------|--------|
| Gmail draft | [✅/❌] | [Draft ID if success / error if fail] · To: david · cristina · ian · Self-contained report embedded inline |
| Log append | [✅/❌] | stock-watch-log.md · [DATETIME AEST] |

---
*Appendix generated: [TIME] AEST · [DATE] · Not financial advice*

---

