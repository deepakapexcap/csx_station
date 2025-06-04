import requests
import json
from keys import api_key,secret_key
from gen_sign import get_signature
import time

def future_wallet_bal_fetcher():
    url = "https://coinswitch.co/trade/api/v2/futures/wallet_balance"

    payload = {}
    epoch_time = str(int(time.time() * 1000))
    signature = get_signature("GET","/trade/api/v2/futures/wallet_balance",payload,epoch_time,secret_key)

    headers = {
      'Content-Type': 'application/json',
      'X-AUTH-SIGNATURE': signature, #https://api-trading.coinswitch.co/#signature-generation
      'X-AUTH-APIKEY': api_key,
      'X-AUTH-EPOCH': epoch_time  
    }

    
    response = requests.request("GET", url, headers=headers, json=payload)
    data =  response.json()
    # print(data)
    return data
        # for i in data["data"]["asset"]:
        #     print(i,"\n")
    