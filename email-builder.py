#!/usr/bin/env python3
"""
email-builder.py — ASX Stock Watch email generator
====================================================
Reads email-template.html and substitutes ALL [PLACEHOLDER] tokens
with values from a JSON data file.

USAGE (from SKILL.md STEP 4):
  python3 "/Users/daviddefranceski/Claude/Projects/Share / Stock Trading/email-builder.py" /tmp/email-data.json

The layout NEVER changes — it always comes from email-template.html.
Only the [PLACEHOLDER] values change each run.

STEP 4 workflow in SKILL.md:
  1. Build this-run values as a Python/JSON dict (see ALL_PLACEHOLDERS below)
  2. Write to /tmp/email-data.json
  3. Run: python3 email-builder.py /tmp/email-data.json
  4. Capture stdout → that is the htmlBody for the Gmail draft
  5. Pass to mcp__50d2dafb-c212-41e5-b526-3b9284a2bb55__create_draft
"""

import json, sys, os, re

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "email-template.html")

# ALL VALID PLACEHOLDERS — fill these each run, leave unknown ones as-is
ALL_PLACEHOLDERS = [
    # Geopolitical briefing (Section 1.5 — rendered as pre-built HTML block)
    "GEO_SECTION",
    # Meta
    "TIME AEST", "DATE", "TIMESTAMP", "NEXT_TIME AEST",
    # Macro
    "ASX200_VALUE", "ASX200_CHANGE", "ASX200_NOTE",
    "VIX_VALUE", "VIX_CHANGE", "VIX_NOTE",
    "GOLD_USD", "GOLD_CHANGE", "GOLD_NOTE",
    "OIL_VALUE", "OIL_CHANGE", "OIL_NOTE",
    "AUDUSD_RATE", "AUDUSD_NOTE", "AUDUSD_SIGNAL",
    "PLTR_PRICE", "PLTR_CHANGE", "PLTR_NOTE",
    # Candidates summary
    "N_TOTAL", "N_VOL", "N_ANN", "N_NEWS", "N_SECTOR", "N_US", "N_MEDIA", "N_SWS", "N_TV", "N_WATCH",
    # ASX Day pick
    "ASX_DAY_TICKER", "ASX_DAY_COMPANY", "ASX_DAY_PRICE", "ASX_DAY_CHANGE",
    "DAY_ENTRY", "DAY_TARGET", "DAY_STOP", "DAY_RR",
    "DAY_CATALYST_BADGES", "DAY_NARRATIVE",
    "DAY_CATALYST_1", "DAY_CATALYST_2", "DAY_CATALYST_3", "DAY_CATALYST_4",
    "DAY_SPECIFIC_RISK", "DAY_TKR", "DAY_NEW_HOLD",
    # ASX Week pick
    "ASX_WEEK_TICKER", "ASX_WEEK_COMPANY", "ASX_WEEK_PRICE", "ASX_WEEK_CHANGE",
    "WEEK_ENTRY", "WEEK_TARGET", "WEEK_STOP", "WEEK_RR",
    "WEEK_CATALYST_BADGES", "WEEK_NARRATIVE",
    "WEEK_CATALYST_1", "WEEK_CATALYST_2", "WEEK_CATALYST_3", "WEEK_CATALYST_4",
    "WEEK_SPECIFIC_RISK", "WEEK_TKR", "WEEK_NEW_HOLD",
    # ASX Long pick
    "ASX_LONG_TICKER", "ASX_LONG_COMPANY", "ASX_LONG_PRICE", "ASX_LONG_CHANGE",
    "LONG_ENTRY", "LONG_TARGET", "LONG_STOP", "LONG_RR",
    "LONG_CATALYST_BADGES", "LONG_NARRATIVE",
    "LONG_CATALYST_1", "LONG_CATALYST_2", "LONG_CATALYST_3", "LONG_CATALYST_4",
    "LONG_SPECIFIC_RISK", "LONG_TKR", "LONG_NOTE", "ASX_LONG_NOTE", "LONG_NEW_HOLD",
    # Global Day pick
    "GLB_DAY_TICKER", "GLB_DAY_COMPANY", "GLB_DAY_EXCHANGE",
    "GLB_DAY_PRICE", "GLB_DAY_CHANGE",
    "GLB_DAY_ENTRY", "GLB_DAY_TARGET", "GLB_DAY_STOP", "GLB_DAY_RR",
    "GLB_DAY_CATALYST_BADGES", "GLB_DAY_NARRATIVE",
    "GLB_DAY_CATALYST_1", "GLB_DAY_CATALYST_2", "GLB_DAY_CATALYST_3",
    "GLB_DAY_SPECIFIC_RISK", "GLB_DAY_NEW_HOLD",
    # Global Week pick
    "GLB_WEEK_TICKER", "GLB_WEEK_COMPANY", "GLB_WEEK_EXCHANGE",
    "GLB_WEEK_PRICE", "GLB_WEEK_CHANGE",
    "GLB_WEEK_ENTRY", "GLB_WEEK_TARGET", "GLB_WEEK_STOP", "GLB_WEEK_RR",
    "GLB_WEEK_CATALYST_BADGES", "GLB_WEEK_NARRATIVE",
    "GLB_WEEK_CATALYST_1", "GLB_WEEK_CATALYST_2", "GLB_WEEK_CATALYST_3",
    "GLB_WEEK_SPECIFIC_RISK", "GLB_WEEK_NEW_HOLD",
    # Global Long pick
    "GLB_LONG_TICKER", "GLB_LONG_COMPANY", "GLB_LONG_EXCHANGE",
    "GLB_LONG_PRICE", "GLB_LONG_CHANGE",
    "GLB_LONG_ENTRY", "GLB_LONG_TARGET", "GLB_LONG_STOP", "GLB_LONG_RR",
    "GLB_LONG_CATALYST_BADGES", "GLB_LONG_NARRATIVE",
    "GLB_LONG_CATALYST_1", "GLB_LONG_CATALYST_2", "GLB_LONG_CATALYST_3",
    "GLB_LONG_SPECIFIC_RISK", "GLB_LONG_NOTE", "GLB_LONG_NEW_HOLD",
    # Portfolio alert (only when triggered)
    "ALERT_TICKER", "ALERT_COMPANY", "ALERT_PRICE", "ALERT_MOVE", "SPECIFIC_ACTION_RECOMMENDATION",
    # Watchlist scan rows (build as HTML string for [WATCHLIST_ROWS])
    "WATCHLIST_ROWS",
    # Sector heat map rows
    "SECTOR_1", "STRENGTH_1", "NAMES_1", "SIGNAL_1",
    "SECTOR_2", "STRENGTH_2", "NAMES_2", "SIGNAL_2",
    "SECTOR_3", "STRENGTH_3", "NAMES_3", "SIGNAL_3",
    "SECTOR_4", "STRENGTH_4", "NAMES_4", "SIGNAL_4",
    # ASX Announcements
    "ANN_TICKER_1", "ANN_DETAIL_1",
    "ANN_TICKER_2", "ANN_DETAIL_2",
    "ANN_TICKER_3", "ANN_DETAIL_3",
    # IPO (conditional)
    "IPO_COMPANY", "IPO_CODE", "IPO_DATE", "IPO_PRICE", "IPO_SECTOR",
    # Dividends (conditional)
    "DIV_TICKER", "DIV_AMT", "DIV_DATE", "DIV_YIELD",
    # Data sources table rows
    "SOURCES_ROWS",
    # Section 15 decision logic
    "S15A_ROWS",       # All tickers evaluated table rows (HTML)
    "S15B_ASX_POOL",   # ASX runner-up logic text
    "S15B_GLB_POOL",   # Global runner-up logic text
    "S15C_SUMMARY",    # "N attempted · N ✅ · N ⚠️ · N ❌"
    # eToro external watchlist (auto-built from SKILL.md)
    "ETORO_WATCHLIST_ROWS",
    # Historical win rate (auto-computed from stock-watch-log.md by win-rate.py)
    "WIN_RATE_SUMMARY",
    # Misc template vars
    "RUNNER_UP", "TICKERS", "WHY", "SIGNAL", "STATUS",
    "TKR", "TKR1", "TKR2", "MONITOR_TKR",
    "RSI", "SMA", "VOL", "TICKER",
]


