# Imports

from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


# NEO4J CONNECTION


def get_neo4j_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


neo4j_driver = get_neo4j_driver()


def run_query(cypher, params=None):
    with neo4j_driver.session() as session:
        result = session.run(cypher, params or {})
        return list(result)


def close_neo4j_driver():
    neo4j_driver.close()


rooms_cache = None

# OPTION 4 — View Connected Attendees

def get_connected_attendees(attendee_id):
    """
    Returns a list of attendees connected to the given attendee ID.
    Relationship is undirected (CONNECTED_TO in either direction).
    """
    cypher = """
    MATCH (a:Attendee {attendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
    RETURN b.attendeeID AS attendeeID, b.attendeeName AS attendeeName
    ORDER BY b.attendeeID
    """

    records = run_query(cypher, {"id": attendee_id})

    return [
        {"attendeeID": r["attendeeID"], "attendeeName": r["attendeeName"]}
        for r in records
    ]


# OPTION 5 - Add Attendees connection


def neo4j_attendee_exists(attendee_id):
    cypher = """
    MATCH (a:Attendee {attendeeID: $id})
    RETURN a.attendeeID AS attendeeID
    """
    records = run_query(cypher, {"id": attendee_id})
    return len(records) > 0


def create_neo4j_attendee(attendee_id, attendee_name):
    cypher = """
    CREATE (a:Attendee {
        attendeeID: $id,
        attendeeName: $name
    })
    """
    run_query(cypher, {"id": attendee_id, "name": attendee_name})


def attendees_already_connected(id1, id2):
    cypher = """
    MATCH (a:Attendee {attendeeID: $id1})-[:CONNECTED_TO]-(b:Attendee {attendeeID: $id2})
    RETURN b.attendeeID AS attendeeID
    """
    records = run_query(cypher, {"id1": id1, "id2": id2})
    return len(records) > 0


def create_connection(id1, id2):
    cypher = """
    MATCH (a:Attendee {attendeeID: $id1})
    MATCH (b:Attendee {attendeeID: $id2})
    MERGE (a)-[:CONNECTED_TO]->(b)
    MERGE (b)-[:CONNECTED_TO]->(a)
    """
    run_query(cypher, {"id1": id1, "id2": id2})


# Sanity check for Neo4j connection when running this module directly

if __name__ == "__main__":
    try:
        print("Testing Neo4j connection...")
        with neo4j_driver.session() as session:
            result = session.run("RETURN 1 AS test")
            print("Neo4j test query result:", result.single()["test"])
    except Exception as e:
        print("Neo4j connection failed:", e)
    finally:
        close_neo4j_driver()

