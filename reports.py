import os
import pandas as pd

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from database import get_connection

from charts import save_category_chart


def generate_pdf_report():

    conn = get_connection()

    query = "SELECT * FROM expenses"

    df = pd.read_sql_query(query, conn)

    conn.close()

    if df.empty:

        return None

    pdf_path = os.path.join(
        "reports",
        "expense_report.pdf"
    )

    pdf = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    # ---------------- TITLE ---------------- #

    title = Paragraph(
        "Expense Tracker Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # ---------------- DATE ---------------- #

    current_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    date_text = Paragraph(
        f"Generated On: {current_date}",
        styles['BodyText']
    )

    elements.append(date_text)

    elements.append(Spacer(1, 20))

    # ---------------- TOTAL ---------------- #

    total_expense = df["amount"].sum()

    total = Paragraph(
        f"<b>Total Expense:</b> ₹{total_expense}",
        styles['Heading2']
    )

    elements.append(total)

    elements.append(Spacer(1, 20))

    # ---------------- TABLE ---------------- #

    table_data = [
        ["ID", "Title", "Amount", "Category", "Date"]
    ]

    for _, row in df.iterrows():

        table_data.append([
            row["id"],
            row["title"],
            row["amount"],
            row["category"],
            row["date"]
        ])

    expense_table = Table(table_data)

    expense_table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('GRID', (0, 0), (-1, -1), 1, colors.black)

    ]))

    elements.append(expense_table)

    elements.append(Spacer(1, 30))

    # ---------------- CHART ---------------- #

    chart_path = save_category_chart()

    if chart_path:

        chart = Image(
            chart_path,
            width=300,
            height=300
        )

        elements.append(chart)

    # ---------------- BUILD PDF ---------------- #

    pdf.build(elements)

    return pdf_path