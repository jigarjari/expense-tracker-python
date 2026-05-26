import pandas as pd

from database import get_connection


def load_expenses():

    conn = get_connection()

    query = "SELECT * FROM expenses"

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def show_total_expense():

    df = load_expenses()

    if df.empty:

        print("No expense data found.")

        return

    total = df["amount"].sum()

    print(f"\nTotal Expense: ₹{total}")


def show_category_expense():

    df = load_expenses()

    if df.empty:

        print("No expense data found.")

        return

    category_total = df.groupby("category")["amount"].sum()

    print("\nCategory-wise Expenses:\n")

    print(category_total)


def show_highest_expense():

    df = load_expenses()

    if df.empty:

        print("No expense data found.")

        return

    highest = df.loc[df["amount"].idxmax()]

    print("\nHighest Expense:\n")

    print(highest)