import requests, logging

def get_price_from_api(exchange, url):
    """
    Attempts to fetch the price from the specified API URL.
    Returns None in case of an error.
    """
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if exchange in ["Binance", "Mexc"]:
            return float(data["price"])
        elif exchange == "KuCoin":
            return float(data["data"]["price"])
        elif exchange == "Coinbase":
            return float(data["price"])
        elif exchange == "OKX":
            return float(data["data"][0]["last"])
        elif exchange == "Gate.io":
            return float(data[0]["last"])
        elif exchange == "BingX":
            return float(data["data"]["book_ticker"]["ask_price"])  # Using ask price
        elif exchange == "Bitget":
            return float(data["data"][0]["askPr"])
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for {exchange}: {e}")
    except (KeyError, TypeError, ValueError) as e:
        logging.error(f"Failed to parse API response from {exchange}: {e}")
    return None