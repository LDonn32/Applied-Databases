#! /usr/bin/env python3





# db_mysql.py
import mysql.connector

# This is the main application code for the conference management system.
from db_mysql import get_mysql_connection, close_mysql_connection


def view_speakers_and_sessions():
    print("\n[Option 1] View Speakers & Sessions\n")
    speaker_name = input("Enter Speaker Name (or part of it): ")

    conn = get_mysql_connection()
    if not conn:
        print("Database connection failed.")
        return

    cursor = conn.cursor()

    query = """
    SELECT s.speakerName, se.sessionTitle, r.roomName
    FROM session se
    JOIN speaker s ON se.speakerID = s.speakerID
    JOIN room r ON se.roomID = r.roomID
    WHERE s.speakerName LIKE %s
    """

    cursor.execute(query, ('%' + speaker_name + '%',))
    results = cursor.fetchall()

    if results:
        for row in results:
            print(f"Speaker: {row[0]}")
            print(f"Session Title: {row[1]}")
            print(f"Room: {row[2]}")
            print("---")
    else:
        print("No speakers found matching that name.")

    cursor.close()
    close_mysql_connection(conn)


def view_attendees_by_company():
    print("\n[Option 2] View Attendees by Company (by Company ID)\n")

    # 1. Get a valid numeric company ID > 0
    while True:
        company_id_input = input("Enter a valid Company ID (>0): ")

        if not company_id_input.isdigit():
            print("Invalid input. Company ID must be a number.")
            continue

        company_id = int(company_id_input)

        if company_id <= 0:
            print("Invalid Company ID. Must be greater than 0.")
            continue

        break

    conn = get_mysql_connection()
    if not conn:
        print("Database connection failed.")
        return

    cursor = conn.cursor()

    # 2. Check if company exists
    company_query = """
    SELECT companyName
    FROM company
    WHERE companyID = %s
    """
    cursor.execute(company_query, (company_id,))
    company_result = cursor.fetchone()

    if not company_result:
        print("\nValid Company ID entered, but no such company exists.")
        cursor.close()
        close_mysql_connection(conn)
        return

    company_name = company_result[0]
    print(f"\nCompany Found: {company_name}\n")

    # 3. Get attendees + session details
    attendee_query = """
    SELECT 
        a.attendeeName,
        a.dateOfBirth,
        se.sessionTitle,
        sp.speakerName,
        r.roomName
    FROM attendee a
    LEFT JOIN attendee_session asj ON a.attendeeID = asj.attendeeID
    LEFT JOIN session se ON asj.sessionID = se.sessionID
    LEFT JOIN speaker sp ON se.speakerID = sp.speakerID
    LEFT JOIN room r ON se.roomID = r.roomID
    WHERE a.companyID = %s
    ORDER BY a.attendeeName
    """

    cursor.execute(attendee_query, (company_id,))
    attendees = cursor.fetchall()

    # 4. Handle company with no attendees
    if not attendees:
        print("This company exists, but has no attendees for any sessions.")
        cursor.close()
        close_mysql_connection(conn)
        return

    # 5. Display results
    print("Attendees from this company:\n")

    for row in attendees:
        attendee_name = row[0]
        dob = row[1]
        session_title = row[2] if row[2] else "No session attended"
        speaker_name = row[3] if row[3] else "N/A"
        room_name = row[4] if row[4] else "N/A"

        print(f"Attendee Name: {attendee_name}")
        print(f"Date of Birth: {dob}")
        print(f"Session Title: {session_title}")
        print(f"Speaker: {speaker_name}")
        print(f"Room: {room_name}")
        print("---")

    cursor.close()
    close_mysql_connection(conn)


def main_menu():
    while True:
        print("\nConference Management")
        print("----------------------")
        print("\nMENU")
        print("====")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("x - Exit application")

        choice = input("Choice: ")

        if choice == "1":
            view_speakers_and_sessions()
        elif choice == "2":
            view_attendees_by_company()
        elif choice == "3":
            print("\n[Option 3 selected] Add New Attendee (to be implemented)\n")
        elif choice == "4":
            print("\n[Option 4 selected] View Connected Attendees (to be implemented)\n")
        elif choice == "5":
            print("\n[Option 5 selected] Add Attendee Connection (to be implemented)\n")
        elif choice == "6":
            print("\n[Option 6 selected] View Rooms (to be implemented)\n")
        elif choice.lower() == "x":
            print("\nExiting application...")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()


















































