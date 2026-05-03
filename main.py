
# Main entry point for the Conference Management application.
# Displays the menu and delegates actions to db.py functions.


import db

def main_menu():
    print("\nConference Management")
    print("------------------------")
    print("\nMENU")
    print("====")
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by company")
    print("3 - Add New Attendee")
    print("4 - View Connected Attendees")
    print("5 - Add Attendee Connection")
    print("6 - View Rooms")
    print("x - Exit Application")
    return input("Choice: ").strip()

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "1":
            db.view_speakers_sessions()
        elif choice == "2":
            db.view_attendees_by_company()
        elif choice == "3":
            db.add_new_attendee()
        elif choice == "4":
            db.view_connected_attendees()
        elif choice == "5":
            db.add_attendee_connection()
        elif choice == "6":
            db.view_rooms()
        elif choice.lower() == "x":
            print("Logging out...")
            break
        else:
            print("This is an invalid option, please try again.")











































































