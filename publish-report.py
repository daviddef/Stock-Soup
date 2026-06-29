import os
#!/usr/bin/env python3
"""
publish-report.py — Publish a filled report HTML to GitHub Pages via git over HTTPS
=====================================================================================
Works from the Cowork sandbox (no local Mac clone required).
Uses a PAT stored in SKILL.md (GITHUB_PAT key) to authenticate.

USAGE (from SKILL.md STEP 4.5):
  python3 publish-report.py \
    --html /path/to/email-filled.html \
    --timestamp "2026-06-25-1501" \
    --picks "⚡KCN A$5.39 +4.6% · 📅RMS A$3.22 -3.01% · 📈MP1 A$20.94 | ⚡NEM $94 +1.5% · 📅WDAY $122 +9.2% · 📈MU $1134" \
    [--risk-off] \
    [--watchlist-status /path/to/watchlist-status.json]

WHAT IT DOES:
  1. git clone --depth=1 the Stock-Soup repo to /tmp/Stock-Soup
  2. Copies filled HTML → reports/{timestamp}.html
  3. Prepends entry to reports/report-index.json
  4. If --watchlist-status provided, writes watchlist-status.json to repo root
     (this is what the browser reads to colour-code the watchlist chips)
  5. git commit + push via HTTPS with PAT
  6. Cleans up /tmp/Stock-Soup
  7. Prints the live URL: https://daviddef.github.io/Stock-Soup/reports/{timestamp}.html
"""

import argparse, json, os, shutil, subprocess, sys
from datetime import datetime

REPO_URL_BASE  = "https://daviddef.github.io/Stock-Soup"
GITHUB_USER    = "daviddef"
GITHUB_REPO    = "Stock-Soup"
GITHUB_BRANCH  = "main"
GITHUB_PAT     = os.environ.get("GITHUB_PAT", "YOUR_GITHUB_PAT_HERE")  # real PAT stored in workspace copy
GIT_EMAIL      = "thestocksoup@gmail.com"
GIT_NAME       = "David DeFranceski"

