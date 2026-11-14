
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from neo4j import GraphDatabase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


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
# 4. DISRUPTION REQUEST MODEL
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

            result = session.run(
                "RETURN 1 AS test"
            )

            record = result.single()

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
# 8. DISRUPTION IMPACT ANALYSIS API
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

            result = session.run(
                query,
                port_name=request.port_name
            )

            record = result.single()

            # Check whether the port exists

            if not record:

                raise HTTPException(
                    status_code=404,
                    detail="Port not found in Neo4j database"
                )

            # Extract graph information

            manufacturers = record["manufacturers"]
            retailers = record["retailers"]
            alternative_ports = record["alternative_ports"]

            # Calculate total impact

            total_impact = (
                len(manufacturers) + len(retailers)
            )

            # Classify disruption severity

            if request.severity == "HIGH" and total_impact >= 3:

                risk_level = "CRITICAL"

            else:

                risk_level = request.severity

            # Determine alternative route status

            if alternative_ports:

                route_status = "ALTERNATIVE ROUTE AVAILABLE"

            else:

                route_status = "NO ALTERNATIVE ROUTE"

            # Return final analysis

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
# 9. CLOSE DATABASE CONNECTION
# ==========================================

@app.on_event("shutdown")
def shutdown():

    driver.close()
