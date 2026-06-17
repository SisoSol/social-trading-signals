# social-trading-signals

[![License: MIT](https://img.shields.io/github/license/SisoSol/social-trading-signals?style=flat-square&color=blue)](LICENSE) [![Last commit](https://img.shields.io/github/last-commit/SisoSol/social-trading-signals?style=flat-square)](https://github.com/SisoSol/social-trading-signals/commits) [![CI](https://github.com/SisoSol/social-trading-signals/actions/workflows/ci.yml/badge.svg)](https://github.com/SisoSol/social-trading-signals/actions/workflows/ci.yml) [![Built for 1322.io](https://img.shields.io/badge/built%20for-1322.io-3b82f6?style=flat-square)](https://1322.io) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/SisoSol/social-trading-signals/pulls)

Pipe **real-time social posts into your trading bot.** A tiny Python harness
that consumes a **WebSocket** of normalized social events (X, Truth Social,
Binance Square) and hands each one to your strategy function in milliseconds, so
your bot reacts the instant an account posts, not on the next poll.

Your bot is only as fast as its slowest input. Polling a REST endpoint caps you
at the poll interval and burns rate limits. A persistent WebSocket pushes the
event as it lands; for signal-driven strategies where the first seconds decide
the fill, that is the only thing that makes sense.

Runs against the [1322](https://1322.io/use-cases/trading-bot-social-alerts) feed
(X ~150-250ms; Truth Social and Binance Square on the same socket, coin pairs
parsed). The consumer is generic.

- Social alerts for trading bots: https://1322.io/use-cases/trading-bot-social-alerts
- The real-time API: https://1322.io/monitoring-api
- Event schema / docs: https://1322.io/docs

## Event shape

```json
{ "platform": "x", "handle": "examplekol", "content": "...", "coinPairs": ["BTCUSDT"], "timestamp": "2026-06-17T12:00:00Z" }
```

Normalized across every platform. `coinPairs` is parsed for Binance Square.

## Run

```bash
pip install websockets
API_KEY=your-key WS_URL=wss://1322.io/your-ws-path python main.py
```

Replace the `on_signal()` body with your strategy: match tickers / contract
addresses, route by author, fan out to multiple strategies, or place an order.

Get an API key + WebSocket path from the dashboard (from $250/mo):
https://1322.io/pricing

## Related

- KOL tweet alert bot: https://github.com/SisoSol/kol-tweet-alert-bot
- Binance Square: https://github.com/SisoSol/binance-square-realtime
- All six platforms: https://github.com/SisoSol/social-monitor-examples

MIT licensed.
