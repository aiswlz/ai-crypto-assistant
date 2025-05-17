import requests
import os
from datetime import datetime, timedelta

def get_crypto_news(coin="BTC"):
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": os.getenv("CRYPTO_PANIC_API_KEY"),
        "currencies": coin.upper(),
        "kind": "news",
        "public": "true"
    }
    try:
        response = requests.get(url, params=params)
        results = response.json().get("results", [])[:3]
        
        detailed_news = []
        for item in results:
            published_at = datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            detailed_news.append({
                'title': item['title'],
                'url': item['url'],
                'source': item['source']['title'],
                'published': f"{published_at.strftime('%b %d, %H:%M')} UTC",
                'excerpt': item.get('excerpt', 'No description available')
            })
        return detailed_news
    except Exception as e:
        print(f"News API Error: {e}")
        return []