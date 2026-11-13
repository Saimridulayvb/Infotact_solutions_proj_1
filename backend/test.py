
import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv(Path(__file__).with_name(".env"))

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Connect to Neo4j
driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    driver.verify_connectivity()
    print("Connected to AtmoGraphDB!")

    with driver.session() as session:

        # Calculate total disruption impact
        result = session.run("""
            MATCH (p:Port {name: "Rotterdam Port"})
                  -[:DISTRIBUTES_TO]->(r:Retailer)

            OPTIONAL MATCH (r)-[:SUPPLIES_TO]->(c:Customer)

            RETURN
                count(DISTINCT p) AS disrupted_ports,
                count(DISTINCT r) AS direct_impact,
                count(DISTINCT c) AS indirect_impact,
                count(DISTINCT r) + count(DISTINCT c)
                    AS total_affected_entities
        """)

        record = result.single()

        print("\n--- AtmoGraph Total Impact Analysis ---")

        print("Disrupted Ports:", record["disrupted_ports"])
        print("Directly Affected Retailers:", record["direct_impact"])
        print("Indirectly Affected Customers:", record["indirect_impact"])
        print("Total Affected Entities:", record["total_affected_entities"])

        # Step 10: Disruption Severity Classification
        result = session.run("""
            MATCH (p:Port {name: "Rotterdam Port"})
                  -[:EXPERIENCING]->(d:Disruption)

            OPTIONAL MATCH (p)-[:DISTRIBUTES_TO]->(r:Retailer)
            OPTIONAL MATCH (r)-[:SUPPLIES_TO]->(c:Customer)

            WITH p, d,
                 count(DISTINCT r) AS direct_impact,
                 count(DISTINCT c) AS indirect_impact

            WITH p, d, direct_impact, indirect_impact,
                 direct_impact + indirect_impact AS total_impact

            RETURN
                d.name AS disruption,
                d.severity AS original_severity,
                total_impact,
                CASE
                    WHEN d.severity = "HIGH"
                         AND total_impact >= 3
                    THEN "CRITICAL"

                    WHEN d.severity = "HIGH"
                    THEN "HIGH"

                    WHEN d.severity = "MEDIUM"
                    THEN "MEDIUM"

                    ELSE "LOW"
                END AS risk_level
        """)

        record = result.single()

        print("\n--- AtmoGraph Severity Classification ---")

        if record:
            print("Disruption:", record["disruption"])
            print("Original Severity:", record["original_severity"])
            print("Total Impact:", record["total_impact"])
            print("Final Risk Level:", record["risk_level"])

finally:
    driver.close()
