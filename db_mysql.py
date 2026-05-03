# imports and config

import mysql.connector
from mysql.connector import Error
from config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
)

# MySQL CONNECTION 

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )
        return conn
    except Error as e:
        print(f"[MySQL] Connection error: {e}")
        return None



# GENERIC SELECT 

def fetch_all(query, params=None):
    conn = get_mysql_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"[MySQL] Query error: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# GENERIC INSERT/UPDATE/DELETE 

def execute_query(query, params=None):
    conn = get_mysql_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Error as e:
        print(f"[MySQL] Query error: {e}")
        conn.rollback()
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



# OPTION 1 —  View Speakers & Sessions

def get_speakers_and_sessions(search_term):
    query = """
        SELECT 
            speaker.speakerName,
            session.sessionTitle,
            room.roomName
        FROM speaker
        JOIN session ON speaker.speakerID = session.sessionSpeakerID
        JOIN room ON session.sessionRoomID = room.roomID
        WHERE speaker.speakerName LIKE %s;
    """
    return fetch_all(query, (f"%{search_term}%",))



# OPTION 2 — Attendees by Company

def get_attendees_by_company(company_id):
    query = """
        SELECT
            company.companyName,
            attendee.attendeeName,
            attendee.attendeeDOB,
            session.sessionTitle,
            speaker.speakerName,
            session.sessionDate,
            room.roomName
        FROM company
        LEFT JOIN attendee ON attendee.attendeeCompanyID = company.companyID
        LEFT JOIN attendee_session ON attendee_session.attendeeID = attendee.attendeeID
        LEFT JOIN session ON session.sessionID = attendee_session.sessionID
        LEFT JOIN speaker ON speaker.speakerID = session.sessionSpeakerID
        LEFT JOIN room ON room.roomID = session.sessionRoomID
        WHERE company.companyID = %s;
    """
    return fetch_all(query, (company_id,))


def company_exists(company_id):
    query = "SELECT companyName FROM company WHERE companyID = %s;"
    rows = fetch_all(query, (company_id,))
    return rows[0]["companyName"] if rows else None



# OPTION 3 — Add New Attendee

def attendee_exists(attendee_id):
    query = "SELECT attendeeID FROM attendee WHERE attendeeID = %s;"
    rows = fetch_all(query, (attendee_id,))
    return len(rows) > 0


def insert_attendee(attendee_id, name, dob, gender, company_id):
    query = """
        INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
        VALUES (%s, %s, %s, %s, %s);
    """
    return execute_query(query, (attendee_id, name, dob, gender, company_id))


# OPTION 4 — View Connected Attendees (The MySQL part)

def get_attendee_name(attendee_id):
    query = "SELECT attendeeName FROM attendee WHERE attendeeID = %s;"
    rows = fetch_all(query, (attendee_id,))
    return rows[0]["attendeeName"] if rows else None



# OPTION 6 - View Rooms


def get_all_rooms():
    query = "SELECT roomID, roomName, roomCapacity FROM room ORDER BY roomID;"
    return fetch_all(query)
