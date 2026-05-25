import sqlite3

def add_expense(title, amount, category, date):

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses(title, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

    conn.commit()
    conn.close()

    print("Expense added successfully")