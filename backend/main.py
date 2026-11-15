
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from neo4j import GraphDatabase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.nlp_processor import analyze_news


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(Path(__file__).with_name(".env"))

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USERNAME, PASSWORD]):
    raise RuntimeError(
        "Neo4j credentials missing. Check backend/.env"
    )


# ==========================================
# 2. CONNECT TO NEO4J
# ==========================================

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# ==========================================
# 3. INITIALIZE FASTAPI
# ==========================================

app = FastAPI(
    title="AtmoGraph API",
    description="Supply Chain Ripple Effect Predictor",
    version="1.0.0"
)


# ==========================================
# 4. REQUEST MODELS
# ==========================================

class DisruptionRequest(BaseModel):

    disruption: str = Field(
        ...,
        description="Name of the supply chain disruption"
    )

    port_name: str = Field(
        ...,
        description="Port affected by the disruption"
    )

    severity: Literal["LOW", "MEDIUM", "HIGH"] = "HIGH"


class NewsRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        description="Supply chain news article"
    )

    severity: Literal["LOW", "MEDIUM", "HIGH"] = "HIGH"


# ==========================================
# 5. HOME API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to AtmoGraph API!",
        "project": "AtmoGraph",
        "status": "Running"
    }


# ==========================================
# 6. APPLICATION HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "Healthy",
        "application": "AtmoGraph"
    }


# ==========================================
# 7. NEO4J DATABASE HEALTH CHECK
# ==========================================

@app.get("/db-health")
def database_health():

    try:

        with driver.session(database="neo4j") as session:

            record = session.run(
                "RETURN 1 AS test"
            ).single()

            return {
                "status": "Connected",
                "database": "AtmoGraphDB",
                "test": record["test"]
            }

    except Exception as e:

        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to Neo4j: {str(e)}"
        )


# ==========================================
# 8. NLP NEWS ANALYSIS API
# ==========================================

@app.post("/analyze-news")
def analyze_news_api(request: NewsRequest):

    try:

        result = analyze_news(request.text)

        return {
            "status": "success",
            "project": "AtmoGraph",
            "analysis": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"News analysis failed: {str(e)}"
        )


# ==========================================
# 9. EXISTING DISRUPTION IMPACT API
# ==========================================

@app.post("/analyze-disruption")
def analyze_disruption(request: DisruptionRequest):

    query = """

        MATCH (p:Port {name: $port_name})

        OPTIONAL MATCH
            (m:Manufacturer)-[:SHIPS_THROUGH]->(p)

        WITH p,
             collect(DISTINCT m.name) AS manufacturers

        OPTIONAL MATCH
            (p)-[:DISTRIBUTES_TO]->(r:Retailer)

        WITH p,
             manufacturers,
             collect(DISTINCT r.name) AS retailers

        OPTIONAL MATCH
            (m2:Manufacturer)-[:SHIPS_THROUGH]->(alt:Port)

        WHERE m2.name IN manufacturers
          AND alt <> p

        RETURN
            p.name AS disrupted_port,
            manufacturers,
            retailers,
            collect(DISTINCT alt.name) AS alternative_ports

    """

    try:

        with driver.session(database="neo4j") as session:

            record = session.run(
                query,
                port_name=request.port_name
            ).single()

            if not record:

                raise HTTPException(
                    status_code=404,
                    detail="Port not found in Neo4j database"
                )

            manufacturers = record["manufacturers"]
            retailers = record["retailers"]
            alternative_ports = record["alternative_ports"]

            total_impact = len(manufacturers) + len(retailers)

            if request.severity == "HIGH" and total_impact >= 3:
                risk_level = "CRITICAL"
            else:
                risk_level = request.severity

            route_status = (
                "ALTERNATIVE ROUTE AVAILABLE"
                if alternative_ports
                else "NO ALTERNATIVE ROUTE"
            )

            return {
                "disruption": request.disruption,
                "disrupted_port": record["disrupted_port"],
                "original_severity": request.severity,
                "affected_manufacturers": manufacturers,
                "affected_retailers": retailers,
                "alternative_ports": alternative_ports,
                "total_affected_entities": total_impact,
                "risk_level": risk_level,
                "route_status": route_status
            }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Disruption analysis failed: {str(e)}"
        )


