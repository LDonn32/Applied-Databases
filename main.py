
# IMPORTS

from db_mysql import (
    get_speakers_and_sessions,
    get_attendees_by_company,
    company_exists,
    attendee_exists,
    insert_attendee,
    get_attendee_name,
    get_connected_attendees,
    get_all_rooms

)

from db_neo4j import (
    get_connected_attendees,
    neo4j_attendee_exists,
    create_neo4j_attendee,
    attendees_already_connected,
    create_connection
)


# OPTION 1 — View Speakers & Sessions

def view_speakers_and_sessions():
    print("\nView Speakers & Sessions")
    search = input("Enter speaker name : ").strip()

    print(f"\nSession Details For : {search}")

    rows = get_speakers_and_sessions(search)

    if not rows:
        print("No speakers found of that name")
        return

    for row in rows:
        print(row["speakerName"])
        print(row["sessionTitle"])
        print(row["roomName"])
        print()



# OPTION 2 — View Attendees by Company

def view_attendees_by_company():
    print("\nView Attendees by Company")

    while True:
        company_input = input("Enter Company ID : ").strip()

        # Must be numeric
        if not company_input.isdigit():
            print("Enter Company ID : ", end="")
            continue

        company_id = int(company_input)

        # Must be > 0
        if company_id <= 0:
            print("Enter Company ID : ", end="")
            continue

        # Check if company exists
        company_name = company_exists(company_id)
        if not company_name:
            print(f"Company with ID {company_id} doesn't exist")
            return

        # Fetch attendees
        rows = get_attendees_by_company(company_id)

        print(f"\n{company_name} Attendees")

        # Check if company has NO attendees
        has_attendees = any(row["attendeeName"] is not None for row in rows)

        if not has_attendees:
            print(f"No attendees found for {company_name}")
            return

        # Print results
        for row in rows:
            if row["attendeeName"] is None:
                continue

            print(
                f"{row['attendeeName']} | {row['attendeeDOB']} | "
                f"{row['sessionTitle']} | {row['speakerName']} | "
                f"{row['sessionDate']} | {row['roomName']}"
            )

        return


# OPTION 3 — Add New Attendee

def add_new_attendee():
    print("\nAdd New Attendee")

    # Attendee ID
    attendee_id_input = input("Attendee ID : ").strip()

    if not attendee_id_input.isdigit():
        print("*** ERROR *** Invalid Attendee ID")
        return

    attendee_id = int(attendee_id_input)

    if attendee_exists(attendee_id):
        print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
        return

    # Name
    name = input("Name : ").strip()

    # DOB
    dob = input("DOB : ").strip()

    # Gender
    gender = input("Gender : ").strip()
    if gender not in ["Male", "Female"]:
        print("*** ERROR *** Gender must be Male/Female")
        return

    # Company ID
    company_input = input("Company ID : ").strip()
    if not company_input.isdigit():
        print("*** ERROR *** Invalid Company ID")
        return

    company_id = int(company_input)

    if not company_exists(company_id):
        print(f"*** ERROR *** Company ID: {company_id} does not exist")
        return

    # Insert attendee
    try:
        success = insert_attendee(attendee_id, name, dob, gender, company_id)
        if success:
            print("Attendee successfully added")
        else:
            print("*** ERROR *** Could not add attendee")
    except Exception as e:
        print(f"*** ERROR *** {e}")



# OPTION 4 — View Connected Attendees 

def view_connected_attendees():
    print("\nView Connected Attendees")

    while True:
        attendee_input = input("Enter Attendee ID : ").strip()

        # Error condition: non-numeric
        if not attendee_input.isdigit():
            print("*** ERROR *** Invalid attendee ID")
            continue

        attendee_id = int(attendee_input)

        # Check MySQL for attendee name
        attendee_name = get_attendee_name(attendee_id)

        # Get Neo4j connections (this could be empty but putting in for sanity check)
        connections = get_connected_attendees(attendee_id)

        # Error condition: not in MySQL AND not in Neo4j
        if not attendee_name and not connections:
            print("*** ERROR *** Attendee does not exist")
            continue

        # Print attendee name (from MySQL if available)
        print(f"\nAttendee Name: {attendee_name if attendee_name else 'Unknown'}")

        # Case - attendee exists in MySQL but has no Neo4j connections
        if not connections:
            print("No connections")
            return

        # Case - attendee has connections
        print("\nThese attendees are connected :")
        for c in connections:
            print(f"{c['attendeeID']} | {c['attendeeName']}")

        return



# OPTION 5 - Add Attendees connection

def add_attendee_connection():
    print("\nAdd Attendee Connection")

    while True:
        id1_input = input("Enter Attendee 1 ID : ").strip()
        id2_input = input("Enter Attendee 2 ID : ").strip()

        # Error: non-numeric
        if not id1_input.isdigit() or not id2_input.isdigit():
            print("*** ERROR *** Attendee IDs must be numbers")
            continue

        id1 = int(id1_input)
        id2 = int(id2_input)

        # Error - cannot connect to self
        if id1 == id2:
            print("*** ERROR *** An attendee cannot connect to him/herself")
            continue

        # Check MySQL existence
        name1 = get_attendee_name(id1)
        name2 = get_attendee_name(id2)

        if not name1 or not name2:
            print("*** ERROR *** One or both attendee IDs do not exist")
            continue

        # Ensure both nodes exist in Neo4j
        if not neo4j_attendee_exists(id1):
            create_neo4j_attendee(id1, name1)

        if not neo4j_attendee_exists(id2):
            create_neo4j_attendee(id2, name2)

        # Check if already connected
        if attendees_already_connected(id1, id2):
            print("*** ERROR *** These attendees are already connected")
            continue

        # Create connection
        create_connection(id1, id2)

        print(f"Attendee {id1} is now connected to Attendee {id2}")
        return


# OPTION 6 - View Rooms 

def view_rooms():
    print("\nView Rooms")

    rows = get_all_rooms()

    if not rows:
        print("No rooms found")
        return

    print("\nRoomID | RoomName | Capacity")
    for row in rows:
        print(f"{row['roomID']} | {row['roomName']} | {row['roomCapacity']}")


# MAIN MENU LOOP

def main():
    while True:
        print("\nConference Management")
        print("MENU")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("x - Exit application")

        choice = input("Choice: ").strip()

        if choice == "1":
            view_speakers_and_sessions()
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
            print("Goodbye")
            break
        else:
            print("Invalid choice")


# Name gaurd for main menu loop

if __name__ == "__main__":
    main()



















































