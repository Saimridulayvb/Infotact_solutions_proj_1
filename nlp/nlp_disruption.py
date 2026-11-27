from datetime import datetime, timezone
import hashlib
import json
import unicodedata
import feedparser
import spacy
from spacy.matcher import Matcher, PhraseMatcher

# Load small English NLP model
nlp = spacy.load("en_core_web_sm")

# Add EntityRuler before NER to prevent false positives and catch key locations/companies
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns([
    {"label": "GPE", "pattern": [{"LOWER": {"IN": ["chinese", "philippine", "egyptian", "russian", "indian", "american"]}}]},
    {"label": "ORG", "pattern": [{"LOWER": {"IN": ["nvidia", "walmart", "amazon", "dhl", "maersk", "tsmc", "pepsico", "usps"]}}]}
])

IGNORED_LOCATIONS = {"ai", "q1", "q2", "q3", "q4"}

# 1. Exact phrase matcher for multi-word disruption terms
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

DISRUPTION_PATTERNS = {
    "LABOR_STRIKE": [
        "strike", "workers strike", "walkout", "labor dispute",
        "union strike", "lay off", "layoffs", "workforce cuts", "job cuts"
    ],
    "PORT_CONGESTION": [
        "port closure", "congested ports", "port congestion",
        "shipping delay", "vessel backlog", "port restrictions"
    ],
    "FACILITY_SHUTDOWN": [
        "factory shutdown", "warehouse closure", "plant closure",
        "temporarily close", "halt production", "production halt"
    ],
    "GEOPOLITICAL_TRADE": [
        "tariff", "sanctions", "export ban", "trade restriction",
        "blockade", "border closure"
    ]
}

for category, phrases in DISRUPTION_PATTERNS.items():
    patterns = [nlp.make_doc(phrase) for phrase in phrases]
    phrase_matcher.add(category, patterns)

# 2. Token-level lemma matcher to catch word variations & modifiers
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
    [{"LEMMA": {"IN": ["worker", "staff", "union", "driver", "workforce"]}}, {"IS_ALPHA": True, "OP": "*"}, {"LEMMA": {"IN": ["strike", "walkout", "protest", "cut", "layoff"]}}]
])

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

DEFAULT_QUERIES = [
    "supply chain strike OR port closure",
    "factory shutdown OR shipping delay"
]


def normalize_text(text):
    """Normalizes smart quotes/dashes (e.g., '\\u2019') into clean ASCII-friendly punctuation."""
    cleaned = unicodedata.normalize("NFKC", text)
    replacements = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-"}
    for bad, good in replacements.items():
        cleaned = cleaned.replace(bad, good)
    return " ".join(cleaned.split())


def clean_headline(raw_title, default_source="Unknown"):
    """Normalizes text and separates the core headline from trailing ' - Publisher'."""
    normalized = normalize_text(raw_title)
    if " - " in normalized:
        parts = normalized.rsplit(" - ", 1)
        return parts[0].strip(), parts[1].strip()
    return normalized.strip(), default_source


def deduplicate_articles(articles):
    """Removes duplicate articles based on normalized headline text."""
    seen = set()
    unique = []
    for article in articles:
        norm_title = article["title"].lower().strip()
        if norm_title and norm_title not in seen:
            seen.add(norm_title)
            unique.append(article)
    return unique


def fetch_supply_chain_news(queries=None, limit=7):
    """Aggregates supply-chain headlines across multiple queries and RSS sources with error handling."""
    if isinstance(queries, str):
        queries = [queries]
    elif not queries:
        queries = DEFAULT_QUERIES

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    articles = []

    for query in queries:
        formatted_query = query.replace(" ", "+")
        for source_name, url_template in RSS_SOURCES:
            if len(articles) >= limit * 2:
                break
            rss_url = url_template.format(query=formatted_query)
            try:
                feed = feedparser.parse(rss_url, request_headers=headers)
                if feed.get("status") in (403, 429, 503) or not feed.entries:
                    continue

                for entry in feed.entries:
                    headline, source = clean_headline(entry.get("title", ""), default_source=source_name)
                    articles.append({
                        "title": headline,
                        "source": source,
                        "published": entry.get("published", ""),
                        "link": entry.get("link", "")
                    })
            except Exception:
                continue

    if not articles:
        sample_titles = [
            "Philippine DHL workers strike against warehouse closure - World Socialist Web Site",
            "Congested Chinese Ports Cause Supply Chain Operation Issues - Supply Chain Digital Magazine",
            "Amazon to temporarily close Florida facility, lay off nearly 500 - Supply Chain Dive"
        ]
        for raw in sample_titles:
            headline, source = clean_headline(raw)
            articles.append({"title": headline, "source": source, "published": "", "link": ""})

    return deduplicate_articles(articles)[:limit]


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
        elif (
            ent.label_ in ("GPE", "LOC", "FAC")
            and ent.text.lower() not in IGNORED_LOCATIONS
            and ent.text not in locations
        ):
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


def get_disruption_report(queries=None, limit=5):
    """Builds a structured JSON-serializable disruption report for backend API integration."""
    articles = fetch_supply_chain_news(queries=queries, limit=limit)
    events = []

    for item in articles:
        analysis = analyze_disruption_headline(item["title"])
        article_id = hashlib.sha256(item["title"].encode("utf-8")).hexdigest()[:12]
        events.append({
            "id": article_id,
            "title": item["title"],
            "source": item["source"],
            "published": item["published"],
            "link": item["link"],
            "event_types": analysis["event_types"],
            "organizations": analysis["organizations"],
            "locations": analysis["locations"],
            "severity": analysis["severity"]
        })

    events.sort(key=lambda e: e["severity"]["score"], reverse=True)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_events": len(events),
        "high_severity_count": sum(1 for e in events if e["severity"]["level"] == "HIGH"),
        "events": events
    }


if __name__ == "__main__":
    report = get_disruption_report(limit=5)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    with open("nlp/sample_output.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)