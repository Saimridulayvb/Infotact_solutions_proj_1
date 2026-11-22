import feedparser
import spacy
from spacy.matcher import PhraseMatcher

# Load small English NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize PhraseMatcher (case-insensitive) for disruption event classification
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

DISRUPTION_PATTERNS = {
    "LABOR_STRIKE": ["strike", "workers strike", "walkout", "labor dispute", "union strike", "lay off", "layoffs"],
    "PORT_CONGESTION": ["port closure", "congested ports", "port congestion", "shipping delay", "vessel backlog", "port restrictions"],
    "FACILITY_SHUTDOWN": ["factory shutdown", "warehouse closure", "plant closure", "temporarily close", "halt production", "production halt"],
    "GEOPOLITICAL_TRADE": ["tariff", "sanctions", "export ban", "trade restriction", "blockade", "border closure"]
}

for category, phrases in DISRUPTION_PATTERNS.items():
    patterns = [nlp.make_doc(phrase) for phrase in phrases]
    matcher.add(category, patterns)


def clean_headline(raw_title):
    """Separates the core headline from the trailing ' - Publisher' added by Google News RSS."""
    if " - " in raw_title:
        parts = raw_title.rsplit(" - ", 1)
        return parts[0].strip(), parts[1].strip()
    return raw_title.strip(), "Unknown"


def fetch_supply_chain_news(query="supply chain strike OR port closure OR factory shutdown", limit=7):
    """Fetches recent supply-chain disruption headlines from Google News RSS."""
    formatted_query = query.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={formatted_query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:limit]:
        headline, source = clean_headline(entry.get("title", ""))
        articles.append({
            "title": headline,
            "source": source,
            "published": entry.get("published", ""),
            "link": entry.get("link", "")
        })
    return articles


def analyze_disruption_headline(text):
    """Extracts affected entities (NER) and classifies disruption event types (PhraseMatcher)."""
    doc = nlp(text)

    organizations = []
    locations = []
    for ent in doc.ents:
        if ent.label_ == "ORG" and ent.text not in organizations:
            organizations.append(ent.text)
        elif ent.label_ in ("GPE", "LOC", "FAC") and ent.text not in locations:
            locations.append(ent.text)

    matches = matcher(doc)
    event_types = []
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        if label not in event_types:
            event_types.append(label)

    if not event_types:
        event_types.append("GENERAL_DISRUPTION")

    return {
        "organizations": organizations,
        "locations": locations,
        "event_types": event_types
    }


if __name__ == "__main__":
    news = fetch_supply_chain_news(limit=5)
    print(f"Analyzed {len(news)} articles:\n")
    for item in news:
        analysis = analyze_disruption_headline(item["title"])
        print(f"Headline: {item['title']} (Source: {item['source']})")
        print("  Event Types:", analysis["event_types"])
        print("  Orgs:", analysis["organizations"])
        print("  Locations:", analysis["locations"])
        print("-" * 50)