def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}", file=sys.stderr)
        print(f"   stderr: {result.stderr.strip()}", file=sys.stderr)
        print(f"   stdout: {result.stdout.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html",             required=True,  help="Path to filled email HTML")
    parser.add_argument("--timestamp",        default=None,   help="e.g. 2026-06-25-1501. Defaults to datetime.now(AEST) if omitted.")
    parser.add_argument("--picks",            default="",     help="Rich format: '⚡ASX_DAY PRICE CHANGE · 📅ASX_WEEK PRICE CHANGE · 📈ASX_LONG PRICE CHANGE | ⚡GLB_DAY PRICE CHANGE · 📅GLB_WEEK PRICE CHANGE · 📈GLB_LONG PRICE CHANGE'. Use · between same-market picks, | between ASX and Global. Archive renders this as two labelled rows.")
    parser.add_argument("--risk-off",         action="store_true")
    parser.add_argument("--dry-run",          action="store_true", help="Skip git push")
    parser.add_argument("--watchlist-status", default=None,
                        help="Path to watchlist-status.json — written to repo root so browser chips get coloured")
    parser.add_argument("--email-data", default=None,
                        help="Path to email-data.json — auto-builds watchlist-status.json if --watchlist-status not given")
    parser.add_argument("--watchlist-json", default=None,
                        help="Path to watchlist.json — adds unresearched monitor tickers to status (optional)")
    # Legacy --repo arg accepted but ignored
    parser.add_argument("--repo", default=None, help="(ignored — sandbox uses git clone)")
    args = parser.parse_args()

    # ── Resolve timestamp ────────────────────────────────────────────
    from datetime import timezone, timedelta
    AEST = timezone(timedelta(hours=10))
    now_aest = datetime.now(AEST)

    if args.timestamp is None:
        # No timestamp supplied — use actual run time
        args.timestamp = now_aest.strftime("%Y-%m-%d-%H%M")
        print(f"ℹ️  Timestamp auto-generated from now(): {args.timestamp} AEST")
    elif "T" in args.timestamp:
        # Scheduled task passed ISO format (e.g. 2026-06-29T10:00:00+10:00)
        # Always override with actual current time so labels show real run time
        args.timestamp = now_aest.strftime("%Y-%m-%d-%H%M")
        print(f"ℹ️  ISO timestamp replaced with actual run time: {args.timestamp} AEST")
    # else: caller passed explicit YYYY-MM-DD-HHMM → use as-is

    clone_dir = "/tmp/Stock-Soup"

    # 1. Clone repo (shallow)
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    auth_url = f"https://{GITHUB_USER}:{GITHUB_PAT}@github.com/{GITHUB_USER}/{GITHUB_REPO}.git"
    print(f"📥 Cloning {GITHUB_USER}/{GITHUB_REPO}...")
    run(f'git clone --depth=1 "{auth_url}" "{clone_dir}"')
    run(f'git -C "{clone_dir}" config user.email "{GIT_EMAIL}"')
    run(f'git -C "{clone_dir}" config user.name "{GIT_NAME}"')
    print("✅ Cloned")

    # 2. Copy HTML to reports/
    reports_dir = os.path.join(clone_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    filename = f"{args.timestamp}.html"
    dest = os.path.join(reports_dir, filename)
    shutil.copy2(args.html, dest)
    print(f"✅ Copied report → reports/{filename}")

    # 3. Update report-index.json
    index_path = os.path.join(reports_dir, "report-index.json")
    try:
        with open(index_path) as f:
            index = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        index = []

    # Normalise timestamp to "Day DD Mon YYYY HH:MM AEST"
    label = args.timestamp  # fallback
    for fmt in ("%Y-%m-%d-%H%M", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            from datetime import timezone, timedelta
            AEST = timezone(timedelta(hours=10))
            dt = datetime.strptime(args.timestamp, fmt) if "T" not in args.timestamp else None
            if dt is None:
                import re as _re
                clean = _re.sub(r"\+\d{2}:\d{2}$", "", args.timestamp)
                dt = datetime.strptime(clean, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=AEST)
            label = dt.strftime("%a %d %b %Y %H:%M AEST").replace(" 0", " ")
            break
        except:
            continue

    entry = {
        "file":      filename,
        "timestamp": label,
        "label":     label,
        "picks":     args.picks,
        "riskOff":   args.risk_off,
    }
    index = [entry] + [e for e in index if e.get("file") != filename][:167]
    import re as _re2
    def _parse_label(e):
        lbl = e.get("label", e.get("timestamp", ""))
        try:
            from datetime import datetime as _dt2
            return _dt2.strptime(lbl.replace(" AEST",""), "%a %d %b %Y %H:%M")
        except:
            pass
        try:
            return datetime.fromisoformat(lbl.replace("Z","+00:00"))
        except:
            return datetime.min
    index.sort(key=_parse_label, reverse=True)
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
    print(f"✅ Updated report-index.json ({len(index)} entries)")

    # 3b. Staleness check — warn if etoro-instruments.json hasn't been synced recently
    import time as _time
    workspace_dir = "/Users/daviddefranceski/Claude/Projects/Share / Stock Trading"
    _etoro_local = os.path.join(workspace_dir, "etoro-instruments.json")
    if os.path.exists(_etoro_local):
        _age_days = (_time.time() - os.path.getmtime(_etoro_local)) / 86400
        if _age_days > 7:
            print(f"⚠️  etoro-instruments.json is {_age_days:.0f} days old — "
                  f"run: python3 etoro-watchlist-sync.py --publish", file=sys.stderr)
    else:
        print("⚠️  etoro-instruments.json not found in workspace — eToro chips may be missing", file=sys.stderr)

    # 3c. Sync user-guide.html from workspace (keeps live guide in sync with User_Guide.md edits)
    user_guide_src = os.path.join(workspace_dir, "user-guide.html")
    user_guide_dest = os.path.join(clone_dir, "user-guide.html")
    if os.path.exists(user_guide_src):
        shutil.copy2(user_guide_src, user_guide_dest)
        print("✅ Synced user-guide.html from workspace → GitHub Pages")
    else:
        print("⚠️  user-guide.html not found in workspace — live guide unchanged")

    # 4. Write watchlist-status.json (colours the browser chips)
    status_dest = os.path.join(clone_dir, "watchlist-status.json")

    # Resolve: explicit file > auto-build from email-data > skip
    status_src = args.watchlist_status

    # Auto-detect email-data.json: explicit arg > /tmp/email-data.json (skill default) > skip
    _email_data_path = args.email_data
    if not _email_data_path and os.path.exists('/tmp/email-data.json'):
        _email_data_path = '/tmp/email-data.json'
        print("ℹ️  Auto-detected /tmp/email-data.json for watchlist-status build")

    if not status_src and _email_data_path and os.path.exists(_email_data_path):
        # Auto-build watchlist-status.json inline from email-data.json
        try:
            from datetime import timezone, timedelta as _td
            _AEST = timezone(_td(hours=10))
            def _fmt_label(ts):
                try:
                    from datetime import datetime as _dt2
                    d2 = _dt2.strptime(ts, "%Y-%m-%d-%H%M")
                    return d2.strftime("%a %d %b %Y %H:%M AEST").replace(" 0", " ")
                except Exception:
                    return ts

            with open(_email_data_path) as _f:
                _d = json.load(_f)

            # Parse structured per-ticker research data written by the skill into WATCHLIST_DATA
            _wd = {}
            try:
                _wd_raw = _d.get('WATCHLIST_DATA', '')
                if _wd_raw:
                    _wd = json.loads(_wd_raw) if isinstance(_wd_raw, str) else _wd_raw
            except Exception:
                pass

            # Sentiment fallback by tier when skill hasn't set it explicitly
            _tier_sentiment = {'day': 'strong_buy', 'week': 'buy', 'long': 'buy', 'monitor': 'hold'}

            def _add(tickers, tk, pr, ch, sc, tier, pfx, note, market=''):
                t = _d.get(tk, '').strip()
                if not t: return
                p = _d.get(pr, '').strip()
                c = _d.get(ch, '').strip()
                s = str(_d.get(sc, '')).strip()
                # Narrative: try ASX_DAY_NARRATIVE, then bare DAY_NARRATIVE (both key styles used across skill versions)
                narr_key = tk.replace('_TICKER', '_NARRATIVE')
                narr_bare = narr_key.replace('ASX_', '').replace('GLB_', '')
                n = str(_d.get(narr_key, _d.get(narr_bare, note)))[:80]
                # Company name from *_COMPANY key (e.g. ASX_DAY_COMPANY, GLB_LONG_COMPANY)
                company = _d.get(tk.replace('_TICKER', '_COMPANY'), '').strip()
                entry = {'tier': tier, 'price': f"{pfx}{p}" if p else '—', 'change': c, 'score': s, 'note': n, 'market': market}
                if company:
                    entry['name'] = company
                # Merge structured research from WATCHLIST_DATA (overrides name if skill provided richer value)
                for _k in ('name', 'sentiment', 'rsi', 'trend', 'signals', 'news'):
                    if _k in _wd.get(t, {}):
                        entry[_k] = _wd[t][_k]
                # Ensure signals/news are always lists (skill may write them as strings)
                for _list_k in ('signals', 'news'):
                    if _list_k in entry and isinstance(entry[_list_k], str):
                        entry[_list_k] = [s.strip() for s in entry[_list_k].replace(' + ', '+').split('+') if s.strip()]
                if 'sentiment' not in entry:
                    entry['sentiment'] = _tier_sentiment.get(tier, 'hold')
                tickers[t] = entry

            _tickers = {}
            _add(_tickers,'ASX_DAY_TICKER', 'ASX_DAY_PRICE', 'ASX_DAY_CHANGE', 'DAY_SCORE',  'day',  'A$','⚡ DAY pick this run',  'ASX')
            _add(_tickers,'ASX_WEEK_TICKER','ASX_WEEK_PRICE','ASX_WEEK_CHANGE','WEEK_SCORE','week', 'A$','📅 WEEK pick this run', 'ASX')
            _add(_tickers,'ASX_LONG_TICKER','ASX_LONG_PRICE','ASX_LONG_CHANGE','LONG_SCORE','long', 'A$','📈 LONG pick this run',  'ASX')
            _add(_tickers,'GLB_DAY_TICKER', 'GLB_DAY_PRICE', 'GLB_DAY_CHANGE', 'DAY_SCORE',  'day',  '$', '⚡ DAY pick this run',  'GLOBAL')
            _add(_tickers,'GLB_WEEK_TICKER','GLB_WEEK_PRICE','GLB_WEEK_CHANGE','WEEK_SCORE','week', '$', '📅 WEEK pick this run', 'GLOBAL')
            _add(_tickers,'GLB_LONG_TICKER','GLB_LONG_PRICE','GLB_LONG_CHANGE','LONG_SCORE','long', '$', '📈 LONG pick this run',  'GLOBAL')

            # Add monitor tickers from watchlist.json — check arg, then cloned repo
            _wl_path = args.watchlist_json
            if not _wl_path:
                _repo_wl = os.path.join(clone_dir, 'watchlist.json')
                if os.path.exists(_repo_wl):
                    _wl_path = _repo_wl
            if _wl_path and os.path.exists(_wl_path):
                with open(_wl_path) as _wf:
                    for _item in json.load(_wf):
                        _t = _item.get('ticker','').strip()
                        if _t and _t not in _tickers:
                            entry = {'tier': 'monitor', 'price': '—', 'change': '—', 'score': '', 'note': 'Not researched this run'}
                            for _k in ('name', 'sentiment', 'rsi', 'trend', 'signals', 'news'):
                                if _k in _wd.get(_t, {}):
                                    entry[_k] = _wd[_t][_k]
                            # Ensure signals/news are always lists
                            for _list_k in ('signals', 'news'):
                                if _list_k in entry and isinstance(entry[_list_k], str):
                                    entry[_list_k] = [s.strip() for s in entry[_list_k].replace(' + ', '+').split('+') if s.strip()]
                            if 'sentiment' not in entry:
                                entry['sentiment'] = 'hold'
                            _tickers[_t] = entry

            _auto_status = {
                'run':     _fmt_label(args.timestamp) if args.timestamp else datetime.now(_AEST).strftime("%a %d %b %Y %H:%M AEST"),
                'report':  f"reports/{filename}",
                'tickers': _tickers,
            }
            _tmp_status = '/tmp/_watchlist-status-auto.json'
            with open(_tmp_status, 'w') as _sf:
                json.dump(_auto_status, _sf, indent=2)
            status_src = _tmp_status
            print(f"✅ Auto-built watchlist-status.json from email-data ({len(_tickers)} tickers)")
        except Exception as _e:
            print(f"⚠️  Auto-build of watchlist-status.json failed: {_e}", file=sys.stderr)

    if status_src:
        try:
            with open(status_src) as f:
                status_data = json.load(f)
            if not status_data.get("run"):
                status_data["run"] = args.timestamp
            if not status_data.get("report"):
                status_data["report"] = f"reports/{filename}"
            with open(status_dest, "w") as f:
                json.dump(status_data, f, indent=2)
            tickers_n = len(status_data.get("tickers", {}))
            print(f"✅ Updated watchlist-status.json ({tickers_n} tickers)")
        except Exception as e:
            print(f"⚠️  Could not write watchlist-status.json: {e}", file=sys.stderr)
    else:
        print("ℹ️  No watchlist-status source — pass --email-data or --watchlist-status to activate chips")

    # 5. Commit and push
    commit_msg = f"report: {args.timestamp} — {args.picks}"
    if args.risk_off:
        commit_msg += " ⚠️ RISK-OFF"

    run(f'git -C "{clone_dir}" add -A')
    rc, out, err = run(f'git -C "{clone_dir}" commit -m "{commit_msg}"', check=False)
    if rc != 0 and "nothing to commit" in err + out:
        print("ℹ️  Nothing new to commit (report already published)")
    else:
        if not args.dry_run:
            run(f'git -C "{clone_dir}" push "{auth_url}" {GITHUB_BRANCH}')
            url = f"{REPO_URL_BASE}/reports/{filename}"
            print(f"✅ Pushed to GitHub Pages")
            print(f"🔗 {url}")
            print(url)
        else:
            print(f"[dry-run] Would push: {commit_msg}")

    # 6. Cleanup
    shutil.rmtree(clone_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
