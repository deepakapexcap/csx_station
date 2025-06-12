from spot_balance_fetcher import balances
from future_symbol_ticker_fetcher import fetch_future_ticker_data
from usdt_price_etcher import  get_usdt_inr_ltp
from future_wallet_balance import future_wallet_bal_fetcher
import csv
from datetime import datetime
from future_multiplier_symbol_list import multiplier_dict
from spot_book_fetcher import book_fetcher
from helper_functions import calculate_weighted_avg_price

usdt_book =book_fetcher("usdt/inr")
# print("usdt_book :",usdt_book)
avg_price = calculate_weighted_avg_price(usdt_book,qty_limit=5000)["final_price"]
# print("usdt_book :",avg_price)

usdt_price = float(avg_price)



portfolio_value = 0
Coin_value = 0
total_usdt = 0

fut_wallet_data =future_wallet_bal_fetcher()
# print("fut_wallet_data",(fut_wallet_data["data"]["base_asset_balances"][0]["balances"]))
blocked_usdt = float(fut_wallet_data["data"]["base_asset_balances"][0]["balances"]["total_blocked_balance"])+ float(fut_wallet_data["data"]["base_asset_balances"][0]["balances"]["total_open_order_margin"])
# print("blocked_usdt for Future positions : ",round(blocked_usdt,2))
portfolio_value += blocked_usdt * float(usdt_price) * 0.99
total_usdt += blocked_usdt
for i in (balances["data"]):
    if float(i["blocked_balance_order"]) or float(i["main_balance"]) != 0:
        # print(i)
        if i["currency"] == "INR":
           total_inr=  float(i["main_balance"]) + float(i["blocked_balance_order"])
           portfolio_value += total_inr
           
        elif  i["currency"] == "USDT":
        #    print(i)
           portfolio_value += (float(i["main_balance"]) + float(i["blocked_balance_order"]) )* float(usdt_price) * 0.99
           total_usdt += (float(i["main_balance"]) + float(i["blocked_balance_order"]) )
        #    Coin_value += (float(i["main_balance"]) + float(i["blocked_balance_order"]) )* float(usdt_price)
        #    print("portfolio_value : ",portfolio_value)


        else:
            # print(" symbol here :",symbol)
            # print(multiplier_dict.keys())
            if i["currency"] in multiplier_dict.keys():
                # print(multiplier_dict[i["currency"]])
                symbol = multiplier_dict[i["currency"]]["future_symbol"]
                multiple = float(multiplier_dict[i["currency"]]["multiple"])
                # print("symbol, multiple")
                # print(symbol, multiple)
                price = float((fetch_future_ticker_data(symbol)["data"]["EXCHANGE_2"]["best_bid_price"]))  
                # print("price :",price/multiple)
                # print(i)
                value_in_USDT = ((float(i["main_balance"]) + float(i["blocked_balance_order"]) ) * price * 0.99) / multiple
                portfolio_value += float(value_in_USDT) * usdt_price
                Coin_value += float(value_in_USDT) * usdt_price
                # print("value_in_inr : ",float(value_in_USDT) * usdt_price,"\n")
                # print("price updated",float(fetch_future_ticker_data(symbol)["data"]["EXCHANGE_2"]["best_bid_price"])


            else:
                symbol = i["currency"]+"usdt"
                try:
                    # print(i)
                    price = float(fetch_future_ticker_data(symbol)["data"]["EXCHANGE_2"]["best_bid_price"]) * float(usdt_price) 
                    # print("price :",price)
                    portfolio_value += (float(i["main_balance"]) + float(i["blocked_balance_order"]) ) * price * 0.99
                    Coin_value += (float(i["main_balance"]) + float(i["blocked_balance_order"]) ) * price
                    # print("portfolio_value : ",portfolio_value)
                    # print("\n")
                except Exception as e:
                    # print("error while fetching data error : ",e, i,"\n")
                    pass

# print("usdt_price : ",usdt_price)
# print("blocked_usdt_fut_positions : ",round(blocked_usdt,2))
# print("total_coins_value : ",round(Coin_value,2))
# print("total_inr : ",total_inr) 
# print("total_portfolio_value : ",round(portfolio_value,2))


# Get current timestamp
time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# CSV file name
csv_file = "portfolio_snapshot.csv"

# Write header only if file is new
try:
    with open(csv_file, 'x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "USDT_price", "Blocked_USDT","Total_usdt", "Coin_Value", "INR", "Total_Value"])
except FileExistsError:
    pass  # File already exists

# Append data to the CSV
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
    time_now,
    round(float(usdt_price), 2),
    round(float(blocked_usdt), 2),
    round(float(total_usdt), 2),
    round(float(Coin_value), 2),
    round(float(total_inr), 2),
    round(float(portfolio_value), 2)])
# Console output
print("usdt_price : ", usdt_price)
print("blocked_usdt_fut_positions : ", round(blocked_usdt, 2))
print("total_usdt_qty : ",round(total_usdt,2))
print("total_coins_value : ", round(Coin_value, 2))
print("total_inr : ", total_inr)
print("total_portfolio_value : ", round(portfolio_value, 2))