
// ==========================================
// ATMOGRAPH - NEO4J IMPORT VERIFICATION
// ==========================================

// 1. Create unique constraints

CREATE CONSTRAINT provider_id_unique IF NOT EXISTS
FOR (n:Provider)
REQUIRE n.provider_id IS UNIQUE;

CREATE CONSTRAINT input_id_unique IF NOT EXISTS
FOR (n:SupplyChainInput)
REQUIRE n.input_id IS UNIQUE;

CREATE CONSTRAINT stage_id_unique IF NOT EXISTS
FOR (n:Stage)
REQUIRE n.stage_id IS UNIQUE;


// 2. Verify node counts

MATCH (n:Provider)
RETURN count(n) AS Provider_Count;

MATCH (n:SupplyChainInput)
RETURN count(n) AS SupplyChainInput_Count;

MATCH (n:Stage)
RETURN count(n) AS Stage_Count;


// 3. Verify relationship counts

MATCH ()-[r:PROVIDES]->()
RETURN count(r) AS PROVIDES_Count;

MATCH ()-[r:GOES_INTO]->()
RETURN count(r) AS GOES_INTO_Count;

MATCH ()-[r:IS_TYPE_OF]->()
RETURN count(r) AS IS_TYPE_OF_Count;

MATCH ()-[r:IN_STAGE]->()
RETURN count(r) AS IN_STAGE_Count;


// 4. Check missing Provider IDs

MATCH (n:Provider)
WHERE n.provider_id IS NULL
RETURN count(n) AS Missing_Provider_IDs;


// 5. Check missing SupplyChainInput IDs

MATCH (n:SupplyChainInput)
WHERE n.input_id IS NULL
RETURN count(n) AS Missing_Input_IDs;


// 6. Check missing Stage IDs

MATCH (n:Stage)
WHERE n.stage_id IS NULL
RETURN count(n) AS Missing_Stage_IDs;


// 7. Inspect sample supply relationships

MATCH (p:Provider)-[r:PROVIDES]->(i:SupplyChainInput)
RETURN p.provider_name, i.input_name, r.year
LIMIT 10;
