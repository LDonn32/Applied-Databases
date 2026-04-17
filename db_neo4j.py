#!/usr/bin/env python3

from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable

def get_neo4j_driver(uri, user, password):
    """
    Creates a Neo4j driver for database operations.
    
    Args:
        uri: Neo4j connection URI (e.g., 'neo4j://localhost:7687')
        user: Neo4j username
        password: Neo4j password
    
    Returns:
        A Neo4j driver object or None if connection fails.
    """
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("Neo4j connection successful.")
        return driver
    except AuthError as err:
        print(f"Neo4j error: Authentication failed - {err}")
        return None
    except ServiceUnavailable as err:
        print(f"Neo4j error: Service unavailable - {err}")
        return None
    except Exception as err:
        print(f"Neo4j error: {err}")
        return None


def close_neo4j_driver(driver):
    """Closes a Neo4j driver connection."""
    if driver:
        driver.close()
        print("Neo4j connection closed.")


def execute_neo4j_query(driver, query):
    """
    Executes a Cypher query on Neo4j.
    
    Args:
        driver: Neo4j driver object
        query: Cypher query string
    
    Returns:
        Query results or None if execution fails.
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            return result.data()
    except Exception as err:
        print(f"Neo4j query error: {err}")
        return None
