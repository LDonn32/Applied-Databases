#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error

def get_mysql_connection():
    """
    Establishes a connection to the MySQL database.
    Returns a connection object or None if connection fails.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",
            database="conference_management"
        )
        print("MySQL connection successful.")
        return conn
    except Error as err:
        if err.errno == 2003:
            print(f"MySQL error: Cannot connect to MySQL server (check if server is running)")
        elif err.errno == 1045:
            print(f"MySQL error: Access denied (check user/password)")
        elif err.errno == 1049:
            print(f"MySQL error: Unknown database")
        else:
            print(f"MySQL error: {err}")
        return None


def close_mysql_connection(conn):
    """Closes a MySQL database connection."""
    if conn and conn.is_connected():
        conn.close()
        print("MySQL connection closed.")
