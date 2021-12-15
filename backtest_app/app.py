import config
from data_fetcher import DataFetcher
from backtest import BacktestRunner
from flask import Flask, render_template, jsonify, request
from binance.client import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = Client(config.API_KEY, config.API_SECRET)

@app.route('/')
def index():
    page_title = "Trading Bot"

    # Get asset balances
    asset_balances = {}

    for symbol in config.AVAILABLE_BALANCES:
        balance_info = client.get_asset_balance(asset=symbol)
        asset_balances.update({symbol : balance_info['free']})

    # Prepare selections
    symbol_selection = config.AVAILABLE_SYMBOLS
    strategy_selection = config.BACKTEST_STRATEGIES.keys()

    return render_template('index.html', title=page_title, asset_balances=asset_balances, symbol_selection=symbol_selection, strategy_selection=strategy_selection)

@app.route('/history/<symbol>')
def history(symbol):

    # Get data loader
    data_fetcher = DataFetcher()

    return data_fetcher.load_chart_data('{symbol}'.format(symbol=symbol))

@app.route('/run_backtest', methods=['GET', 'POST'])
def run_backtest():

    # Get selected symbol
    symbol = request.values.get('symbol_select', config.DEFAULT_SYMBOL)
    strategy = request.values.get('strategy_select', "RSI Strategy")

    # Prepare runners
    bt_runner = BacktestRunner()
    data_fetcher = DataFetcher()

    # Get data and perform backtest
    data_fetcher.import_backtest_data('10 days ago', symbol)
    bt_runner.test_strategy(config.BACKTEST_STRATEGIES[strategy])

    return index()
