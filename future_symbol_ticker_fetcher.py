import requests
import json
from urllib.parse import urlencode, urlparse
from keys import api_key,secret_key
import time
from cryptography.hazmat.primitives.asymmetric import ed25519


def fetch_future_ticker_data(symbol):
    params = {
        "symbol": symbol,
        "exchange": "EXCHANGE_2"
    }

    payload = {}

    endpoint = "/trade/api/v2/futures/ticker"

    endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)

    url = "https://coinswitch.co" + endpoint



    epoch_time = str(int(time.time() * 1000))
    signature_msg = "GET" + endpoint + epoch_time
    request_bytes = signature_msg.encode("utf-8")
    secret_key_bytes = bytes.fromhex(secret_key)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
    signature = private_key.sign(request_bytes).hex()


    headers = {
                "Content-Type": "application/json",
                "X-AUTH-SIGNATURE": signature,
                "X-AUTH-APIKEY": api_key,
                "X-AUTH-EPOCH": epoch_time
            }
    
    try:
        response = requests.request("GET", url, headers=headers, json=params)
        # print("Response JSON:", response.json())
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")