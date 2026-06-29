#!/usr/bin/env python3
"""
etoro-watchlist-sync.py — Fetch eToro watchlists and optionally publish to GitHub Pages
========================================================================================

USAGE:
  python3 etoro-watchlist-sync.py            # Print summary only (no publish)
  python3 etoro-watchlist-sync.py --publish  # Fetch, print, AND push etoro-watchlist.json to Stock-Soup repo

WHAT IT DOES (--publish):
  1. Fetches all eToro watchlists via public API
  2. Fetches live rates for each instrument
  3. Writes etoro-watchlist.json to the Stock-Soup GitHub repo
     → Browser at daviddef.github.io/Stock-Soup reads this to display the eToro chips section
  4. Git commits and pushes via PAT

Run this whenever your eToro watchlists change. The hourly research skill reads the same
watchlist.json + etoro-watchlist.json from the repo each run.
"""
import requests, uuid, json, os, shutil, subprocess, sys, argparse
from datetime import datetime, timezone, timedelta

API_KEY  = "sdgdskldFPLGfjHn1421dgnlxdGTbngdflg6290bRjslfihsjhSDsdgGHH25hjf"
USER_KEY = "eyJjaSI6IjYwY2FiYjBiLTU1OTctNDQ4NS04ZjYzLTdlOWUwNTZlMGJiOCIsImVhbiI6IlVucmVnaXN0ZXJlZEFwcGxpY2F0aW9uIiwiZWsiOiJqQ2lqT3BoMno1cGlOZ3NHLWhvRVJhbWEwRzd6b2ttWFJJV1Qxek85UTF3THY5MjR2UlZpcVRsUFVmMS1WNEQubTFmanJTRnB6QW9nbmJneDVHZzJCTHc0clRCVkNRVlR6NEFRYlRwLlNwQV8ifQ__"
BASE     = "https://public-api.etoro.com/api/v1"

GITHUB_USER   = "daviddef"
GITHUB_REPO   = "Stock-Soup"
GITHUB_BRANCH = "main"
GITHUB_PAT    = os.environ.get("GITHUB_PAT", "YOUR_GITHUB_PAT_HERE")  # real PAT stored in workspace copy
GIT_EMAIL     = "thestocksoup@gmail.com"
GIT_NAME      = "David DeFranceski"

# Map eToro exchange codes / asset types to display exchange labels
ASSET_TYPES = {1:"Forex", 2:"Commodity", 3:"CFD", 4:"Index", 5:"Stock", 6:"ETF", 7:"Bond", 8:"Fund", 9:"Option"}
EXCHANGE_MAP = {
    # String codes from eToro
    "US":    "NYSE",
    "NASDAQ":"NASDAQ",
    "ASX":   "ASX",
    "LSE":   "LSE",
    "XASX":  "ASX",
    "XNAS":  "NASDAQ",
    "XNYS":  "NYSE",
    # Numeric exchangeId values from eToro API
    "2":  "COMDTY",   # Commodities (GOLD, SILVER, OIL)
    "3":  "INDEX",    # Indices (NSDQ100, SPX500)
    "4":  "NASDAQ",   # US stocks — NASDAQ tier
    "5":  "NYSE",     # US stocks — NYSE tier
    "8":  "CRYPTO",   # Cryptocurrency
    "9":  "EU",       # European exchanges
    "12": "SIX",      # Swiss Exchange
    "20": "ETF",      # ETFs
    "21": "HKEX",     # Hong Kong Exchange
    "31": "ASX",      # ASX (e.g. RIO.ASX)
}


def hdrs():
    return {"x-api-key": API_KEY, "x-user-key": USER_KEY,
            "x-request-id": str(uuid.uuid4()), "Accept": "application/json"}


