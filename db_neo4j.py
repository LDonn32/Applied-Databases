
# db_neo4j.py
from neo4j import GraphDatabase, basic_auth

# Edit these to match your Neo4j local DB credentials
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j"   # <-- change this

_driver = None


def get_neo4j_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))
    return _driver


def close_neo4j_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None

 
 
 
 
 
 
 
 
 
 
 
 
