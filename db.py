# Database access layer for the Conference Management app.

# datetime import is used for validating and formatting date fields from MySQLq
import datetime

# MySQL access is done via PyMySQL, a pure Python MySQL client library
import pymysql

# Neo4j access is done via the official Neo4j Python driver, which supports Bolt protocol
from neo4j import GraphDatabase

# Configuration for MySQL Connection
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "appdbproj"
MYSQL_PORT = 3306

# Configuration for Neo4j Connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4jneo4j"
NEO4J_DATABASE = "appdbprojNeo4j"  



# Simple connection helpers
# See: https://pymysql.readthedocs.io/en/latest/modules/connections.html#pymysql.connections.Connection

def connect():
    """Return a new PyMySQL connection to the MySQL server."""
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        port=MYSQL_PORT,
        cursorclass=pymysql.cursors.Cursor,  
        autocommit=False
    )

# Simple helper for Neo4j connection using the official Neo4j Python driver
# See: https://neo4j.com/docs/api/python-driver/current/driver.html#driver

def connect_neo4j():
    """Return a neo4j.Driver instance for the configured Neo4j server."""
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Simple in-memory cache for rooms to avoid repeated queries 
rooms_cache = None





#  MySQL functions (Options 1,2,3,6) 

# Option 1 - View Speakers & Sessions

def view_speakers_sessions():
    """Option 1 - prompt for a speaker name and print matching sessions and rooms."""
    speaker = input("Enter speaker name: ").strip()
    print(f"\nSessions details for {speaker}")
    print("------------------------------------------")

    conn = connect()
    try:
        cur = conn.cursor()
        query = """
            SELECT DISTINCT s.speakerName, s.sessionTitle, r.roomName
            FROM session s
            JOIN room r ON s.roomID = r.roomID
            WHERE s.speakerName LIKE %s
        """
        cur.execute(query, (f"%{speaker}%",))
        rows = cur.fetchall()

        if rows:
            for speakerName, sessionTitle, roomName in rows:
                print(f"Speaker: {speakerName} | Session: {sessionTitle} | Room: {roomName}")
        else:
            print("No speaker was found of that name")
    finally:
        conn.close()

# Option 2 - View Attendees by Company

def view_attendees_by_company():
    """Option 2 - prompt for a company ID and list attendees and their sessions."""
    conn = connect()
    try:
        cur = conn.cursor()
        while True:
            user_input = input("Enter Company ID: ").strip()
            try:
                company_id = int(user_input)
                if company_id > 0:
                    break
                else:
                    print("*** ERROR *** Invalid Company ID")
            except ValueError:
                print("*** ERROR *** Invalid Company ID")

        cur.execute("SELECT companyName FROM company WHERE companyID = %s", (company_id,))
        company = cur.fetchone()
        if not company:
            print(f"Company with ID {company_id} doesn't exist")
            return
        company_name = company[0]

        query = """
            SELECT DISTINCT 
                a.attendeeName, 
                a.attendeeDOB, 
                s.sessionTitle, 
                s.speakerName, 
                s.sessionDate, 
                r.roomName
            FROM attendee a
            INNER JOIN attendee_session asn ON a.attendeeID = asn.attendeeID
            INNER JOIN session s ON asn.sessionID = s.sessionID
            INNER JOIN room r ON s.roomID = r.roomID
            WHERE a.attendeeCompanyID = %s
        """
        cur.execute(query, (company_id,))
        rows = cur.fetchall()

        if rows:
            print(f"\n{company_name} Attendees:\n")
            for row in rows:
                attendee_name = row[0]
                attendee_dob = row[1].strftime("%Y-%m-%d") if isinstance(row[1], (datetime.date, datetime.datetime)) else str(row[1])
                session_title = row[2]
                speaker_name = row[3]
                session_date = row[4].strftime("%Y-%m-%d") if isinstance(row[4], (datetime.date, datetime.datetime)) else str(row[4])
                room_name = row[5]
                print(
                    f"Attendee: {attendee_name} | DOB: {attendee_dob} | "
                    f"Session: {session_title} | Speaker: {speaker_name} | "
                    f"Date: {session_date} | Room: {room_name}"
                )
        else:
            print(f"No attendees found for {company_name}")
    finally:
        conn.close()

# Option 3 - Add New Attendee

