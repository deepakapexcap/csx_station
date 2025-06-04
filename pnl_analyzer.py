from future_coin_trade_history import fetch_orders_time_paging
orders = fetch_orders_time_paging()
# print(orders)
print(f"Total orders fetched: {len(orders)}")


def summarize_orders(orders, symbol_filter=None):
    total_buy_qty = 0
    total_sell_qty = 0
    total_buy_value = 0.0
    total_sell_value = 0.0
    total_execution_fee = 0.0
    total_realised_pnl = 0.0
    
    for order in orders:
        print(order,"\n")
        symbol = order.get('symbol')
        if symbol_filter and symbol != symbol_filter:
            continue
        
        qty = float(order.get('quantity', 0))
        price = float(order.get('avg_execution_price', 0))
        side = order.get('side', '').upper()
        fee = float(order.get('execution_fee', 0))
        pnl = float(order.get('realised_pnl', 0))
        
        total_execution_fee += fee
        total_realised_pnl += pnl
        
        if side == 'BUY':
            total_buy_qty += qty
            total_buy_value += price * qty
        elif side == 'SELL':
            total_sell_qty += qty
            total_sell_value += price * qty

    return {
        "total_buy_qty": total_buy_qty,
        "total_sell_qty": total_sell_qty,
        "total_buy_value": total_buy_value,
        "total_sell_value": total_sell_value,
        "total_execution_fee": total_execution_fee,
    }


# Example usage:
result = summarize_orders(orders, symbol_filter="DOGEUSDT")
print(result)
