
import spacy
import json


# ==========================================
# 1. LOAD SPACY ENGLISH MODEL
# ==========================================

nlp = spacy.load("en_core_web_sm")


# ==========================================
# 2. DISRUPTION KEYWORD DICTIONARY
# ==========================================

DISRUPTION_KEYWORDS = {

    "strike": "LABOUR_STRIKE",

    "flood": "NATURAL_DISASTER",
    "earthquake": "NATURAL_DISASTER",

    "fire": "INDUSTRIAL_ACCIDENT",
    "explosion": "INDUSTRIAL_ACCIDENT",

    "delay": "SHIPPING_DELAY",

    "disrupt": "SUPPLY_CHAIN_DISRUPTION",
    "disruption": "SUPPLY_CHAIN_DISRUPTION",

    "close": "PORT_CLOSURE",
    "closure": "PORT_CLOSURE"
}


# ==========================================
# 3. NEWS ANALYSIS FUNCTION
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
    # Detect Disruptions Using Lemmatization
    # --------------------------------------

    disruptions = []

    for token in doc:

        # Convert word into its base form
        base_word = token.lemma_.lower()

        # Handle flooding manually
        if token.text.lower() == "flooding":
            base_word = "flood"

        # Check base word in dictionary
        if base_word in DISRUPTION_KEYWORDS:

            disruptions.append({

                "keyword": token.text.lower(),

                "event_type": DISRUPTION_KEYWORDS[base_word]

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
    Workers are striking at Hamburg Port.
    Heavy flooding has disrupted operations.
    Shipping delays are affecting manufacturers.
    The port was closed due to severe weather.
    """

    result = analyze_news(news)

    print(json.dumps(result, indent=4))