# ==========================================
# 10. AUTOMATIC NEWS-TO-GRAPH IMPACT API
# ==========================================

@app.post("/analyze-news-impact")
def analyze_news_impact(request: NewsRequest):

    try:

        # STEP 1: Process news using NLP
        nlp_result = analyze_news(request.text)

        # STEP 2: Check for detected disruptions
        if not nlp_result["disruptions"]:

            return {
                "status": "no_disruption_detected",
                "message": "No known disruption keywords found.",
                "nlp_analysis": nlp_result
            }

        # STEP 3: Get available ports from Neo4j
        with driver.session(database="neo4j") as session:

            port_result = session.run(
                """
                MATCH (p:Port)
                RETURN p.name AS name
                """
            )

            port_names = [
                record["name"]
                for record in port_result
                if record["name"]
            ]

            # STEP 4: Match a port mentioned in the article
            news_lower = request.text.lower()

            matching_ports = [
                port for port in port_names
                if port.lower() in news_lower
            ]

            # Prefer the longest matching port name
            matching_ports.sort(
                key=len,
                reverse=True
            )

            if not matching_ports:

                return {
                    "status": "port_not_found",
                    "message": (
                        "No known port from Neo4j "
                        "was identified in the news article."
                    ),
                    "available_ports": port_names,
                    "nlp_analysis": nlp_result
                }

            matched_port = matching_ports[0]

            # STEP 5: Analyze the matched port in Neo4j
            impact_query = """

                MATCH (p:Port {name: $port_name})

                OPTIONAL MATCH
                    (m:Manufacturer)-[:SHIPS_THROUGH]->(p)

                WITH p,
                     collect(DISTINCT m.name) AS manufacturers

                OPTIONAL MATCH
                    (p)-[:DISTRIBUTES_TO]->(r:Retailer)

                WITH p,
                     manufacturers,
                     collect(DISTINCT r.name) AS retailers

                OPTIONAL MATCH
                    (m2:Manufacturer)-[:SHIPS_THROUGH]->(alt:Port)

                WHERE m2.name IN manufacturers
                  AND alt <> p

                RETURN
                    p.name AS disrupted_port,
                    manufacturers,
                    retailers,
                    collect(DISTINCT alt.name) AS alternative_ports

            """

            record = session.run(
                impact_query,
                port_name=matched_port
            ).single()

            if not record:

                raise HTTPException(
                    status_code=404,
                    detail="Matched port not found in Neo4j."
                )

            # STEP 6: Extract graph results
            manufacturers = record["manufacturers"]
            retailers = record["retailers"]
            alternative_ports = record["alternative_ports"]

            # STEP 7: Calculate impact
            total_impact = (
                len(manufacturers) + len(retailers)
            )

            if request.severity == "HIGH" and total_impact >= 3:

                risk_level = "CRITICAL"

            else:

                risk_level = request.severity

            # STEP 8: Check alternative route availability
            route_status = (
                "ALTERNATIVE ROUTE AVAILABLE"
                if alternative_ports
                else "NO ALTERNATIVE ROUTE"
            )

            # STEP 9: Return complete analysis
            return {

                "status": "success",

                "project": "AtmoGraph",

                "nlp_analysis": nlp_result,

                "graph_analysis": {

                    "detected_disruption":
                        nlp_result["disruptions"][0]["event_type"],

                    "matched_port": matched_port,

                    "disrupted_port":
                        record["disrupted_port"],

                    "severity": request.severity,

                    "affected_manufacturers": manufacturers,

                    "affected_retailers": retailers,

                    "total_affected_entities": total_impact,

                    "alternative_ports": alternative_ports,

                    "risk_level": risk_level,

                    "route_status": route_status

                }

            }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"News impact analysis failed: {str(e)}"
        )


# ==========================================
# 11. CLOSE DATABASE CONNECTION
# ==========================================

@app.on_event("shutdown")
def shutdown():

    driver.close()
