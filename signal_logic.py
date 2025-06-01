import requests
import random

API_KEYS = {
    "twelve": "YOUR_TWELVE_API_KEY",
    "alpha": "YOUR_ALPHA_KEY",
    "finnhub": "YOUR_FINNHUB_KEY"
}

def get_signal(pair, timeframe, direction, minAcc, maxAcc, source="twelve"):
    if source == "twelve":
        url = f"https://api.twelvedata.com/time_series?symbol={pair}&interval={timeframe}&apikey={API_KEYS['twelve']}"
        close_key = "close"

    elif source == "alpha":
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={pair}&interval={timeframe}&apikey={API_KEYS['alpha']}"
        close_key = "4. close"

    elif source == "finnhub":
        url = f"https://finnhub.io/api/v1/quote?symbol={pair}&token={API_KEYS['finnhub']}"
        response = requests.get(url).json()
        if "c" not in response:
            return {"error": "Finnhub data not available"}
        last_price = response["c"]
        prev_price = response["pc"]
        direction_result = "CALL" if last_price > prev_price else "PUT"
    else:
        return {"error": "Invalid source"}

    if source in ["twelve", "alpha"]:
        response = requests.get(url).json()
        try:
            candles = list(response["values"].values()) if source == "alpha" else response["values"]
            last_close = float(candles[0][close_key])
            prev_close = float(candles[1][close_key])
            direction_result = "CALL" if last_close > prev_close else "PUT"
        except:
            return {"error": "Invalid API response"}

    if direction.upper() == "BOTH":
        final_dir = direction_result
    elif direction.upper() == direction_result:
        final_dir = direction_result
    else:
        return {"signal": "Filtered out: direction mismatch"}

    accuracy = random.randint(minAcc, maxAcc)

    return {
        "pair": pair,
        "direction": final_dir,
        "accuracy": accuracy,
        "price": last_close if source != "finnhub" else last_price
    }