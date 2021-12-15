var symbolSelection = document.getElementById("symbol");
var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 600,
    height: 300,
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
});
var candleSeries = chart.addCandlestickSeries();
var symbol = symbolSelection.value.toLowerCase();
var binanceWebSocket = new WebSocket("wss://stream.binance.com:9443/ws/" + symbol + "@kline_15m")
var newSymbolChosen = false;
var currentBar = {
	open: null,
	high: null,
	low: null,
	close: null,
	time: null,
};

// Initial set up
addEventListeners()
loadRecentDataIntoChart(symbol);
setWebSocketEventHandlers();

function initialiseChart(newSymbol) {	
	chart.removeSeries(candleSeries)
	candleSeries = chart.addCandlestickSeries();
	symbol = newSymbol.toLowerCase();

	loadRecentDataIntoChart(symbol);

	// Prevent trying to close a web socket before it's opened
	if (binanceWebSocket.readyState == WebSocket.OPEN) {
		binanceWebSocket.close();
	}
	
	newSymbolChosen = true;
}

function setWebSocketEventHandlers() {
	binanceWebSocket.onclose = webSocketOnClose;
	binanceWebSocket.onmessage = webSocketOnMessage;
}

function webSocketOnMessage(event) {
	var message = JSON.parse(event.data);
	var candleData = message.k;

	// Set the current bar details
	currentBar.time = candleData.t / 1000;
	currentBar.open = candleData.o;
	currentBar.close = candleData.c;
	currentBar.high = candleData.h;
	currentBar.low = candleData.l;

	// Update the chart
	candleSeries.update(currentBar);
}

function webSocketOnClose() {
	if (newSymbolChosen) {
		// Open a new websocket with the new symbol
		binanceWebSocket = new WebSocket("wss://stream.binance.com:9443/ws/" + symbol + "@kline_15m")
		setWebSocketEventHandlers();
		newSymbolChosen = false;
	}
}

function loadRecentDataIntoChart(symbol) {

	// Get recent data and set it in the candle series
	fetch('http://localhost:5000/history/' + symbol.toUpperCase())
	.then((r) => r.json())
	.then((response) => {candleSeries.setData(response)});

}

function symbolChange(event) {
	initialiseChart(event.target.value);
}

function addEventListeners() {
	symbolSelection.addEventListener("change", symbolChange);
}