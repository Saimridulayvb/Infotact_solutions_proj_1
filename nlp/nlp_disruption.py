import feedparser


def fetch_supply_chain_news(query="supply chain strike OR port closure OR factory shutdown", limit=7):
    """Fetches recent supply-chain disruption headlines from Google News RSS."""
    formatted_query = query.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={formatted_query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:limit]:
        articles.append({
            "title": entry.get("title", ""),
            "published": entry.get("published", ""),
            "link": entry.get("link", "")
        })
    return articles


if __name__ == "__main__":
    news = fetch_supply_chain_news(limit=5)
    print(f"Fetched {len(news)} articles:")
    for item in news:
        print("-", item["title"])