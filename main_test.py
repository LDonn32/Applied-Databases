#! /usr/bin/env python3

# This is a placeholder for the main application code. 
# The main_menu function will be implemented here to provide a user interface 
# for the conference management system.


# Connect to the database using the db_mysql module


####

# db_mysql.py
import mysql.connector

####

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",
            database="appdbproj"
        )
        print("MySQL connection successful.")
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        return None


#################################################

# Goal is to create a menu for the CMS first. 
# Then will add extra functionality to the menu options.


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
            print("\n[Option 1 selected] View Speakers & Sessions\n")
            speaker_name = input("Enter Speaker Name: ")
            conn = get_mysql_connection()
            if conn:
                cursor = conn.cursor()
                query = """
                SELECT s.speakerName, s.sessionTitle, r.roomName
                FROM session s
                JOIN room r ON s.roomID = r.roomID
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
                conn.close()
            else:
                print("Database connection failed.")
        elif choice == "2":
            print("\n[Option 2 selected] View Attendees by Company\n")
        elif choice == "3":
            print("\n[Option 3 selected] Add New Attendee\n")
        elif choice == "4":
            print("\n[Option 4 selected] View Connected Attendees\n")
        elif choice == "5":
            print("\n[Option 5 selected] Add Attendee Connection\n")
        elif choice == "6":
            print("\n[Option 6 selected] View Rooms\n")
        elif choice.lower() == "x":
            print("\nExiting application...")
            break
        else:
            print("\nInvalid choice. Please try again.")



elif choice == "2":
    print("\n[Option 2 selected] View Attendees by Company\n")

    while True:
        company_id_input = input("Enter a valid Company ID (>0): ")

        # 1. Check numeric
        if not company_id_input.isdigit():
            print("Invalid input. Company ID must be a number.")
            continue

        company_id = int(company_id_input)

        # 2. Check > 0
        if company_id <= 0:
            print("Invalid Company ID. Must be greater than 0.")
            continue

        # If we reach here → numeric and > 0
        break

    conn = get_mysql_connection()
    if conn:
        cursor = conn.cursor()

        # 3. Check if company exists
        company_query = """
        SELECT companyName
        FROM company
        WHERE companyID = %s
        """

        cursor.execute(company_query, (company_id,))
        company_result = cursor.fetchone()

        if not company_result:
            print("\nCompany ID exists as a number, but no such company was found.")
            cursor.close()
            conn.close()
            return

        company_name = company_result[0]
        print(f"\nCompany Found: {company_name}\n")

        # 4. Get attendees + session details
        attendee_query = """
        SELECT 
            a.attendeeName,
            a.dateOfBirth,
            s.sessionTitle,
            sp.speakerName,
            r.roomName
        FROM attendee a
        LEFT JOIN attendee_session asj ON a.attendeeID = asj.attendeeID
        LEFT JOIN session s ON asj.sessionID = s.sessionID
        LEFT JOIN speaker sp ON s.speakerID = sp.speakerID
        LEFT JOIN room r ON s.roomID = r.roomID
        WHERE a.companyID = %s
        ORDER BY a.attendeeName
        """

        cursor.execute(attendee_query, (company_id,))
        attendees = cursor.fetchall()

        if not attendees:
            print("This company exists, but has no attendees for any sessions.")
            cursor.close()
            conn.close()
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
        conn.close()

    else:
        print("Database connection failed.")







    if __name__ == "__main__":
        main_menu()
###################################################################