import feedparser
import spacy

# Load small English NLP model for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")


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


def extract_disruption_entities(text):
    """Extracts affected organizations and locations/facilities from text using spaCy NER."""
    doc = nlp(text)
    entities = {
        "organizations": [],
        "locations": []
    }

    for ent in doc.ents:
        if ent.label_ == "ORG" and ent.text not in entities["organizations"]:
            entities["organizations"].append(ent.text)
        elif ent.label_ in ("GPE", "LOC", "FAC") and ent.text not in entities["locations"]:
            entities["locations"].append(ent.text)

    return entities


if __name__ == "__main__":
    news = fetch_supply_chain_news(limit=5)
    print(f"Analyzed {len(news)} articles:\n")
    for item in news:
        extracted = extract_disruption_entities(item["title"])
        print("Headline:", item["title"])
        print("  Orgs:", extracted["organizations"])
        print("  Locations:", extracted["locations"])
        print("-" * 50)