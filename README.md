# Applied-Databases

A conference management system integrating both MySQL and Neo4j databases.

## Project Overview

This project for applied databases demonstrates the implementation of a conference management system with dual database support:
- **MySQL**: Relational database for structured data such as speakers, sessions, attendees, companies
- **Neo4j**: Graph database for relationship-based queries such as connected attendees, networks



## Prepare the databases

__MySQL__

Import the provided SQL:

Install "pymysql":

Run in your terminal:

python -m pip install pymysql to connect to MYSQL with python.


__Neo4j__

Activate Neo4j in the virtual machine.

Open Folder-> C:\Users\appDB\Documents\neo4j-community-5.26.19\conf 
OPen file -> neo4j.conf 
Make sure dbms.default_database=appdbprojNeo4j 
After that go to -> C:\Users\appDB\Documents\neo4j-community-5.26.19\bin -> cmd 
Once the commander is open run -> neo4j.bat console 
Open http://localhost:7474/ and run the query given on: appdbprojNeo4j to make sure you have the connections.

To upload the json data input the below into cmd from 

```
cmd
cypher-shell,bat -u neo4j -p neo4jneo4j -f appdbprojNeo4j.json
```

Run the application
From the project root 

```
cmd
python main.py
```

Follow the menu prompts when running in command terminal.

__Menu options__

View Speakers & Sessions — search by speaker name fragment.

View Attendees by Company — enter a numeric company ID (>0).

Add New Attendee — prompts for ID, name, DOB (YYYY-MM-DD), gender, company ID.

View Connected Attendees — shows Neo4j connections for an attendee ID.

Add Attendee Connection — creates CONNECTED_TO relationships in Neo4j (validates MySQL existence).

View Rooms — cached on first call; restart app to refresh.
x. Exit — terminates the program.



## Additional testing utility
`test_functions.py` is a helper script that exercises the same `db.py` functions used by `main.py` directly. It is used for testing and debugging database behavior without having to navigate the interactive menu options.

This is expanded on in the innvation.doc

Testing checklist
Option 6 (View Rooms) should list rooms and capacities.

Option 1 (View Speakers & Sessions) should return speaker/session/room rows.

Option 2 (View Attendees by Company) should return attendee/session rows or "No attendees found".

Option 3 (Add New Attendee) should insert a row into MySQL and show success.

Option 4 (View Connected Attendees) should list connected attendees or "No connections".

Option 5 (Add Attendee Connection) should create nodes/relationships in Neo4j and report success.


## Troubleshooting (common issues)
Connection refused / WinError 10061: Neo4j not running or Bolt port incorrect. Start Neo4j Desktop and confirm Bolt port (default 7687).

cryptography runtime errors: install cryptography via pip

Empty results: verify the correct database and that the sample data was imported.



## References

- [Neo4j Documentation](https://neo4j.com/blog/cypher-and-gql/cypher-load-json-from-url/)



## Virtual Environment 

python 3.11.14 - windows x86_64-none














