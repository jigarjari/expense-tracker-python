from database import get_connection

def add_expense(title, amount, category, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses(title, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

    conn.commit()
    conn.close()

    print("Expense added successfully")

def view_expenses():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    conn.close()

    if len(expenses) == 0:
        print("\nNo expenses found.")
        return

    print("\n--- All Expenses ---")

    for expense in expenses:

        print(f"""
            ID: {expense[0]}
            Title: {expense[1]}
            Amount: ₹{expense[2]}
            Category: {expense[3]}
            Date: {expense[4]}
        -------------------------
        """)
        
def delete_expense(expense_id):

    conn = get_connection()

    cursor = conn.cursor()

    # Check if expense exists
    cursor.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    )

    expense = cursor.fetchone()

    if expense is None:

        print("Expense not found.")

        conn.close()

        return

    # Delete expense
    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    conn.close()

    print("Expense deleted successfully.")

def update_expense(expense_id, new_title, new_amount, new_category, new_date):

    conn = get_connection()

    cursor = conn.cursor()

    # Check if expense exists
    cursor.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    )

    expense = cursor.fetchone()

    if expense is None:

        print("Expense not found.")

        conn.close()

        return

    # Update expense
    cursor.execute("""
    UPDATE expenses
    SET title = ?,
        amount = ?,
        category = ?,
        date = ?
    WHERE id = ?
    """, (
        new_title,
        new_amount,
        new_category,
        new_date,
        expense_id
    ))

    conn.commit()

    conn.close()

    print("Expense updated successfully.")