ETORO_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "etoro-instruments.json")
WIN_RATE_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills", "win-rate.py")

# Asset type ID → label
ASSET_TYPE_LABELS = {
    1: "Forex", 2: "Commodity", 3: "CFD", 4: "Index",
    5: "Stock", 6: "ETF", 10: "Crypto",
}

def build_etoro_rows(live_prices=None):
    """Read etoro-instruments.json → HTML rows grouped by watchlist.
    live_prices: optional dict of {symbol: price_float} from the hourly run.
    If not provided, prices column shows sync date note instead.
    """
    try:
        with open(ETORO_JSON_PATH, "r", encoding="utf-8") as f:
            etoro = json.load(f)
    except FileNotFoundError:
        return '<tr><td colspan="5" style="padding:8px;color:#888;font-style:italic;">etoro-instruments.json not found — run etoro-watchlist-sync first</td></tr>'

    instruments_data = etoro.get("instruments", {})
    synced = etoro.get("synced", "unknown")
    if not instruments_data:
        return '<tr><td colspan="5" style="padding:8px;color:#888;font-style:italic;">No instruments in etoro-instruments.json</td></tr>'

    from collections import defaultdict
    grouped = defaultdict(list)
    for sym, v in instruments_data.items():
        grouped[v.get("watchlist", "Other")].append({
            "sym": sym, "name": v.get("displayName", sym),
            "type": v.get("type", ""), "wl": v.get("watchlist", "Other")
        })

    # Use the order recorded by etoro-watchlist-sync (from the live API response),
    # falling back to alphabetical for any groups not in that list.
    watchlist_order = etoro.get("watchlist_order", [])
    ordered_wls = [w for w in watchlist_order if w in grouped]
    ordered_wls += sorted(w for w in grouped if w not in watchlist_order)

    html_rows = []
    row_idx = 0
    for wl_name in ordered_wls:
        html_rows.append(
            f'<tr><td colspan="5" style="padding:5px 8px;background-color:#eef1f5;font-weight:bold;font-size:11px;color:#1a2332;border-top:2px solid #1a2332;">' + wl_name + '</td></tr>'
        )
        for inst in sorted(grouped[wl_name], key=lambda x: x["sym"]):
            bg = '#ffffff' if row_idx % 2 == 0 else '#fafafa'
            # Price from live_prices if provided, else show dash with sync note
            price_display = '<span style="color:#aaa;">—</span>'
            if live_prices and inst["sym"] in live_prices:
                pf = live_prices[inst["sym"]]
                try:
                    pf = float(pf)
                    if pf > 0:
                        price_display = f'${pf:,.4f}'.rstrip('0').rstrip('.') if pf < 10 else f'${pf:,.2f}'
                except (ValueError, TypeError):
                    pass
            html_rows.append(
                f'<tr style="background-color:{bg};">' +
                f'<td style="padding:5px 8px;font-weight:bold;">{inst["sym"]}</td>' +
                f'<td style="padding:5px 8px;color:#444;">{inst["name"]}</td>' +
                f'<td style="padding:5px 8px;font-size:11px;color:#666;">{inst["type"]}</td>' +
                f'<td style="padding:5px 8px;font-family:monospace;">{price_display}</td>' +
                f'<td style="padding:5px 8px;font-size:11px;color:#555;">{inst["wl"]}</td>' +
                '</tr>'
            )
            row_idx += 1

    return "\n      ".join(html_rows)

