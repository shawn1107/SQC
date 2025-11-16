"""Fetches the latest TSMC (2330.TW) stock price and plots a simple candlestick chart.

The script only depends on ``requests`` and ``matplotlib``.  Run it with:

    python tsmc_stock.py

"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import requests

QUOTE_API = "https://query1.finance.yahoo.com/v7/finance/quote"
CHART_API = "https://query1.finance.yahoo.com/v8/finance/chart"
TICKER = "2330.TW"


def fetch_latest_price() -> float:
    """Return the most recent regular market price for TSMC."""
    response = requests.get(QUOTE_API, params={"symbols": TICKER}, timeout=10)
    response.raise_for_status()
    data = response.json()
    result = data["quoteResponse"]["result"]
    if not result:
        raise ValueError("No quote data returned for ticker 2330.TW")
    return float(result[0]["regularMarketPrice"])


def fetch_chart_data(range_: str = "1mo", interval: str = "1d") -> List[Dict[str, float]]:
    """Fetch OHLC data from Yahoo Finance for a given range and interval."""
    params = {"range": range_, "interval": interval, "events": "div,splits"}
    response = requests.get(f"{CHART_API}/{TICKER}", params=params, timeout=10)
    response.raise_for_status()
    data = response.json()["chart"]["result"][0]

    timestamps = data.get("timestamp", [])
    quotes = data["indicators"]["quote"][0]

    candles: List[Dict[str, float]] = []
    for ts, open_, high, low, close in zip(
        timestamps, quotes["open"], quotes["high"], quotes["low"], quotes["close"]
    ):
        if None in (ts, open_, high, low, close):
            continue
        candles.append(
            {
                "time": datetime.fromtimestamp(ts),
                "open": float(open_),
                "high": float(high),
                "low": float(low),
                "close": float(close),
            }
        )
    return candles


def plot_candlestick(candles: List[Dict[str, float]]) -> None:
    """Render a minimal candlestick chart using Matplotlib."""
    if not candles:
        print("沒有可以繪圖的價量資料。")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    for idx, candle in enumerate(candles):
        color = "#2ca02c" if candle["close"] >= candle["open"] else "#d62728"
        ax.plot([idx, idx], [candle["low"], candle["high"]], color=color, linewidth=1)
        ax.plot([idx - 0.2, idx], [candle["open"], candle["open"]], color=color, linewidth=3)
        ax.plot([idx, idx + 0.2], [candle["close"], candle["close"]], color=color, linewidth=3)

    ax.set_title("台積電 (2330.TW) 最近一個月日K線")
    ax.set_ylabel("價格 (TWD)")
    ax.set_xlim(-1, len(candles))

    step = max(len(candles) // 6, 1)
    ticks = list(range(0, len(candles), step))
    labels = [candles[i]["time"].strftime("%m-%d") for i in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, rotation=45, ha="right")

    ax.grid(True, axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()


def main() -> None:
    price = fetch_latest_price()
    print(f"台積電即時股價：{price:.2f} TWD")
    candles = fetch_chart_data()
    plot_candlestick(candles)


if __name__ == "__main__":
    main()
