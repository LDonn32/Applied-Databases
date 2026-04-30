# db_mysql.py
import mysql.connector
from mysql.connector import Error

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",
            database="conference_management"
        )
        return conn
    except Error as err:
        print(f"MySQL error: {err}")
        return None

def close_mysql_connection(conn):
    if conn and conn.is_connected():
        conn.close()







