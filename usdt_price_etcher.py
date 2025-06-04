import json
import requests
from urllib.parse import urlparse, urlencode
from keys import api_key,secret_key
from gen_sign import get_signature
import time



def get_usdt_inr_ltp():

    params = {
      "symbol": "USDT/INR",
      "exchange": "coinswitchx"
    }


    endpoint = "/trade/api/v2/24hr/ticker"

    endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)

    url = "https://coinswitch.co" + endpoint
    payload = {}
    epoch_time = str(int(time.time() * 1000))
    endpoint = "/trade/api/v2/24hr/ticker"
    signature = get_signature("GET", endpoint, params, epoch_time,secret_key)

    headers = {
      'Content-Type': 'application/json',
      'X-AUTH-SIGNATURE': signature,
      'X-AUTH-APIKEY': api_key,
      "X-AUTH-EPOCH": epoch_time

    }
    response = requests.request("GET", url, headers=headers, json=payload)
    usdt_price = response.json()["data"]["coinswitchx"]["lastPrice"]
    return usdt_price