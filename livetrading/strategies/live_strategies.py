import enum, talib, numpy, enum
from config import RSI_OVERSOLD, RSI_OVERBOUGHT, RSI_PERIOD

class StrategyAction(enum.Enum):
    NO_ACTION=0
    BUY_ORDER=1
    SELL_ORDER=2

class RSIStrategyLive:

    def next_action(self, closed_candles, active_trade):

        # Get current RSI
        current_rsi = self.get_current_rsi(closed_candles)

        # Oversold - enter buy position
        if current_rsi < RSI_OVERSOLD and not active_trade:
            return StrategyAction.BUY_ORDER

        # Overbought - close position
        if current_rsi > RSI_OVERBOUGHT and active_trade:
            return StrategyAction.SELL_ORDER

    def get_current_rsi(self, closed_candles):

        # Convert to numpy array
        numpy_closed_candles = numpy.array(closed_candles)

        # Calculate RSIs using TA-Lib
        all_rsi = talib.RSI(numpy_closed_candles, timeperiod=RSI_PERIOD)

        return all_rsi[-1]

