# db_mysql.py
import pymysql
from pymysql.err import OperationalError, InternalError, ProgrammingError

# Edit these to match your local MySQL credentials and database name
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",   # <-- change this
    "database": "appdbproj",             # <-- change to your DB name if different
    "port": 3306,
    "cursorclass": pymysql.cursors.Cursor,
    "autocommit": False
}


def get_mysql_connection():
    """
    Return a pymysql connection or None on failure.
    """
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        return conn
    except OperationalError as e:
        print(f"MySQL OperationalError: {e}")
    except InternalError as e:
        print(f"MySQL InternalError: {e}")
    except Exception as e:
        print(f"MySQL connection error: {e}")
    return None


def close_mysql_connection(conn):
    """
    Close the connection if open.
    """
    try:
        if conn:
            conn.close()
    except Exception:
        pass






















