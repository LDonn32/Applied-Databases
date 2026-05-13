# Just a test file that will check all SQL + Neo4j functions used by main.py.
# Using this for debugging and testing changes to the database functions without having to run the full main.py menu. 


# test_functions.py

from db import (
    view_speakers_sessions,        
    view_attendees_by_company,
    add_new_attendee,
    view_connected_attendees,
    add_attendee_connection,
    view_rooms
)

print("\n==============================")
print("TEST 1 — View Speakers & Sessions")
print("==============================")
try:
    view_speakers_sessions("dr")  
except Exception as e:
    print("ERROR in Option 1:", e)

print("\n==============================")
print("TEST 2 — View Attendees by Company")
print("==============================")
try:
    view_attendees_by_company(2)
    view_attendees_by_company(9)
except Exception as e:
    print("ERROR in Option 2:", e)

print("\n==============================")
print("TEST 3 — Add New Attendee")
print("==============================")
try:
    add_new_attendee(200, "Test User", "1990-01-01", "Male", 2)
except Exception as e:
    print("ERROR in Option 3:", e)

print("\n==============================")
print("TEST 4 — View Connected Attendees")
print("==============================")
try:
    view_connected_attendees(101)
    view_connected_attendees(112)
except Exception as e:
    print("ERROR in Option 4:", e)

print("\n==============================")
print("TEST 5 — Add Attendee Connection")
print("==============================")
try:
    add_attendee_connection(117, 118)
except Exception as e:
    print("ERROR in Option 5:", e)

print("\n==============================")
print("TEST 6 — View Rooms")
print("==============================")
try:
    view_rooms()
except Exception as e:
    print("ERROR in Option 6:", e)

print("\n==============================")
print("ALL TESTS COMPLETE")
print("==============================\n")
