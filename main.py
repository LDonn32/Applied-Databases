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


if __name__ == "__main__":
    main_menu()
