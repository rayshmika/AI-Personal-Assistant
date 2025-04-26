import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def get_news(country="us", query=None):
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": API_KEY,
        "country": country.lower(),
        "pageSize": 5
    }

    if query:
        base_url = "https://newsapi.org/v2/everything"
        params["q"] = query
        del params["country"]

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if not articles:
            return "No news articles found."
        news = "\n".join([f"- {article['title']}" for article in articles])
        return f"Here are the top headlines:\n{news}"
    else:
        return "Sorry, I couldn’t fetch the news."
