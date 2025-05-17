import requests

def get_market_data(coin_id="bitcoin"):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        data = requests.get(url).json()
        
        price_change_24h = data["market_data"]["price_change_percentage_24h"]
        
        return {
            "market_cap": round(data["market_data"]["market_cap"]["usd"]),
            "rank": data["market_data"]["market_cap_rank"],
            "price_change_24h": round(price_change_24h, 2),
            "volume": round(data["market_data"]["total_volume"]["usd"])
        }
    except Exception as e:
        print(f"CoinGecko Error: {e}")
        return {"market_cap": 0, "rank": "N/A", "price_change_24h": 0, "volume": 0}

def get_top_coins(limit=50):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "sparkline": "true"
    }
    try:
        coins = requests.get(url, params=params).json()
        return {coin["symbol"].upper(): coin["id"] for coin in coins}
    except Exception as e:
        print(f"Top Coins Error: {e}")
        return {"BTC": "bitcoin"}