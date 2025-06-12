
import requests
import json
from urllib.parse import urlparse, urlencode
from keys import api_key,secret_key
from gen_sign import get_signature
import time


def book_fetcher(symbol):
    params = {
        "exchange": "coinswitchx",
        "symbol": symbol
    }
    endpoint = "/trade/api/v2/depth"
    epoch_time = str(int(time.time() * 1000))
    endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
    url = "https://coinswitch.co" + endpoint
    signature= get_signature("GET","/trade/api/v2/depth",params,epoch_time,secret_key)
    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'X-AUTH-SIGNATURE': signature,
      'X-AUTH-APIKEY': api_key,
      "X-AUTH-EPOCH": epoch_time
    }

    response = requests.request("GET", url, headers=headers, json=payload)
    return response.json()
