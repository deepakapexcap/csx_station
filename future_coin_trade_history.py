import time
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from keys import api_key, secret_key
import datetime

def fetch_orders_time_paging():
    all_orders = []
    url = "https://coinswitch.co/trade/api/v2/futures/orders/closed"
    endpoint = "/trade/api/v2/futures/orders/closed"

    # Set your starting datetime here (must be within last 7 days)
    from_dt = datetime.datetime(2025, 5, 25, 0, 0, 0)
    # We'll page by 1 day each loop
    page_delta = datetime.timedelta(days=1)
    to_dt = from_dt + page_delta

    while True:
        from_time_ms = int(from_dt.timestamp() * 1000)
        to_time_ms = int(to_dt.timestamp() * 1000)
        # print("from_time_ms :",from_time_ms)
        # print("to_time_ms : ",to_time_ms)
        payload = {
            "exchange": "EXCHANGE_2",
            "symbol": "dogeusdt",
            "limit": 50,              # Limit set to 10 per request
            "from_time": from_time_ms,
            "to_time": to_time_ms
        }

        # Prepare signature
        epoch_time = str(int(time.time() * 1000))
        signature_msg = "POST" + endpoint + epoch_time
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

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json().get("data", {})
        orders = data.get("orders", [])
        # print("data : ","\n",data,"\n")


        if not orders:
            print(f"No more orders from {from_dt} to {to_dt}. Moving to next day.")
            # Move window forward anyway if no orders, to cover all days
            from_dt = to_dt
            to_dt = to_dt + page_delta
            # If we passed current time, stop
            if from_dt > datetime.datetime.now():
                break
            continue

        all_orders.extend(orders)
        print(f"Fetched {len(orders)} orders from {from_dt} to {to_dt}")

        # Move to next time window
        from_dt = to_dt
        to_dt = to_dt + page_delta

        # Stop if beyond current time
        if from_dt > datetime.datetime.now():
            break

        time.sleep(1)  # rate limit delay
    # Remove duplicate orders based on order_id
    unique_orders = {order["order_id"]: order for order in all_orders}

    # Convert dict back to list and sort by created_at descending
    sorted_orders = sorted(unique_orders.values(), key=lambda x: x.get("created_at", 0), reverse=False)
    print("printing len here :",len(sorted_orders))
    return sorted_orders


# Usage