def get(path, params=None):
    r = requests.get(f"{BASE}{path}", headers=hdrs(), params=params, timeout=12)
    return r.json() if r.status_code == 200 else None


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def run_git(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ git: {cmd}", file=sys.stderr)
        print(f"   {result.stderr.strip()}", file=sys.stderr)
    return result.returncode, result.stdout.strip()


def infer_exchange(market: dict) -> str:
    """Best-effort exchange label from eToro market data."""
    ex_code = str(market.get("exchangeId") or market.get("exchange") or "").upper()
    mapped = EXCHANGE_MAP.get(ex_code)
    if mapped:
        return mapped
    # Fall back to asset type + symbol heuristics
    sym = market.get("symbolName", "")
    if sym.endswith(".AU") or ex_code == "XASX":
        return "ASX"
    atype = market.get("assetTypeId", 0)
    if atype == 1:
        return "FOREX"
    return ex_code or "OTHER"



def _get_watchlist_tickers():
    """Fetch ASX watchlist tickers from watchlist.json on GitHub — used to compute not_on_etoro."""
    try:
        url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/watchlist.json"
        r = requests.get(url, timeout=10)
        data = r.json()
        # watchlist.json is [{ticker, exchange, name}, ...]
        return [item["ticker"] for item in data if isinstance(item, dict) and "ticker" in item]
    except Exception as e:
        print(f"⚠️  Could not fetch watchlist.json for not_on_etoro calc: {e}")
        return []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true",
                        help="Push etoro-watchlist.json to GitHub after fetching")
    args = parser.parse_args()

    AEST = timezone(timedelta(hours=10))
    now_str = datetime.now(AEST).isoformat()

    # ── 1. Fetch all watchlists ────────────────────────────────────
    data = get("/watchlists")
    if not data:
        print("ERROR: Could not fetch eToro watchlists — check API keys", file=sys.stderr)
        sys.exit(1)

    watchlists_raw = data.get("watchlists", [])
    all_instruments = {}   # sym → {id, name, exchange, type, watchlist}

    print("=" * 70)
    print(f"eToro Watchlists — {len(watchlists_raw)} list(s) — {now_str}")
    print("=" * 70)

    result_watchlists = []

    for wl in watchlists_raw:
        wl_name = wl.get("name", "?")
        wl_type = wl.get("watchlistType", "")
        items   = wl.get("items", [])
        print(f"\n📋 {wl_name} ({len(items)} items, type={wl_type})")
        print(f"   {'Symbol':<14} {'Exchange':<10} {'Display Name'}")
        print(f"   {'-'*14} {'-'*10} {'-'*30}")

        result_items = []
        for item in items:
            market = item.get("market", {})
            sym    = market.get("symbolName", "")
            iid    = market.get("id") or item.get("itemId")
            name   = market.get("displayName", "")
            atype  = market.get("assetTypeId", 0)
            ex     = infer_exchange(market)
            if sym and sym != "?" and iid:
                all_instruments[sym] = {
                    "id": int(iid), "name": name, "type": atype,
                    "exchange": ex, "watchlist": wl_name
                }
                result_items.append({"ticker": sym, "exchange": ex, "name": name, "id": int(iid)})
            print("   %-14s %-10s %s" % (sym or "?", ex, name))

        result_watchlists.append({"name": wl_name, "items": result_items})

    # ── 2. Fetch live rates ────────────────────────────────────────
    ids = [str(v["id"]) for v in all_instruments.values()]
    live = {}
    for batch in chunks(ids, 20):
        r = requests.get(
            f"{BASE}/market-data/instruments/rates?instrumentIds={','.join(batch)}",
            headers=hdrs(), timeout=12
        )
        if r.status_code == 200:
            for rate in r.json().get("rates", []):
                live[rate["instrumentID"]] = rate

    print(f"\n{'Symbol':<14} {'Exchange':<10} {'Last':<14} {'Ask':<14} {'Bid':<14} Updated")
    print(f"{'-'*14} {'-'*10} {'-'*14} {'-'*14} {'-'*14} {'-'*19}")
    for sym, info in sorted(all_instruments.items()):
        rate = live.get(info["id"], {})
        print(f"{sym:<14} {info['exchange']:<10} {str(rate.get('lastExecution','—')):<14} "
              f"{str(rate.get('ask','—')):<14} {str(rate.get('bid','—')):<14} "
              f"{str(rate.get('date','—'))[:19]}")

    # ── 3a. Build etoro-watchlist.json (with rates — for browser display) ──
    output = {
        "last_synced": now_str,
        "watchlists":  result_watchlists
    }

    # ── 3b. Build etoro-instruments.json (no prices — for hourly skill/email-builder) ──
    WORKSPACE = "/Users/daviddefranceski/Claude/Projects/Share / Stock Trading"
    instruments_output = {
        "synced": datetime.now(AEST).strftime("%Y-%m-%d"),
        "source": "eToro watchlist API — /watchlists + /market-data/instruments/rates",
        # Preserve the API response order so email-builder can display groups in the same sequence
        "watchlist_order": [wl.get("name") for wl in result_watchlists],
        "instruments": {
            sym: {
                "id":          info["id"],
                "displayName": info["name"],
                "type": {5: "Stock/ETF", 6: "Stock/ETF", 10: "Crypto",
                         1: "Forex/Index/Commodity", 2: "Forex/Index/Commodity",
                         3: "Forex/Index/Commodity", 4: "Forex/Index/Commodity"}.get(info["type"], "Other"),
                "watchlist":   info["watchlist"]
            }
            for sym, info in all_instruments.items()
        },
        "not_on_etoro": sorted([
            t for t in _get_watchlist_tickers()
            if t not in all_instruments
        ])
    }
    local_json = os.path.join(WORKSPACE, "etoro-instruments.json")
    with open(local_json, "w") as f:
        json.dump(instruments_output, f, indent=2)
    print(f"✅ etoro-instruments.json written locally ({len(all_instruments)} instruments)")

    print("\n" + "=" * 70)
    print(f"Total instruments: {len(all_instruments)} across {len(result_watchlists)} watchlist(s)")
    print("=" * 70)

    if not args.publish:
        print("\n💡 Run with --publish to push etoro-watchlist.json to GitHub Pages")
        print(json.dumps(output, indent=2)[:600] + "…")
        return

    # ── 4. Publish to GitHub ──────────────────────────────────────
    clone_dir = "/tmp/Stock-Soup-etoro"
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)

    auth_url = f"https://{GITHUB_USER}:{GITHUB_PAT}@github.com/{GITHUB_USER}/{GITHUB_REPO}.git"
    print(f"\n📥 Cloning {GITHUB_REPO}…")
    run_git(f'git clone --depth=1 "{auth_url}" "{clone_dir}"')
    run_git(f'git -C "{clone_dir}" config user.email "{GIT_EMAIL}"')
    run_git(f'git -C "{clone_dir}" config user.name "{GIT_NAME}"')

    dest = os.path.join(clone_dir, "etoro-watchlist.json")
    with open(dest, "w") as f:
        json.dump(output, f, indent=2)
    print(f"✅ Wrote etoro-watchlist.json ({len(all_instruments)} instruments)")

    # Copy etoro-instruments.json to repo
    instr_src = os.path.join(WORKSPACE, 'etoro-instruments.json')
    instr_dst = os.path.join(clone_dir, 'etoro-instruments.json')
    shutil.copy(instr_src, instr_dst)
    run_git(f'git -C "{clone_dir}" add etoro-watchlist.json etoro-instruments.json')
    rc, out = run_git(
        f'git -C "{clone_dir}" commit -m "sync: eToro watchlist — {now_str[:16]} — {len(all_instruments)} instruments"',
        cwd=clone_dir
    )
    if rc == 0:
        run_git(f'git -C "{clone_dir}" push "{auth_url}" {GITHUB_BRANCH}')
        print(f"✅ Pushed — chips will update at daviddef.github.io/Stock-Soup within ~60s")
    else:
        print("ℹ️  Nothing changed in eToro watchlist since last sync")

    shutil.rmtree(clone_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
