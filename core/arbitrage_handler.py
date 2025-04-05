def check_arbitrage(prices, ARBITRAGE_THRESHOLD):
    """
    Determines the lowest and highest prices from the fetched prices,
    calculates the spread, and logs if there is an arbitrage opportunity above the set threshold.
    
    ARGS:
        prices (dict): Dictionary containing prices from different exchanges.
        ARBITRAGE_THRESHOLD (float): Minimum spread percentage required for arbitrage opportunity.
    """
    valid_prices = {ex: price for ex, price in prices.items() if price is not None}
    if not valid_prices:
        valid_msg = "No valid prices were obtained."
        return {"info_msg": valid_msg, "Arbitrage_detail_msg": "", "valid_price" : False }

    min_exchange = min(valid_prices, key=valid_prices.get)
    max_exchange = max(valid_prices, key=valid_prices.get)
    min_price = valid_prices[min_exchange]
    max_price = valid_prices[max_exchange]

    spread = ((max_price - min_price) / min_price) * 100
    Arbitrage_detail_msg = f"Lowest: {min_exchange} = {min_price:.4f}, Highest: {max_exchange} = {max_price:.4f}, Spread: {spread:.2f}%"

    if spread >= ARBITRAGE_THRESHOLD:
        info_msg = f"Arbitrage opportunity! Buy from {min_exchange}, sell at {max_exchange}. Spread: {spread:.2f}%"
        success = True
    else:
        info_msg = "No significant arbitrage opportunity found."
        success = False
        
    real_data = {"min_price" : min_price, "min_exchange" : min_exchange,
                 "max_price" : max_price, "max_exchange" : max_exchange,
                 "arbitrage_percentage" : spread,
                 "prices" : valid_prices}
    
    return {"info_msg": info_msg, "Arbitrage_detail_msg": Arbitrage_detail_msg, "valid_price" : True, "real_data" : real_data, "success": success}