def add_new_attendee():
    """Option 3 - prompt for attendee details, validate and insert into attendee table."""
    try:
        new_user_id = int(input("Insert new user ID: ").strip())
    except ValueError:
        print("*** ERROR *** Attendee ID must be a number")
        return

    new_user_name = input("Insert new user Name: ").strip()
    new_user_dob = input("Insert DOB (YYYY-MM-DD): ").strip()
    new_user_gender = input("Insert Gender (Male/Female): ").strip()
    try:
        new_user_company = int(input("Insert Company ID: ").strip())
    except ValueError:
        print("*** ERROR *** Company ID must be a number")
        return

    # Validate date format
    try:
        datetime.datetime.strptime(new_user_dob, "%Y-%m-%d")
    except ValueError:
        print("*** ERROR *** Invalid date format")
        return

    conn = connect()
    try:
        cur = conn.cursor()
        # Check for duplicate attendee ID
        cur.execute("SELECT COUNT(*) FROM attendee WHERE attendeeID = %s", (new_user_id,))
        if cur.fetchone()[0] > 0:
            print("*** ERROR *** Attendee ID already exists")
            return

        # Check company exists
        cur.execute("SELECT COUNT(*) FROM company WHERE companyID = %s", (new_user_company,))
        if cur.fetchone()[0] == 0:
            print("*** ERROR *** Company does not exist")
            return

        cur.execute("""
            INSERT INTO attendee 
            (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s)
        """, (new_user_id, new_user_name, new_user_dob, new_user_gender, new_user_company))

        conn.commit()
        print("Attendee added")
    except Exception as e:
        conn.rollback()
        print("*** ERROR *** Could not add attendee:", e)
    finally:
        conn.close()


# Option 6 - View Rooms

def view_rooms():
    """Option 6 - print cached list of rooms (caches on first call)."""
    global rooms_cache
    if rooms_cache is None:
        conn = connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT roomID, roomName, capacity FROM room")
            rooms_cache = cur.fetchall()
        finally:
            conn.close()

    if not rooms_cache:
        print("No rooms found")
        return

    print("\nROOMS LIST")
    print("----------------")
    for room in rooms_cache:
        print(f"RoomID: {room[0]} | Name: {room[1]} | Capacity: {room[2]}")




# Neo4j functions (Options 4,5) 

# Option 4 - View Connected Attendees

def view_connected_attendees():
    """Option 4 - given an attendee ID, list connected attendees (Neo4j) with names from MySQL."""
    try:
        attendee_id = int(input("Enter Attendee ID: ").strip())
    except ValueError:
        print("*** ERROR *** Invalid attendee ID")
        return

    # Verify attendee exists in MySQL
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (attendee_id,))
        result = cur.fetchone()
        if not result:
            print("*** ERROR *** Attendee does not exist")
            return
        attendee_name = result[0]
    finally:
        conn.close()

    # Query Neo4j for connections
    driver = connect_neo4j()
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            print(f"\n{attendee_id} | {attendee_name}")
            print("------------------------------")
            query = """
                MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
                RETURN b.AttendeeID AS id
            """
            results = session.run(query, id=attendee_id)
            connections = [record["id"] for record in results]

            if not connections:
                print("No connections")
                return

            # Fetch names from MySQL for the connected IDs
            conn = connect()
            try:
                cur = conn.cursor()
                placeholders = ",".join(["%s"] * len(connections))
                cur.execute(f"SELECT attendeeID, attendeeName FROM attendee WHERE attendeeID IN ({placeholders})", tuple(connections))
                name_map = dict(cur.fetchall())
            finally:
                conn.close()

            for cid in connections:
                name = name_map.get(cid, "Unknown")
                print(f"{cid} | {name}")
    finally:
        driver.close()

# Option 5 - Add Attendees connection

def add_attendee_connection():
    """Option 5 - create a bidirectional connection between two attendees in Neo4j."""
    conn = connect()
    try:
        cur = conn.cursor()
        driver = connect_neo4j()
        try:
            with driver.session(database=NEO4J_DATABASE) as session:
                while True:
                    try:
                        id1 = int(input("Enter first Attendee ID: ").strip())
                        id2 = int(input("Enter second Attendee ID: ").strip())
                    except ValueError:
                        print("*** ERROR *** Attendee IDs must be numbers")
                        continue

                    if id1 == id2:
                        print("*** ERROR *** An attendee cannot connect to him/herself")
                        continue

                    # Check both IDs exist in MySQL
                    cur.execute("SELECT COUNT(*) FROM attendee WHERE attendeeID IN (%s, %s)", (id1, id2))
                    count = cur.fetchone()[0]
                    if count < 2:
                        print("*** ERROR *** One or both attendee IDs do not exist")
                        continue

                    # Ensure nodes exist in Neo4j
                    session.run("""
                        MERGE (a:Attendee {AttendeeID: $id1})
                        MERGE (b:Attendee {AttendeeID: $id2})
                    """, id1=id1, id2=id2)

                    # Check existing connection
                    check = session.run("""
                        MATCH (a:Attendee {AttendeeID: $id1})-[:CONNECTED_TO]-(b:Attendee {AttendeeID: $id2})
                        RETURN count(*) AS c
                    """, id1=id1, id2=id2)

                    if check.single()["c"] > 0:
                        print("*** ERROR *** These attendees are already connected")
                        continue

                    # Create connection (undirected)
                    session.run("""
                        MATCH (a:Attendee {AttendeeID: $id1})
                        MATCH (b:Attendee {AttendeeID: $id2})
                        MERGE (a)-[:CONNECTED_TO]-(b)
                    """, id1=id1, id2=id2)

                    print(f"Attendee {id1} is now connected to Attendee {id2}")
                    break
        finally:
            driver.close()
    finally:
        conn.close()
