
import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Sample supply chain news
text = """
A major strike has disrupted operations at Hamburg Port.
Samsung Components and Nova Components may face delays.
Retailers TechWorld and EuroElectronics are also affected.
"""

# Process the text
doc = nlp(text)

# Display extracted entities
print("\n===== AtmoGraph NLP Entity Extraction =====\n")

for entity in doc.ents:
    print("Entity:", entity.text)
    print("Type:", entity.label_)
    print("Description:", spacy.explain(entity.label_))
    print("-----------------------------------")
