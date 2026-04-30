#! /usr/bin/env python3

# main.py
import datetime
from db_mysql import get_mysql_connection, close_mysql_connection
from db_neo4j import get_neo4j_driver, close_neo4j_driver


def view_speakers_sessions():
    speaker = input("Enter speaker name: ").strip()
    print(f"\nSessions details for '{speaker}'")
    print("------------------------------------------")

    conn = get_mysql_connection()
    if not conn:
        print("Database connection failed.")
        return

    try:
        cur = conn.cursor()
        query = """
            SELECT DISTINCT s.speakerName, se.sessionTitle, r.roomName
            FROM session se
            JOIN speaker s ON se.speakerID = s.speakerID
            JOIN room r ON se.roomID = r.roomID
            WHERE s.speakerName LIKE %s
        """
        cur.execute(query, (f"%{speaker}%",))
        rows = cur.fetchall()

        if rows:
            for speakerName, sessionTitle, roomName in rows:
                print(f"Speaker: {speakerName} | Session: {sessionTitle} | Room: {roomName}")
        else:
            print("No speaker was found of that name")
    except Exception as e:
        print(f"Error querying MySQL: {e}")
    finally:
        cur.close()
        close_mysql_connection(conn)


def view_attendees_by_company():
    conn = get_mysql_connection()
    if not conn:
        print("Database connection failed.")
        return

    cur = conn.cursor()
    # Prompt until valid numeric > 0
    while True:
        user_input = input("Enter Company ID (>0): ").strip()
        try:
            company_id = int(user_input)
            if company_id > 0:
                break
            else:
                print("Company ID must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a numeric Company ID.")

    try:
        cur.execute("SELECT companyName FROM company WHERE companyID = %s", (company_id,))
        company = cur.fetchone()

        if not company:
            print(f"Company with ID {company_id} doesn't exist")
            return

        company_name = company[0]
        print(f"\nCompany Found: {company_name}\n")

        # Query attendees who registered for sessions (matches your provided SQL structure)
        query = """
            SELECT DISTINCT 
                a.attendeeName, 
                a.attendeeDOB, 
                s.sessionTitle, 
                sp.speakerName, 
                s.sessionDate, 
                ro.roomName
            FROM attendee a
            INNER JOIN registration r 
                ON a.attendeeID = r.attendeeID
            INNER JOIN session s 
                ON r.sessionID = s.sessionID
            LEFT JOIN speaker sp ON s.speakerID = sp.speakerID
            LEFT JOIN room ro ON s.roomID = ro.roomID
            WHERE a.attendeeCompanyID = %s
            ORDER BY a.attendeeName
        """
        cur.execute(query, (company_id,))
        rows = cur.fetchall()

        if rows:
            print(f"{company_name} Attendees:\n")
            for row in rows:
                # row: attendeeName, attendeeDOB, sessionTitle, speakerName, sessionDate, roomName
                name, dob, session_title, speaker_name, session_date, room_name = row
                dob_str = dob.strftime("%Y-%m-%d") if isinstance(dob, datetime.date) else str(dob)
                session_date_str = session_date.strftime("%Y-%m-%d") if isinstance(session_date, datetime.date) else str(session_date)
                print(f"Name: {name}")
                print(f"Date of Birth: {dob_str}")
                print(f"Session Title: {session_title}")
                print(f"Speaker: {speaker_name or 'N/A'}")
                print(f"Session Date: {session_date_str or 'N/A'}")
                print(f"Room: {room_name or 'N/A'}")
                print("---")
        else:
            print(f"No attendees found for {company_name}")
    except Exception as e:
        print(f"Error querying MySQL: {e}")
    finally:
        cur.close()
        close_mysql_connection(conn)


