import config, websocket, json
from binance.client import Client
from binance.enums import *
from strategies.live_strategies import RSIStrategyLive, StrategyAction

class LiveTrader:

    def __init__(self, strategy, symbol):
        self.client = Client(config.API_KEY, config.API_SECRET)
        self.strategy = strategy
        self.symbol = symbol
        self.socket = "wss://stream.binance.com:9443/ws/" + symbol.lower() + "@kline_1m"
        self.web_socket = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
        self.closed_candles = []
        self.active_trade = False

    def on_open(self, web_socket):
        print("socket opened")

    def on_close(self, web_socket):
        print("socket closed")

    def on_message(self, web_socket, message):

        # Extract whether the candle is closed, and the close value
        json_data = json.loads(message)
        candle_data = json_data['k']
        candle_closed = candle_data['x']
        close = candle_data['c']

        if candle_closed:
            # Add close to array and choose next action
            self.closed_candles.append(float(close))
            action = self.strategy.next_action(self.closed_candles, self.active_trade)

            if action != StrategyAction.NO_ACTION:
                self.execute_order(action)
            
    def run_bot(self):
        self.web_socket.run_forever()

    def execute_order(self, action):
        try:
            match action:
                case StrategyAction.BUY_ORDER:
                    order = self.client.create_order(symbol=self.symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=0.0001)
                case StrategyAction.SELL_ORDER:
                    order = self.client.create_order(symbol=self.symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=0.0001)
            
            print("Order created - {}".format(order))

        except Exception as e:
            print("Caught exception - {}".format(e))

    def stop_bot(self):
        self.web_socket.close()

# Run the live trading bot
strategy = RSIStrategyLive()
trader = LiveTrader(strategy, 'ETHUSDT')
trader.run_bot()

