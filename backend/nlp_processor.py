
import spacy
import json


# ==========================================
# 1. LOAD SPACY NLP MODEL
# ==========================================

nlp = spacy.load("en_core_web_sm")


# ==========================================
# 2. DISRUPTION KEYWORDS
# ==========================================

DISRUPTION_KEYWORDS = {
    "strike": "LABOUR_STRIKE",
    "flood": "NATURAL_DISASTER",
    "earthquake": "NATURAL_DISASTER",
    "fire": "INDUSTRIAL_ACCIDENT",
    "explosion": "INDUSTRIAL_ACCIDENT",
    "delay": "SHIPPING_DELAY",
    "delays": "SHIPPING_DELAY",
    "disrupted": "SUPPLY_CHAIN_DISRUPTION",
    "disruption": "SUPPLY_CHAIN_DISRUPTION",
    "closure": "PORT_CLOSURE",
    "closed": "PORT_CLOSURE"
}


# ==========================================
# 3. ANALYZE NEWS ARTICLE
# ==========================================

def analyze_news(text):

    # Process news using spaCy
    doc = nlp(text)

    # --------------------------------------
    # Extract Named Entities
    # --------------------------------------

    entities = []

    for entity in doc.ents:

        entities.append({
            "name": entity.text,
            "type": entity.label_
        })

    # --------------------------------------
    # Detect Supply Chain Disruptions
    # --------------------------------------

    disruptions = []

    for token in doc:

        word = token.text.lower()

        if word in DISRUPTION_KEYWORDS:

            disruptions.append({
                "keyword": word,
                "event_type": DISRUPTION_KEYWORDS[word]
            })

    # --------------------------------------
    # Prepare Final Result
    # --------------------------------------

    result = {
        "original_text": text,
        "entities": entities,
        "disruptions": disruptions
    }

    return result


# ==========================================
# 4. TEST NLP PROCESSOR
# ==========================================

if __name__ == "__main__":

    news = """
    A major strike has disrupted operations at Hamburg Port.
    Samsung Components and Nova Components may face shipping delays.
    """

    result = analyze_news(news)

    print("\n========== ATMOGRAPH NLP ANALYSIS ==========\n")

    print(json.dumps(result, indent=4))

    print("\n========== ANALYSIS COMPLETED ==========\n")
