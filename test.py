from binance.client import Client
from binance.enums import *
import time

# Set up the API client
api_key = 'pL241GM6Ml8OpYXPT1Ydsp5DzC6ecDOFf8ruDJNXUgCp2GRajy2anw7Fo9l8d65O'
api_secret = 'OgdlxQbCCLNrRYBL4ah9V2uX730INY73HNvmPqJsXVSdQtz2bvJSB0KVAKYRv0Xa'

client = Client(api_key, api_secret)


# get account info
account_info = client.get_account()

# get account balance
balance = account_info['balances'].find({'asset': 'BTC'})['free']
client.futures_create_order()
pass