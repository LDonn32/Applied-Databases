
# db_neo4j.py
from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "YOUR_PASSWORD"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def run_query(query, params=None):
    with driver.session() as session:
        return session.run(query, params or {}).data()



 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


d
 
 
 
 


d
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
