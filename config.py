from backtest_app.strategies.bt_strategies import RSIStrategy

# API key/secret for binance
API_KEY = 'CENSORED'
API_SECRET = 'CENSORED'

# Symbol settings
DEFAULT_SYMBOL='BTCUSDT'
AVAILABLE_SYMBOLS=['BTCUSDT', 'ETHUSDT', 'LUNAUSDT', 'EGLDUSDT']
AVAILABLE_BALANCES=['BTC', 'ETH', 'LUNA', 'EGLD', 'USDT']

# Backtest config
BACKTEST_DATA_PATH='data_sets/backtest_data.csv'
BACKTEST_STRATEGIES={
    "RSI Strategy" : RSIStrategy
}

# RSI Strategy Config
RSI_OVERBOUGHT=70
RSI_OVERSOLD=30
RSI_PERIOD=14