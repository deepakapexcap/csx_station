import requests
import json
from gen_sign import get_signature
import time
from keys import api_key,secret_key

url = "https://coinswitch.co/trade/api/v2/futures/order"

payload = {
    "symbol" : "xrpusdt",
    "exchange" : "EXCHANGE_2",
    "price" : 2.0,
    "side" : "BUY",
    "order_type" : "LIMIT",
    "quantity" : 7,
    "reduce_only" : False,
}

method= "POST"
endpoint = "https://coinswitch.co/trade/api/v2/futures/order"
params = payload
epoch_time = str(int(time.time() * 1000))

signature = get_signature(method,endpoint,params,epoch_time,secret_key)
print("signature :",signature)

# headers = {
#   'Content-Type': 'application/json',
#   'X-AUTH-SIGNATURE': signature, #https://api-trading.coinswitch.co/#signature-generation
#   'X-AUTH-APIKEY': api_key,
# }


headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': api_key,
    'X-AUTH-EPOCH': epoch_time  # 
}


try:
  response = requests.request("POST", url, headers=headers, json=payload)
  print("Response JSON:", response.json())
except Exception as e:
    print(f"An error occurred: {e}")