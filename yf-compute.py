#!/usr/bin/env python3
"""
yf-compute.py — Yahoo Finance signal computer
==============================================
Replaces yfinance library (which is blocked by sandbox proxy).

WORKFLOW (from SKILL.md STEP 0F-i):
  1. For each ticker, call mcp__workspace__web_fetch with:
       https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}?interval=1d&range=6mo
  2. Save the JSON response body to /tmp/yf_{SYMBOL}.json
  3. Run: python3 yf-compute.py /tmp/yf_EOS.AX.json EOS.AX
     → prints JSON signals for that ticker

OR pass multiple pre-saved JSON files:
  python3 yf-compute.py /tmp/yf_*.json

USAGE:
  python3 yf-compute.py <json_file> [<json_file> ...]

Each json_file should be the raw response from:
  https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}?interval=1d&range=6mo
"""

import json, sys, math

def compute_rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [max(d, 0) for d in deltas]
    losses = [abs(min(d, 0)) for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def compute_sma(values, period):
    if len(values) < period:
        return None
    return round(sum(values[-period:]) / period, 4)

def compute_signals(data, symbol="UNKNOWN"):
    """Compute trading signals from Yahoo Finance v8 chart JSON."""
    try:
        result = data["chart"]["result"][0]
    except (KeyError, IndexError, TypeError):
        error = data.get("chart", {}).get("error", {})
        return {"symbol": symbol, "error": str(error) or "No chart result"}

    timestamps = result.get("timestamp", [])
    quote = result.get("indicators", {}).get("quote", [{}])[0]
    closes = [c for c in quote.get("close", []) if c is not None]
    volumes = [v for v in quote.get("volume", []) if v is not None]
    highs = [h for h in quote.get("high", []) if h is not None]
    lows = [l for l in quote.get("low", []) if l is not None]

    if not closes:
        return {"symbol": symbol, "error": "No close price data"}

    current_price = closes[-1]
    current_vol = volumes[-1] if volumes else None

    # RSI (14-period)
    rsi_now = compute_rsi(closes, 14)
    rsi_5d_ago = compute_rsi(closes[:-5], 14) if len(closes) > 19 else None

    # RSI trend: compare current RSI to RSI 5 days ago
    if rsi_now and rsi_5d_ago:
        rsi_trend = "rising" if rsi_now > rsi_5d_ago else "falling"
        rsi_trend_delta = round(rsi_now - rsi_5d_ago, 2)
    else:
        rsi_trend = "unknown"
        rsi_trend_delta = None

    # SMAs
    sma20  = compute_sma(closes, 20)
    sma50  = compute_sma(closes, 50)
    sma200 = compute_sma(closes, 200)

    # Volume ratio (today vs 20-day avg)
    avg_vol_20d = sum(volumes[-21:-1]) / 20 if len(volumes) >= 21 else None
    vol_ratio_20d = round(current_vol / avg_vol_20d, 2) if (current_vol and avg_vol_20d and avg_vol_20d > 0) else None

    # 52-week high/low (252 trading days)
    w52_closes = closes[-252:]
    w52_high = round(max(w52_closes), 4) if w52_closes else None
    w52_low  = round(min(w52_closes), 4) if w52_closes else None

    # Price vs SMAs
    above_sma50  = (current_price > sma50)  if sma50  else None
    above_sma200 = (current_price > sma200) if sma200 else None
    pct_from_52w_high = round((current_price - w52_high) / w52_high * 100, 2) if w52_high else None

    # STEP 0E scoring bonuses (pre-computed)
    bonuses = {}
    if above_sma50 and above_sma200:
        bonuses["above_both_smas"] = True
    if rsi_trend == "rising" and above_sma50:
        bonuses["rsi_trend_rising_above_sma50"] = True
    if vol_ratio_20d and vol_ratio_20d > 3.0:
        bonuses["vol_spike_3x"] = True
    if w52_high and pct_from_52w_high and pct_from_52w_high > -3:
        bonuses["near_52w_high"] = True

    # Penalties
    penalties = {}
    if not above_sma50:
        penalties["below_sma50"] = True
    if rsi_now and rsi_now > 70 and rsi_trend == "rising":
        penalties["overbought_rising"] = True
    if rsi_trend == "falling" and not above_sma50:
        penalties["rsi_falling_below_sma50"] = True

    signals = {
        "symbol": symbol,
        "price": round(current_price, 4),
        "rsi_14": rsi_now,
        "rsi_5d_ago": rsi_5d_ago,
        "rsi_trend_5d": rsi_trend,
        "rsi_trend_delta": rsi_trend_delta,
        "sma20": sma20,
        "sma50": sma50,
        "sma200": sma200,
        "vol_ratio_20d": vol_ratio_20d,
        "avg_vol_20d": round(avg_vol_20d) if avg_vol_20d else None,
        "price_vs_sma50": "above" if above_sma50 else ("below" if above_sma50 is False else "unknown"),
        "price_vs_sma200": "above" if above_sma200 else ("below" if above_sma200 is False else "unknown"),
        "52w_high": w52_high,
        "52w_low": w52_low,
        "pct_from_52w_high": pct_from_52w_high,
        "data_points": len(closes),
        "step0e_bonuses": bonuses,
        "step0e_penalties": penalties,
    }
    return signals


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 yf-compute.py <yf_response.json> [...]", file=sys.stderr)
        sys.exit(1)

    all_signals = {}
    for path in sys.argv[1:]:
        try:
            with open(path) as f:
                data = json.load(f)
            # Try to extract symbol from the data
            try:
                symbol = data["chart"]["result"][0]["meta"]["symbol"]
            except (KeyError, IndexError):
                symbol = path.split("/")[-1].replace(".json","").replace("yf_","")
            signals = compute_signals(data, symbol)
            all_signals[symbol] = signals
        except Exception as e:
            all_signals[path] = {"error": str(e)}

    print(json.dumps(all_signals, indent=2))


if __name__ == "__main__":
    main()
