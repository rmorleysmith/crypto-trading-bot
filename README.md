# Backtester & Trading Bot

This is a basic tool which can be used for backtesting or running live trading strategies for Cryptocurrency trading using the Binance exchange.

The backtesting and display portion  uses HTML & JavaScript for the front-end, and the Flask framework for Python in the back-end.

The live trade portion is not controlled with a front-end, and is coded in Python only. Please note that this is little more than a proof of concept only and should not be run with any serious intentions.

## Chart

The front-end contains a 15 minute chart for a chosen Coin-USDT pair. It is initialised by reading 5 days of data from Binance with Python, then processed and converted to JSON which is then output to '/history' where we fetch it using JavaScript, which then populates the chart. After this is done, the current data is then streamed to the chart using a JavaScript web socket.

Changing the Coin-USDT pair in the dropdown will refresh the chart, load up 5 days of data, and begin streaming data for the new pair.

## Backtesting

You are able to backtest a particular strategy on a particular cryptocurrency pair with this program by choosing a pair and strategy from two dropdowns, then clicking 'Run backtest'. 

This is done by using the Backtrader package for Python at the '/run_backtest/<symbol>' endpoint.

The only backtestable strategy currently coded is a basic RSI strategy in which we buy in an oversold state, and sell in an overbought state.

## Live Trading

The live trading bot can be run via livebot.py, it will stream data from a Binance web socket and buy/sell depending on the strategy selected.

This is done by collecting an array of closing candle prices and passing it over to the strategy to decide whether to buy or sell, depending on specified conditions. We use TA-Lib for technical analysis indicators.

The only strategy currently coded is a basic RSI strategy in which we buy in an oversold state, and sell in an overbought state.