"""Pipe real-time social posts into a trading strategy.

Consumes a WebSocket of normalized social events (X, Truth Social, Binance
Square) and hands each one to on_signal() in milliseconds. Replace the
on_signal() body with your strategy. See README for env vars.
"""
import asyncio
import json
import os

import websockets

API_KEY = os.environ.get("API_KEY")
WS_URL = os.environ.get("WS_URL")

# Which platforms to act on. Drop entries you don't trade.
PLATFORMS = {"x", "truth", "binance"}


def on_signal(event):
    """Your strategy goes here. Called once per event, in order, as it lands.

    event = {platform, handle, content, coinPairs, timestamp}
    Return / place an order, push to a queue, score a sentiment model, etc.
    """
    platform = event.get("platform")
    handle = event.get("handle", "?")
    pairs = event.get("coinPairs") or []
    content = (event.get("content") or "").replace("\n", " ")[:140]
    print(f"[{platform}] @{handle} {pairs} {content}")


async def run():
    if not API_KEY or not WS_URL:
        raise SystemExit("set API_KEY and WS_URL (see README)")
    while True:
        try:
            async with websockets.connect(WS_URL, additional_headers={"X-Api-Key": API_KEY}) as ws:
                print(f"connected: streaming {sorted(PLATFORMS)}")
                async for raw in ws:
                    try:
                        event = json.loads(raw)
                    except ValueError:
                        continue
                    if event.get("platform") in PLATFORMS:
                        on_signal(event)
        except Exception as exc:  # noqa: BLE001
            print(f"disconnected ({exc}); reconnecting in 1s")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
