import feedparser
import spacy
from spacy.matcher import Matcher, PhraseMatcher

# Load small English NLP model
nlp = spacy.load("en_core_web_sm")

# Add EntityRuler before NER to prevent Title-Case false positives and catch key locations
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns([
    {"label": "GPE", "pattern": [{"LOWER": {"IN": ["chinese", "philippine", "egyptian", "russian", "indian", "american"]}}]}
])

# 1. Exact phrase matcher for multi-word disruption terms
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

DISRUPTION_PATTERNS = {
    "LABOR_STRIKE": ["strike", "workers strike", "walkout", "labor dispute", "union strike", "lay off", "layoffs"],
    "PORT_CONGESTION": ["port closure", "congested ports", "port congestion", "shipping delay", "vessel backlog", "port restrictions"],
    "FACILITY_SHUTDOWN": ["factory shutdown", "warehouse closure", "plant closure", "temporarily close", "halt production", "production halt"],
    "GEOPOLITICAL_TRADE": ["tariff", "sanctions", "export ban", "trade restriction", "blockade", "border closure"]
}

for category, phrases in DISRUPTION_PATTERNS.items():
    patterns = [nlp.make_doc(phrase) for phrase in phrases]
    phrase_matcher.add(category, patterns)

# 2. Token-level lemma matcher to catch word variations & modifiers (e.g., "halts egg production", "congested Chinese ports")
token_matcher = Matcher(nlp.vocab)
token_matcher.add("PORT_CONGESTION", [
    [{"LEMMA": {"IN": ["congest", "block", "close", "restrict", "delay"]}}, {"IS_ALPHA": True, "OP": "*"}, {"LEMMA": {"IN": ["port", "shipping", "vessel", "cargo"]}}],
    [{"LEMMA": {"IN": ["port", "shipping", "cargo"]}}, {"IS_ALPHA": True, "OP": "*"}, {"LEMMA": {"IN": ["congest", "congestion", "delay", "backlog", "restrict"]}}]
])
token_matcher.add("FACILITY_SHUTDOWN", [
    [{"LEMMA": {"IN": ["close", "shutdown", "halt", "suspend"]}}, {"IS_ALPHA": True, "OP": "*"}, {"LEMMA": {"IN": ["factory", "plant", "warehouse", "facility", "production"]}}],
    [{"LEMMA": {"IN": ["factory", "plant", "warehouse", "facility"]}}, {"IS_ALPHA": True, "OP": "*"}, {"LEMMA": {"IN": ["closure", "close", "shutdown", "halt"]}}]
])
token_matcher.add("LABOR_STRIKE", [
    [{"LEMMA": {"IN": ["worker", "staff", "union", "driver"]}}, {"IS_ALPHA": True, "OP": "*"}, {"LEMMA": {"IN": ["strike", "walkout", "protest"]}}]
])

# Base severity weights per disruption category
CATEGORY_WEIGHTS = {
    "FACILITY_SHUTDOWN": 4,
    "PORT_CONGESTION": 3,
    "LABOR_STRIKE": 3,
    "GEOPOLITICAL_TRADE": 3,
    "GENERAL_DISRUPTION": 1
}

HIGH_IMPACT_LEMMAS = {"halt", "shutdown", "closure", "blockade", "ban", "crisis", "severe", "indefinite", "suspend", "outbreak"}

RSS_SOURCES = [
    ("Supply Chain Dive", "https://www.supplychaindive.com/feeds/news/"),
    ("FreightWaves", "https://www.freightwaves.com/feed"),
    ("Google News", "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en")
]


def clean_headline(raw_title, default_source="Unknown"):
    """Separates the core headline from the trailing ' - Publisher' added by Google News RSS."""
    if " - " in raw_title:
        parts = raw_title.rsplit(" - ", 1)
        return parts[0].strip(), parts[1].strip()
    return raw_title.strip(), default_source


def fetch_supply_chain_news(query="supply chain strike OR port closure OR factory shutdown", limit=7):
    """Fetches recent supply-chain disruption headlines from reliable RSS feeds with fallback."""
    formatted_query = query.replace(" ", "+")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    articles = []

    for source_name, url_template in RSS_SOURCES:
        if len(articles) >= limit:
            break
        rss_url = url_template.format(query=formatted_query)
        feed = feedparser.parse(rss_url, request_headers=headers)

        if feed.get("status") == 503 or not feed.entries:
            continue

        for entry in feed.entries:
            if len(articles) >= limit:
                break
            headline, source = clean_headline(entry.get("title", ""), default_source=source_name)
            articles.append({
                "title": headline,
                "source": source,
                "published": entry.get("published", ""),
                "link": entry.get("link", "")
            })

    if not articles:
        sample_titles = [
            "Philippine DHL workers strike against warehouse closure - World Socialist Web Site",
            "Congested Chinese Ports Cause Supply Chain Operation Issues - Supply Chain Digital Magazine",
            "Amazon to temporarily close Florida facility, lay off nearly 500 - Supply Chain Dive"
        ]
        for raw in sample_titles[:limit]:
            headline, source = clean_headline(raw)
            articles.append({"title": headline, "source": source, "published": "", "link": ""})

    return articles


def calculate_severity(doc, event_types, organizations, locations):
    """Computes a 1-10 severity score and risk level (LOW, MEDIUM, HIGH) from NLP signals."""
    score = sum(CATEGORY_WEIGHTS.get(evt, 1) for evt in event_types)

    if organizations:
        score += 1
    if locations:
        score += 1
    if any(token.lemma_.lower() in HIGH_IMPACT_LEMMAS for token in doc):
        score += 2

    score = min(score, 10)
    if score >= 7:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {"score": score, "level": level}


def analyze_disruption_headline(text):
    """Extracts entities, classifies disruption events via phrase + lemma matching, and scores severity."""
    doc = nlp(text)

    organizations = []
    locations = []
    for ent in doc.ents:
        if ent.label_ == "ORG" and len(ent.text.split()) <= 4 and ent.text not in organizations:
            organizations.append(ent.text)
        elif ent.label_ in ("GPE", "LOC", "FAC") and ent.text not in locations:
            locations.append(ent.text)

    event_types = []
    for match_id, start, end in phrase_matcher(doc) + token_matcher(doc):
        label = nlp.vocab.strings[match_id]
        if label not in event_types:
            event_types.append(label)

    if not event_types:
        event_types.append("GENERAL_DISRUPTION")

    severity = calculate_severity(doc, event_types, organizations, locations)

    return {
        "organizations": organizations,
        "locations": locations,
        "event_types": event_types,
        "severity": severity
    }


if __name__ == "__main__":
    news = fetch_supply_chain_news(limit=5)
    print(f"Analyzed {len(news)} articles:\n")
    for item in news:
        analysis = analyze_disruption_headline(item["title"])
        print(f"Headline: {item['title']} (Source: {item['source']})")
        print("  Event Types:", analysis["event_types"])
        print(f"  Severity: {analysis['severity']['level']} ({analysis['severity']['score']}/10)")
        print("  Orgs:", analysis["organizations"])
        print("  Locations:", analysis["locations"])
        print("-" * 50)