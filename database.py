import sqlite3

DB_NAME = "expenses.db"


def get_connection():

    return sqlite3.connect(DB_NAME)


def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        amount REAL,
        category TEXT,
        date TEXT
    )
    """)

    conn.commit()

    conn.close()


create_table()