import requests
import json
from keys import api_key,secret_key
import time
from gen_sign import get_signature



url = "https://coinswitch.co/trade/api/v2/user/portfolio"
payload={}

method= "GET"
epoch_time = str(int(time.time() * 1000))
endpoint = "/trade/api/v2/user/portfolio"
signature = get_signature(method, endpoint, payload, epoch_time,secret_key)

headers = {
            "Content-Type": "application/json",
            "X-AUTH-SIGNATURE": signature,
            "X-AUTH-APIKEY": api_key,
            "X-AUTH-EPOCH": epoch_time
        }

response = requests.request("GET", url, headers=headers, json=payload)
response = response.json()
balances = response
