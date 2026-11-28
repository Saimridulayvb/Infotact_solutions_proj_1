import unittest
from nlp_disruption import (
    analyze_disruption_headline,
    clean_headline,
    deduplicate_articles,
    normalize_text,
)


class TestNLPDisruption(unittest.TestCase):
    def test_normalize_and_clean_headline(self):
        raw = "PepsiCo\u2019s supply chain faces delays - Supply Chain Dive"
        title, source = clean_headline(raw)
        self.assertEqual(title, "PepsiCo's supply chain faces delays")
        self.assertEqual(source, "Supply Chain Dive")
        self.assertEqual(normalize_text("  Extra   spaces\u2014removed "), "Extra spaces-removed")

    def test_phrase_and_lemma_event_classification(self):
        strike_res = analyze_disruption_headline("Philippine DHL workers strike against warehouse closure")
        self.assertIn("LABOR_STRIKE", strike_res["event_types"])
        self.assertIn("FACILITY_SHUTDOWN", strike_res["event_types"])

        port_res = analyze_disruption_headline("Congested Chinese Ports Cause Supply Chain Issues")
        self.assertIn("PORT_CONGESTION", port_res["event_types"])

        plant_res = analyze_disruption_headline("Cal-Maine halts egg production at Florida plant after outbreak")
        self.assertIn("FACILITY_SHUTDOWN", plant_res["event_types"])

    def test_entity_extraction_and_false_positive_filters(self):
        res = analyze_disruption_headline("Nvidia gets more supplier capacity to meet AI demand")
        self.assertIn("Nvidia", res["organizations"])
        self.assertNotIn("AI", res["locations"])

        loc_res = analyze_disruption_headline("Congested Chinese Ports Cause Supply Chain Operation Issues")
        self.assertIn("Chinese", loc_res["locations"])
        self.assertEqual(loc_res["organizations"], [])

    def test_severity_scoring_levels(self):
        high_res = analyze_disruption_headline(
            "Cal-Maine halts egg production at Florida plant after bird flu outbreak"
        )
        self.assertEqual(high_res["severity"]["level"], "HIGH")
        self.assertGreaterEqual(high_res["severity"]["score"], 7)

        low_res = analyze_disruption_headline("Walmart delivery volume surges in Q3")
        self.assertEqual(low_res["severity"]["level"], "LOW")
        self.assertLess(low_res["severity"]["score"], 4)

    def test_deduplicate_articles(self):
        sample = [
            {"title": "Port closure delays cargo", "source": "Feed A"},
            {"title": "  port closure delays cargo  ", "source": "Feed B"},
            {"title": "Factory shutdown in Texas", "source": "Feed A"},
        ]
        unique = deduplicate_articles(sample)
        self.assertEqual(len(unique), 2)


if __name__ == "__main__":
    unittest.main()