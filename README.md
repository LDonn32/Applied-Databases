# Applied-Databases

A conference management system integrating both MySQL and Neo4j databases.

## Project Overview

This project for applied databases demonstrates the implementation of a conference management system with dual database support:
- **MySQL**: Relational database for structured data such as speakers, sessions, attendees, companies
- **Neo4j**: Graph database for relationship-based queries such as connected attendees, networks

## Folder structure 

```
Applied-Databases/
├── main.py                      # Main application entry point
├── main_test.py                 # Test file with CLI menu
├── db_mysql.py                  # MySQL database connection module
├── db_neo4j.py                  # Neo4j database connection module
├── appdbproj.sql.txt            # MySQL database schema and setup statements
├── appdbprojNeo4j.cypher        # Neo4j Cypher queries for initial data load
└── README.md                    
```

## Database Setup

### MySQL
- File: `appdbproj.sql.txt`
- Contains: Database schema, table definitions, and initial data
- Update credentials in `db_mysql.py` before connecting

### Neo4j
- File: `appdbprojNeo4j.cypher`
- Contains: Cypher queries to create attendee nodes and connections
- Run queries in Neo4j database console after setup

## Features ..... so far 


- View speakers and sessions
- View attendees by company
- Add new attendees
- View connected attendees (graph relationships)
- Add attendee connections
- View available rooms
- Interactive CLI menu

# To do ...

1. View speakers and sessions and make sure detailed query is possible.. so for each speaker show:
Speaker name
Title of session they are giving
Name of the room session is in 
Return to main menue

2. 

3. 

4. 

5

## Getting Started

### Prerequisites
- Python 3.11+
- MySQL Server
- Neo4j Server

### Installation

1. Install required Python packages:
```bash
pip install mysql-connector-python neo4j
```

2. Set up MySQL database using `appdbproj.sql.txt`

3. Set up Neo4j database using `appdbprojNeo4j.cypher`

4. Update database credentials in `db_mysql.py` and `db_neo4j.py`

### Running the Application

```bash
python main_test.py
```

This launches the conference management system menu.

## References

- [Neo4j Documentation](https://neo4j.com/blog/cypher-and-gql/cypher-load-json-from-url/)


Virtual Environment - python 3.11.14 - windows x86_64-none














