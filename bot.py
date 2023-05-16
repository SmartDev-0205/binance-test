def initialize(state):
    state.run = 0
    state.sl = 0
    state.tp = 0
    state.leverage = 1
    state.profit_percent = 20
    state.cost = -100


@schedule(interval="1h", symbol="BTCUSDT")
def handler(state, data):
    if state.run == 0:
        order_market_value(symbol="BTCUSDT", value=state.cost)
        last_closing_price = data.close_last
        stoploss = last_closing_price - (state.profit_percent / (100 * state.leverage)) * last_closing_price
        takeprofit = last_closing_price + (state.profit_percent / (100 * state.leverage)) * last_closing_price
        state.sl = stoploss
        state.tp = takeprofit
        state.run = 1
    else:
        # get current price
        last_closing_price = data.close_last

        if last_closing_price > state.tp:
            close_position(symbol="BTCUSDT")

            order_market_value(symbol="BTCUSDT", value=state.cost)
            last_closing_price = data.close_last
            stoploss = last_closing_price - (state.profit_percent / (100 * state.leverage)) * last_closing_price
            takeprofit = last_closing_price + (state.profit_percent / (100 * state.leverage)) * last_closing_price
            state.sl = stoploss
            state.tp = takeprofit
        elif last_closing_price < state.sl:
            close_position(symbol="BTCUSDT")

            state.cost = 2 * state.cost
            order_market_value(symbol="BTCUSDT", value=state.cost)

            last_closing_price = data.close_last
            stoploss = last_closing_price - (state.profit_percent / (100 * state.leverage)) * last_closing_price
            takeprofit = last_closing_price + (state.profit_percent / (100 * state.leverage)) * last_closing_price
            state.sl = stoploss
            state.tp = takeprofit
