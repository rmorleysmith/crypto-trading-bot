import config, csv, json
from flask import jsonify
from binance.client import Client
from config import DEFAULT_SYMBOL, BACKTEST_DATA_PATH

class DataFetcher:

    def __init__(self):

        # Initialise Binance client
        self.client = Client(config.API_KEY, config.API_SECRET)

    def import_backtest_data(self, start_date, symbol=DEFAULT_SYMBOL, file_path=BACKTEST_DATA_PATH):

        print(symbol)

        # Get candle data from Binance
        candles = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, start_date)
        
        # Setup CSV for writing
        csvfile = open(file_path, 'w', newline='')
        csvfile.truncate()

        # Get a CSV writer
        candle_writer = csv.writer(csvfile, delimiter=',')

        for candle in candles:

            # Make sure UNIX timestamp is in the format we need 
            candle[0] = candle[0] / 1000

            candle_writer.writerow(candle)

        csvfile.close()
    
    def load_chart_data(self, symbol):

        # Get candle data from Binance
        candles = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, "5 days ago")

        processed_candles = []

        # Process the data into the correct format
        for data in candles:
            candle = {
                "time" : data[0] / 1000,
                "open" : data[1],
                "high" : data[2],
                "low"  : data[3],
                "close": data[4]
            }

            processed_candles.append(candle)

        return jsonify(processed_candles)