def add_new_attendee():
    conn = get_mysql_connection()
    if not conn:
        print("Database connection failed.")
        return

    cur = conn.cursor()
    try:
        # Collect input
        new_user_id_input = input("Insert new user ID (leave blank to auto-generate): ").strip()
        if new_user_id_input == "":
            new_user_id = None
        else:
            try:
                new_user_id = int(new_user_id_input)
                if new_user_id <= 0:
                    print("ID must be > 0")
                    return
            except ValueError:
                print("Invalid ID")
                return

        new_user_name = input("Insert new user Name: ").strip()
        new_user_dob = input("Insert DOB (YYYY-MM-DD): ").strip()
        new_user_gender = input("Insert Gender (Male/Female/Other): ").strip()
        new_user_company_input = input("Insert Company ID: ").strip()
        try:
            new_user_company = int(new_user_company_input)
        except ValueError:
            print("Invalid Company ID")
            return

        # Validate date
        try:
            dob_obj = datetime.datetime.strptime(new_user_dob, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format")
            return

        # Optional: check company exists
        cur.execute("SELECT companyName FROM company WHERE companyID = %s", (new_user_company,))
        if not cur.fetchone():
            print("Company ID does not exist.")
            return

        # Build insert
        if new_user_id is None:
            insert_sql = """
                INSERT INTO attendee (attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
                VALUES (%s, %s, %s, %s)
            """
            params = (new_user_name, dob_obj, new_user_gender, new_user_company)
        else:
            insert_sql = """
                INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (new_user_id, new_user_name, dob_obj, new_user_gender, new_user_company)

        cur.execute(insert_sql, params)
        conn.commit()
        print("Attendee added")
    except Exception as e:
        conn.rollback()
        print(f"Error adding attendee: {e}")
    finally:
        cur.close()
        close_mysql_connection(conn)


def view_connected_attendees():
    attendee = input("Enter Attendee ID: ").strip()
    try:
        attendee_id = int(attendee)
    except ValueError:
        print("*** ERROR *** Invalid attendee ID")
        return

    driver = get_neo4j_driver()
    if not driver:
        print("Neo4j connection failed.")
        return

    # Use default database name if your Neo4j DB uses a different name change below
    # For Neo4j 5.x the database name is often "neo4j" unless you created a custom DB
    database_name = "neo4j"

    with driver.session(database=database_name) as session:
        # Check attendee exists
        result = session.run(
            "MATCH (a:Attendee {AttendeeID: $id}) RETURN a.AttendeeID AS id, a.AttendeeName AS name",
            id=attendee_id
        )
        record = result.single()
        if not record:
            print("*** ERROR *** Attendee does not exist")
            return

        print(f"Attendee ID: {record['id']} | Name: {record.get('name', 'N/A')}")
        print("------------------------------")

        # Get connections
        query = """
            MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
            RETURN b.AttendeeID AS id, b.AttendeeName AS name
            ORDER BY b.AttendeeID
        """
        results = session.run(query, id=attendee_id)
        connections = list(results)

        if not connections:
            print("No connections")
        else:
            for r in connections:
                print(f"-> Attendee {r['id']} | Name: {r.get('name', 'N/A')}")

    # close driver only if you plan to exit app; otherwise keep open for reuse
    # close_neo4j_driver()


def add_attendee_connection():
    print("\n[Option 5] Add Attendee Connection\n")
    try:
        a1 = int(input("Enter Attendee ID 1: ").strip())
        a2 = int(input("Enter Attendee ID 2: ").strip())
    except ValueError:
        print("Invalid IDs")
        return

    driver = get_neo4j_driver()
    if not driver:
        print("Neo4j connection failed.")
        return

    database_name = "neo4j"
    with driver.session(database=database_name) as session:
        # Create bidirectional CONNECTED_TO relationship (single undirected relationship)
        query = """
            MATCH (a:Attendee {AttendeeID: $a1}), (b:Attendee {AttendeeID: $a2})
            MERGE (a)-[r:CONNECTED_TO]-(b)
            RETURN a.AttendeeID AS a, b.AttendeeID AS b
        """
        res = session.run(query, a1=a1, a2=a2)
        rec = res.single()
        if rec:
            print(f"Connected attendee {rec['a']} and {rec['b']}")
        else:
            print("One or both attendees not found in Neo4j.")


def view_rooms():
    conn = get_mysql_connection()
    if not conn:
        print("Database connection failed.")
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT roomID, roomName FROM room ORDER BY roomID")
        rows = cur.fetchall()
        if rows:
            print("\nRooms:")
            for rid, rname in rows:
                print(f"{rid} - {rname}")
        else:
            print("No rooms found.")
    except Exception as e:
        print(f"Error querying rooms: {e}")
    finally:
        cur.close()
        close_mysql_connection(conn)


def main_menu():
    while True:
        print("\nConference Management")
        print("----------------------")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("x - Exit application")

        choice = input("Choice: ").strip()

        if choice == "1":
            view_speakers_sessions()
        elif choice == "2":
            view_attendees_by_company()
        elif choice == "3":
            add_new_attendee()
        elif choice == "4":
            view_connected_attendees()
        elif choice == "5":
            add_attendee_connection()
        elif choice == "6":
            view_rooms()
        elif choice.lower() == "x":
            print("Exiting...")
            # close neo4j driver if open
            close_neo4j_driver()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()































