def _auto_win_rate():
    """Run win-rate.py --json and format a one-line HTML summary for [WIN_RATE_SUMMARY]."""
    import subprocess
    if not os.path.exists(WIN_RATE_SCRIPT):
        return "📊 Win rate: not available (win-rate.py not found)"
    try:
        result = subprocess.run(
            ["python3", WIN_RATE_SCRIPT, "--json", "--days", "90"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return "📊 Win rate: error running win-rate.py"
        r = json.loads(result.stdout)
        overall  = r.get("win_rate_pct", "—")
        wins     = r.get("wins", "—")
        losses   = r.get("losses", "—")
        open_    = r.get("open", "—")
        asx_wr   = r.get("asx", {}).get("win_rate_pct", "—")
        glb_wr   = r.get("global", {}).get("win_rate_pct", "—")
        days     = r.get("window_days", 90)
        return (f"📊 Win rate (last {days}d): <b>{overall}%</b> &nbsp;·&nbsp; "
                f"✅{wins}W / ❌{losses}L / ⏳{open_} open &nbsp;·&nbsp; "
                f"🇦🇺 ASX {asx_wr}% &nbsp;·&nbsp; 🌏 Global {glb_wr}%")
    except Exception as e:
        return f"📊 Win rate: unavailable ({e})"


def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def handle_conditional_sections(html, data):
    """
    Remove optional sections if show flag is False/absent.
    Template wraps optional sections in:
      <!-- SECTION_START: NAME -->..content..<!-- SECTION_END: NAME -->
    """
    sections = {
        "PORTFOLIO_ALERT":   data.get("SHOW_PORTFOLIO_ALERT", False),
        "IPO_SECTION":       data.get("SHOW_IPO_SECTION", False),
        "DIVIDENDS_SECTION": data.get("SHOW_DIVIDENDS_SECTION", False),
        "RISK_OFF_BANNER":   data.get("SHOW_RISK_OFF", True),
    }
    for name, show in sections.items():
        start = f"<!-- SECTION_START: {name} -->"
        end   = f"<!-- SECTION_END: {name} -->"
        if start in html:
            if not show:
                pattern = re.compile(
                    re.escape(start) + r".*?" + re.escape(end), re.DOTALL
                )
                html = pattern.sub("", html)
            else:
                html = html.replace(start, "").replace(end, "")
    return html

def substitute(html, data):
    # Auto-generate _CHANGE_COLOR tokens: red for negative, green for positive
    auto_colors = {}
    for key, value in data.items():
        if key.endswith('_CHANGE') and isinstance(value, str):
            color_key = key + '_COLOR'
            if color_key not in data:
                stripped = value.lstrip('~').strip()
                auto_colors[color_key] = '#c53030' if stripped.startswith('-') else '#007a55'
    data = {**data, **auto_colors}

    # Auto-strip currency prefixes from ASX prices (template already adds A$ prefix)
    asx_price_keys = ['ASX_DAY_PRICE', 'ASX_WEEK_PRICE', 'ASX_LONG_PRICE']
    for key in asx_price_keys:
        if key in data and isinstance(data[key], str):
            data[key] = data[key].lstrip('A$').lstrip('$').lstrip('~').strip()

    # Auto-strip $ prefix from Global prices (template already adds $)
    # Strip currency prefixes from ALL keys the template prefixes with $ or A$
    dollar_prefix_keys = [
        'DAY_ENTRY','DAY_TARGET','DAY_STOP',
        'WEEK_ENTRY','WEEK_TARGET','WEEK_STOP',
        'LONG_ENTRY','LONG_TARGET','LONG_STOP',
        'GLB_DAY_PRICE','GLB_DAY_ENTRY','GLB_DAY_TARGET','GLB_DAY_STOP',
        'GLB_WEEK_PRICE','GLB_WEEK_ENTRY','GLB_WEEK_TARGET','GLB_WEEK_STOP',
        'GLB_LONG_PRICE','GLB_LONG_ENTRY','GLB_LONG_TARGET','GLB_LONG_STOP',
        'PLTR_PRICE',
    ]
    for key in dollar_prefix_keys:
        if key in data and isinstance(data[key], str):
            data[key] = data[key].lstrip('~').lstrip('A$').lstrip('$').strip()

    for key, value in data.items():
        html = html.replace(f"[{key}]", str(value))
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 email-builder.py <data.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    html = load_template()
    html = handle_conditional_sections(html, data)
    # Auto-populate eToro external watchlist
    if "[ETORO_WATCHLIST_ROWS]" in html:
        live_prices = data.get("ETORO_LIVE_PRICES", None)
        data.setdefault("ETORO_WATCHLIST_ROWS", build_etoro_rows(live_prices))
    # Auto-compute win rate from stock-watch-log.md
    if "[WIN_RATE_SUMMARY]" in html:
        data.setdefault("WIN_RATE_SUMMARY", _auto_win_rate())
    html = substitute(html, data)

    # Report unfilled placeholders (excluding known format-only tokens)
    ignore = {"COLOR", "RED_IF_NEG_ELSE_GREEN"}
    remaining = [r for r in re.findall(r'\[[A-Z][A-Z0-9_ ]+\]', html) if r.strip("[]") not in ignore]
    if remaining:
        print(f"⚠️  {len(remaining)} unfilled placeholders: {sorted(set(remaining))}", file=sys.stderr)

    print(html)

if __name__ == "__main__":
    main()
