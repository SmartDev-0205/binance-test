import requests
import time
import hmac
import hashlib

# Define API credentials for the testnet environment
api_key = 'LHPDXO48HGZXvHEOphBPy8HiUygFmeKcd05gdHOnogb84xqUqY3hI9TlYWs8rw80'
api_secret = b'Ng3kLfSLwiaR0ONPXALlC8X3o2D2twyDtu5ezuUgfuC2Ih9Q2ZCpGsktpoAnloFv'

# Define the API endpoint for the testnet environment
endpoint = 'https://testnet.binance.vision/api/v3/order'

# Define the order parameters
symbol = 'BTCUSDT'
side = 'SELL'
quantity = '0.01'
trailing_stop_percent = '0.5'  # the percentage by which the stop price will trail the market price

# Define the request parameters
params = {
    'symbol': symbol,
    'side': side,
    'type': 'STOP_LOSS_LIMIT',
    'timeInForce':"GTC",
    'quantity': quantity,
    "price":25000,
    "stopPrice":24000,
    'timestamp': int(time.time() * 1000)  # current timestamp in milliseconds
}

# Generate the signature
query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
signature = hmac.new(api_secret, query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Add the signature to the request parameters
params['signature'] = signature

# Send the request
response = requests.post(endpoint, params=params, headers={'X-MBX-APIKEY': api_key})

# Print the response
print(response.json())
