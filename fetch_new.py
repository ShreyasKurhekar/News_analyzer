
# fetch_news.py
import json
from pathlib import Path

import requests

API_KEY = "d7622c8b4cc541d29c38ac819e612b00"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
NEWS_FILE = DATA_DIR / "news.json"


def fetch_news(query="india"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
    DATA_DIR.mkdir(exist_ok=True)

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            print("No articles returned by the API.")
            return False

        with NEWS_FILE.open("w", encoding="utf-8") as f:
            json.dump(articles, f, indent=4)

        print("News fetched successfully!")
        return True

    except Exception as e:
        print("Error fetching news:", e)
        return False
