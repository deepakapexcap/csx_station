


def calculate_weighted_avg_price(depth_data, qty_limit=1000):
    def weighted_avg(orders):
        total_qty = 0
        total_value = 0
        for price_str, qty_str in orders:
            price = float(price_str)
            qty = float(qty_str)
            if total_qty + qty <= qty_limit:
                total_value += price * qty
                total_qty += qty
            else:
                remaining = qty_limit - total_qty
                total_value += price * remaining
                total_qty += remaining
                break
        return total_value / total_qty if total_qty > 0 else 0

    asks = depth_data["data"]["asks"]
    bids = depth_data["data"]["bids"]

    avg_ask = weighted_avg(asks)
    avg_bid = weighted_avg(bids)
    final_avg = (avg_ask + avg_bid) / 2

    return {
        "avg_bid_price": round(avg_bid, 4),
        "avg_ask_price": round(avg_ask, 4),
        "final_price": round(final_avg, 4)
    }
