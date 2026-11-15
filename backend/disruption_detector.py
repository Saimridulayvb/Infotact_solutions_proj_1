
import spacy

nlp = spacy.load("en_core_web_sm")

# Supply chain disruption keywords
disruption_keywords = {
    "strike": "LABOUR_STRIKE",
    "flood": "NATURAL_DISASTER",
    "earthquake": "NATURAL_DISASTER",
    "fire": "INDUSTRIAL_ACCIDENT",
    "explosion": "INDUSTRIAL_ACCIDENT",
    "delay": "SHIPPING_DELAY",
    "disrupted": "SUPPLY_CHAIN_DISRUPTION",
    "closure": "PORT_CLOSURE",
    "closed": "PORT_CLOSURE"
}

text = """
A major strike has disrupted operations at Hamburg Port.
Several manufacturers are facing shipping delays.
"""

doc = nlp(text)

print("\n===== AtmoGraph Disruption Detection =====\n")

detected = []

for token in doc:
    word = token.text.lower()

    if word in disruption_keywords:
        event_type = disruption_keywords[word]

        detected.append({
            "keyword": word,
            "event_type": event_type
        })

for event in detected:
    print("Keyword:", event["keyword"])
    print("Event type:", event["event_type"])
    print("-----------------------------")

if not detected:
    print("No disruption detected.")
