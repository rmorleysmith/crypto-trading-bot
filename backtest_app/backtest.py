import backtrader as bt
from data_fetcher import BACKTEST_DATA_PATH

class BacktestRunner:

    def __init__(self):
        self.cerebro = bt.Cerebro()

    def test_strategy(self, strategy, data_set=BACKTEST_DATA_PATH):
        
        # Fetch the data from the data set
        data = bt.feeds.GenericCSVData(dataname=data_set, dtformat=2)

        # Set up the engine and run the strategy
        self.cerebro.adddata(data)
        self.cerebro.addstrategy(strategy)
        self.cerebro.run()
        self.cerebro.plot()
