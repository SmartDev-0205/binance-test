import requests
import time
import hmac
import hashlib
import json

api_key = 'pL241GM6Ml8OpYXPT1Ydsp5DzC6ecDOFf8ruDJNXUgCp2GRajy2anw7Fo9l8d65O'
api_secret = b'OgdlxQbCCLNrRYBL4ah9V2uX730INY73HNvmPqJsXVSdQtz2bvJSB0KVAKYRv0Xa'

create_order_endpoint = 'https://fapi.binance.com/fapi/v1/order'
price_endpoint = 'https://api.binance.com/api/v3/ticker/price?symbol'
leverage_endpoint = 'https://fapi.binance.com/fapi/v1/leverage'
all_orders_endpoint = 'https://fapi.binance.com/fapi/v1/allOrders'


leverage = 50
profit_percent = 20
cost = 10
# quantity = 0.01
symbol = 'BTCUSDT'
side = "BUY"

orders = []


def set_leverage(leverage):
    params = {
        'symbol': symbol,
        'leverage': leverage,
        "recvWindow": 60000,
        'timestamp': int(time.time() * 1000)
    }

    # Generate the signature
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    signature = hmac.new(api_secret, query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Add the signature to the request parameters
    params['signature'] = signature
    # Send the request
    response = requests.post(leverage_endpoint, params=params, headers={'X-MBX-APIKEY': api_key})
    # Print the response
    print(response.json())


def cancel_order(order_id):
    params = {
        'symbol': symbol,
        "orderId": order_id,
        "recvWindow": 60000,
        'timestamp': int(time.time() * 1000)  # current timestamp in milliseconds
    }

    # Generate the signature
    query_string = '&'.join([f"{k}={v}" for k,v in params.items()])
    signature = hmac.new(api_secret, query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Define the headers for the request
    headers = {'X-MBX-APIKEY': api_key}

    # Send the request to cancel the order
    response = requests.delete(create_order_endpoint, headers=headers, params={**params, 'signature': signature})

    # Print the response from Binance
    print(response.json())


def get_price(symbol):
    url = f'{price_endpoint}={symbol}'
    response = requests.get(url)
    data = response.json()
    price = data['price']
    return float(price)

def get_orders():
    params = {
        'symbol': symbol,
        "recvWindow": 60000,
        'timestamp': int(time.time() * 1000)
    }

    # create the signature
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(api_secret, query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # add the signature to the query parameters
    params['signature'] = signature

    # define the request headers
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # send the GET request
    response = requests.get(all_orders_endpoint, headers=headers, params=params).json()

    # print the response
    print(json.dumps(response, indent=2))

def create_stoploss_takeProfit_order(symbol, side, quantity, profit_percent):
    # Define the request parameters
    price = get_price(symbol)
    if side == "SELL":
        stoploss = price - (profit_percent / (100 * leverage)) * price
        takeprofit = price + (profit_percent / (100 * leverage)) * price
    if side == "BUY":
        stoploss = price + (profit_percent / (100 * leverage)) * price
        takeprofit = price - (profit_percent / (100 * leverage)) * price
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': round(quantity,2),
        # 'quantity': 0.01,
        "recvWindow": 60000,
        'timestamp': int(time.time() * 1000)  # current timestamp in milliseconds
    }


    # Generate the signature
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    signature = hmac.new(api_secret, query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Add the signature to the request parameters
    params['signature'] = signature
    # Send the request
    response = requests.post(create_order_endpoint, params=params, headers={'X-MBX-APIKEY': api_key})
    # Print the response
    print(response.json())
    order = {
        "orderID": response.json()["orderId"],
        "stoploss": stoploss,
        "takeprofit": takeprofit,
        "quantity": quantity
    }
    return order


def main():
    # Set leverage
    set_leverage(leverage)
    # Create first order
    price = get_price(symbol)
    quantity = cost * leverage / price
    order = create_stoploss_takeProfit_order(symbol, side, quantity, profit_percent)
    orders.append(order)
    # bot strategy
    while True:
        price = get_price(symbol)
        print("current price : {}".format(price))
        for i, order in enumerate(orders):
            if side == "SELL":
                if price > order["takeprofit"]:
                    orderId = order["orderId"]
                    cancel_order(orderId)
                    new_order = create_stoploss_takeProfit_order(symbol, side, order["quantity"], profit_percent)
                    orders[i] = new_order
                elif price < order["stoploss"]:
                    new_order = create_stoploss_takeProfit_order(symbol, side, 2 * order["quantity"], profit_percent)
                    orders[i] = new_order
            else:
                if price > order["takeprofit"]:
                    orderId = order["orderId"]
                    cancel_order(orderId)
                    new_order = create_stoploss_takeProfit_order(symbol, side, order["quantity"], profit_percent)
                    orders[i] = new_order
                elif price < order["stoploss"]:
                    new_order = create_stoploss_takeProfit_order(symbol, side, 2 * order["quantity"], profit_percent)
                    orders[i] = new_order


if __name__ == "__main__":
    main()
