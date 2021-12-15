import backtrader as bt
from config import RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT

class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data, period=RSI_PERIOD)
        self.name = "RSI Strategy"

    def next(self):

        # Buy if RSI is under 30
        if self.rsi < RSI_OVERSOLD and not self.position:
            self.buy(size=0.05)

        # Sell if RSI is above 70
        if self.rsi > RSI_OVERBOUGHT and self.position:
            self.sell(size=0.05)