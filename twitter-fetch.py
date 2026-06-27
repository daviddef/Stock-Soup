#!/usr/bin/env python3
"""
twitter-fetch.py — Twitter/X v2 API social signal collector
============================================================
Searches for ASX + US stock ticker mentions on Twitter/X.
Runs via GitHub Actions (scheduled hourly) or locally.
Outputs: twitter-signals.json (committed to repo → Claude reads via web_fetch)

USAGE (local): python3 twitter-fetch.py
USAGE (GitHub Actions): see .github/workflows/twitter-fetch.yml

AUTH: Bearer Token (App-only) for search/recent endpoint.
OAuth 1.0a credentials (Consumer Key/Secret + Access Token/Secret) are
available for user-context endpoints if needed later.
"""

import json, os, sys, time, urllib.request, urllib.parse
from datetime import datetime, timezone

# ── CONFIG ──────────────────────────────────────────────────────
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")

# Tickers to search — keep to 6–8 per run to stay inside rate limits
# These are injected fresh each run from the active picks + watchlist
SEARCH_TICKERS = [
    ("EOS", "ASX"),
    ("4DX", "ASX"),
    ("TLX", "ASX"),
    ("DRO", "ASX"),
    ("PLTR", "NASDAQ"),
    ("NVDA", "NASDAQ"),
]

# Additional broad ASX sentiment queries
BROAD_QUERIES = [
    ("ASX bulls today", "ASX_SENTIMENT"),
    ("ASX buy recommendation", "ASX_RECO"),
]

MIN_LIKES = 2  # filter noise — only include tweets with ≥2 likes

# ── TWITTER API ─────────────────────────────────────────────────
def bearer_headers():
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "User-Agent": "StockSoupBot/1.0"
    }

def search_recent(query, max_results=15):
    """Search Twitter recent tweets (last 7 days). Returns list of tweet dicts."""
    params = urllib.parse.urlencode({
        "query": query + " -is:retweet lang:en",
        "tweet.fields": "public_metrics,created_at,author_id",
        "expansions": "author_id",
        "user.fields": "username,public_metrics",
        "max_results": max_results,
    })
    url = f"https://api.twitter.com/2/tweets/search/recent?{params}"
    req = urllib.request.Request(url, headers=bearer_headers())
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"error": f"HTTP {e.code}: {body[:200]}"}
    except Exception as e:
        return {"error": str(e)}

def score_sentiment(text):
    """Simple keyword-based sentiment. Returns: BULLISH / BEARISH / NEUTRAL."""
    t = text.lower()
    bull = sum(t.count(w) for w in ["buy","bullish","long","breakout","surge","rocket","moon","rally","hold","strong","upgrade","catalyst"])
    bear = sum(t.count(w) for w in ["sell","bearish","short","crash","dump","drop","warning","downgrade","avoid","risk","overvalued"])
    if bull > bear: return "BULLISH"
    if bear > bull: return "BEARISH"
    return "NEUTRAL"

# ── MAIN ─────────────────────────────────────────────────────────
def main():
    if not BEARER_TOKEN:
        print("ERROR: TWITTER_BEARER_TOKEN env var not set", file=sys.stderr)
        sys.exit(1)

    results = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tickers": {},
        "broad": {},
        "summary": {}
    }

    # Per-ticker searches
    for ticker, exchange in SEARCH_TICKERS:
        query = f"${ticker}" if exchange in ("NASDAQ","NYSE") else f"{ticker} ASX"
        print(f"  Searching: {query}...", flush=True)
        raw = search_recent(query, 15)
        time.sleep(1.2)  # respect rate limits

        if "error" in raw:
            results["tickers"][ticker] = {"status": "error", "error": raw["error"]}
            continue

        tweets = raw.get("data", [])
        users  = {u["id"]: u for u in raw.get("includes", {}).get("users", [])}

        filtered = []
        bull_count = bear_count = 0
        for t in tweets:
            m = t.get("public_metrics", {})
            if m.get("like_count", 0) < MIN_LIKES and m.get("retweet_count", 0) < 1:
                continue
            sentiment = score_sentiment(t["text"])
            if sentiment == "BULLISH": bull_count += 1
            if sentiment == "BEARISH": bear_count += 1
            author = users.get(t.get("author_id", ""), {})
            filtered.append({
                "text": t["text"][:200],
                "created_at": t["created_at"],
                "likes": m.get("like_count", 0),
                "retweets": m.get("retweet_count", 0),
                "sentiment": sentiment,
                "author_followers": author.get("public_metrics", {}).get("followers_count", 0),
                "author": author.get("username", "unknown")
            })

        # Sort by engagement
        filtered.sort(key=lambda x: x["likes"] + x["retweets"] * 3, reverse=True)
        net = "BULLISH" if bull_count > bear_count else ("BEARISH" if bear_count > bull_count else "NEUTRAL")
        results["tickers"][ticker] = {
            "exchange": exchange,
            "query": query,
            "tweet_count": len(filtered),
            "bullish": bull_count,
            "bearish": bear_count,
            "net_sentiment": net,
            "top_tweets": filtered[:5]
        }
        results["summary"][ticker] = {"sentiment": net, "tweets": len(filtered), "bull": bull_count, "bear": bear_count}

    # Broad sentiment queries
    for label, key in BROAD_QUERIES:
        print(f"  Broad: {label}...", flush=True)
        raw = search_recent(label, 10)
        time.sleep(1.2)
        if "error" not in raw:
            tweets = raw.get("data", [])
            results["broad"][key] = {
                "query": label,
                "count": len(tweets),
                "headlines": [t["text"][:150] for t in tweets[:5]]
            }

    out = json.dumps(results, indent=2)
    with open("twitter-signals.json", "w") as f:
        f.write(out)
    print(f"\n✅ twitter-signals.json written ({len(results['tickers'])} tickers)")
    print("Summary:", json.dumps(results["summary"], indent=2))

if __name__ == "__main__":
    main()
