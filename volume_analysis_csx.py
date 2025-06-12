import time
import requests
from urllib.parse import urlencode, urlparse
from keys import api_key, secret_key
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from gen_sign import get_signature


# --- Endpoint and Method ---
method = "GET"
endpoint = "/trade/api/v2/orders"

# --- Timestamp ---
epoch_time = str(int(time.time() * 1000))

# --- Query Parameters ---
params = {
    "count": 500,
    "from_time": 1749670965000,
    # "symbols": "shib/inr",
    "exchanges": "coinswitchx",
    "type": "limit",
    "status": "EXECUTED",
    "open": False
    
}
query_string = ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
url = "https://coinswitch.co" + endpoint + query_string

payload ={}

# --- Signature ---

signature = get_signature(method, endpoint, params, epoch_time, secret_key)
# print("signature :",signature)

# --- Headers ---
headers = {
    "Content-Type": "application/json",
    "X-AUTH-APIKEY": api_key,
    "X-AUTH-SIGNATURE": signature,
    "X-AUTH-EPOCH": epoch_time
}

# --- Request ---
response = requests.get(url, headers=headers, json=payload)
# print("Status Code:", response.status_code)
res=  response.json()
# print(res)
# for i in res["data"]["orders"]:    
#     print(i,"\n")











from collections import defaultdict

# Initialize summary dictionary
summary = defaultdict(lambda: {
    "buy_qty": 0.0,
    "sell_qty": 0.0,
    "buy_value": 0.0,
    "sell_value": 0.0,
    "total_trade_value": 0.0,
    "tds_deducted": 0.0
})

# Process each order
for order in res["data"]["orders"]:
    symbol = order["symbol"]
    coin = symbol.split("/")[0]
    qty = float(order["executed_qty"])
    price = float(order["average_price"])
    side = order["side"].upper()

    trade_value = qty * price

    if side == "BUY":
        summary[coin]["buy_qty"] += qty
        summary[coin]["buy_value"] += trade_value
    elif side == "SELL":
        summary[coin]["sell_qty"] += qty
        summary[coin]["sell_value"] += trade_value
        summary[coin]["tds_deducted"] += trade_value * 0.01  # 1% TDS on sells

    summary[coin]["total_trade_value"] += trade_value

# Round and finalize values
for coin in summary:
    data = summary[coin]
    data["buy_qty"] = round(data["buy_qty"], 4)
    data["sell_qty"] = round(data["sell_qty"], 4)
    data["total_qty"] = round(data["buy_qty"] + data["sell_qty"], 4)
    data["buy_value"] = round(data["buy_value"], 2)
    data["sell_value"] = round(data["sell_value"], 2)
    data["total_trade_value"] = round(data["total_trade_value"], 2)
    data["tds_deducted"] = round(data["tds_deducted"], 2)

# Calculate totals
total_trade_value = sum(d["total_trade_value"] for d in summary.values())
total_tds_deducted = sum(d["tds_deducted"] for d in summary.values())

# Prepare clean print dict without buy_value/sell_value
for coin in summary:
    clean_data = {k: v for k, v in summary[coin].items() if k not in ["buy_value", "sell_value"]}
    print(f"{coin}: {clean_data}\n")

print(f"Total Trade Value: {round(total_trade_value, 2)}")
print(f"Total TDS Deducted: {round(total_tds_deducted, 2)}")
