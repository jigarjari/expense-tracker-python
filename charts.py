import pandas as pd
import matplotlib.pyplot as plt

from database import get_connection


def show_category_chart():

    conn = get_connection()

    query = "SELECT category, amount FROM expenses"

    df = pd.read_sql_query(query, conn)

    conn.close()

    if df.empty:

        print("No expense data found.")

        return

    category_total = df.groupby("category")["amount"].sum()

    plt.figure(figsize=(7, 7))

    plt.pie(
        category_total,
        labels=category_total.index,
        autopct="%1.1f%%"
    )

    plt.title("Expense Distribution by Category")

    plt.show()
def save_category_chart():

    conn = get_connection()

    query = "SELECT category, amount FROM expenses"

    df = pd.read_sql_query(query, conn)

    conn.close()

    if df.empty:
        return None

    category_total = df.groupby("category")["amount"].sum()

    chart_path = "reports/category_chart.png"

    plt.figure(figsize=(5, 5))

    plt.pie(
        category_total,
        labels=category_total.index,
        autopct="%1.1f%%"
    )

    plt.title("Expense Distribution")

    plt.savefig(chart_path)

    plt.close()

    return chart_path