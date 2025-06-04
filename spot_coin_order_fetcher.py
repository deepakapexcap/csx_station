import time
import requests
from urllib.parse import urlencode
from cryptography.hazmat.primitives.asymmetric import ed25519
import datetime
from keys import api_key, secret_key  # your keys

def generate_signature(method, endpoint_path, epoch_time):
    message = method + endpoint_path + epoch_time
    private_key_bytes = bytes.fromhex(secret_key)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    signature = private_key.sign(message.encode("utf-8")).hex()
    return signature

def fetch_spot_orders_no_cursor():
    base_url = "https://coinswitch.co"
    endpoint_path = "/trade/api/v2/orders"

    dt = datetime.datetime(2024, 5, 5)
    from_time_ms = int(dt.timestamp() * 1000)

    params = {
        "count": 50,  # max records to fetch in one call
        "from_time": from_time_ms,
        "to_time": int(time.time() * 1000),
        "symbols": "xrp/inr",
        "exchanges": "coinswitchx",
        "status": "EXECUTED",
        "open": False
    }

    query_string = urlencode(params)
    endpoint = endpoint_path + ('&' if '?' in endpoint_path else '?') + query_string
    url = base_url + endpoint

    epoch_time = str(int(time.time() * 1000))
    signature = generate_signature("GET", endpoint_path, epoch_time)

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-SIGNATURE": signature,
        "X-AUTH-APIKEY": api_key,
        "X-AUTH-EPOCH": epoch_time
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()

    orders = response_json.get("data", {}).get("orders", [])
    print(f"Fetched {len(orders)} orders.")
    return orders

if __name__ == "__main__":
    orders = fetch_spot_orders_no_cursor()
    print(orders)
