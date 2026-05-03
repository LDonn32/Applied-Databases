# Imports

from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD



# Neo4j Client class to manage connection and queries   

class Neo4jClient:
    def __init__(self, uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def run_query(self, cypher, parameters=None):
        parameters = parameters or {}
        with self._driver.session() as session:
            result = session.run(cypher, parameters)
            return [record for record in result]


# Create a single shared Neo4j client instance
neo4j_client = Neo4jClient()



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

    records = neo4j_client.run_query(cypher, {"id": attendee_id})

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
    records = neo4j_client.run_query(cypher, {"id": attendee_id})
    return len(records) > 0


def create_neo4j_attendee(attendee_id, attendee_name):
    cypher = """
    CREATE (a:Attendee {
        attendeeID: $id,
        attendeeName: $name
    })
    """
    neo4j_client.run_query(cypher, {"id": attendee_id, "name": attendee_name})


def attendees_already_connected(id1, id2):
    cypher = """
    MATCH (a:Attendee {attendeeID: $id1})-[:CONNECTED_TO]-(b:Attendee {attendeeID: $id2})
    RETURN b.attendeeID AS attendeeID
    """
    records = neo4j_client.run_query(cypher, {"id1": id1, "id2": id2})
    return len(records) > 0


def create_connection(id1, id2):
    cypher = """
    MATCH (a:Attendee {attendeeID: $id1})
    MATCH (b:Attendee {attendeeID: $id2})
    MERGE (a)-[:CONNECTED_TO]->(b)
    MERGE (b)-[:CONNECTED_TO]->(a)
    """
    neo4j_client.run_query(cypher, {"id1": id1, "id2": id2})





