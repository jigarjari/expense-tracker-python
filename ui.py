import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
import os

from expense_manager import (
    add_expense,
    delete_expense,
    update_expense
)

from database import get_connection

from charts import show_category_chart

from reports import generate_pdf_report


# ---------------- FUNCTIONS ---------------- #

selected_expense_id = None


def clear_fields():

    title_entry.delete(0, "end")

    amount_entry.delete(0, "end")

    category_dropdown.set("Select Category")

    date_entry.set_date(date.today())


def load_expenses():

    for row in expense_table.get_children():

        expense_table.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM expenses"
    )

    expenses = cursor.fetchall()

    conn.close()

    for expense in expenses:

        expense_table.insert(
            "",
            "end",
            values=expense
        )


def save_expense():

    title = title_entry.get()

    amount = amount_entry.get()

    category = category_dropdown.get()

    selected_date = date_entry.get()

    if (
        title == "" or
        amount == "" or
        category == "Select Category"
    ):

        status_label.configure(
            text="All Fields Are Required",
            text_color="orange"
        )

        return

    try:

        amount = float(amount)

        add_expense(
            title,
            amount,
            category,
            selected_date
        )

        load_expenses()

        clear_fields()

        status_label.configure(
            text="Expense Added Successfully",
            text_color="green"
        )

        refresh_dashboard_cards()

    except ValueError:

        status_label.configure(
            text="Invalid Amount",
            text_color="red"
        )


def generate_pdf():

    pdf_path = generate_pdf_report()

    if pdf_path and os.path.exists(pdf_path):

        os.startfile(pdf_path)

        status_label.configure(
            text="PDF Generated Successfully",
            text_color="green"
        )

    else:

        status_label.configure(
            text="PDF Generation Failed",
            text_color="red"
        )


def select_expense(event):

    global selected_expense_id

    selected_item = expense_table.selection()

    if not selected_item:
        return

    values = expense_table.item(
        selected_item,
        "values"
    )

    selected_expense_id = values[0]

    title_entry.delete(0, "end")
    title_entry.insert(0, values[1])

    amount_entry.delete(0, "end")
    amount_entry.insert(0, values[2])

    category_dropdown.set(values[3])

    date_entry.set_date(values[4])


def delete_selected_expense():

    global selected_expense_id

    if selected_expense_id is None:

        status_label.configure(
            text="Select Expense First",
            text_color="orange"
        )

        return

    delete_expense(selected_expense_id)

    load_expenses()

    clear_fields()

    status_label.configure(
        text="Expense Deleted",
        text_color="green"
    )

    refresh_dashboard_cards()


def update_selected_expense():

    global selected_expense_id

    if selected_expense_id is None:

        status_label.configure(
            text="Select Expense First",
            text_color="orange"
        )

        return

    try:

        title = title_entry.get()

        amount = float(amount_entry.get())

        category = category_dropdown.get()

        selected_date = date_entry.get()

        update_expense(
            selected_expense_id,
            title,
            amount,
            category,
            selected_date
        )

        load_expenses()

        clear_fields()

        status_label.configure(
            text="Expense Updated",
            text_color="green"
        )

        refresh_dashboard_cards()

    except ValueError:

        status_label.configure(
            text="Invalid Amount",
            text_color="red"
        )


def filter_expenses():

    search_text = search_entry.get().lower()

    selected_category = category_filter.get()

    selected_date = date_filter.get()

    for row in expense_table.get_children():

        expense_table.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM expenses"
    )

    expenses = cursor.fetchall()

    conn.close()

    for expense in expenses:

        title = str(expense[1]).lower()

        category = str(expense[3])

        expense_date = str(expense[4])

        title_match = (
            search_text in title
        )

        category_match = (
            selected_category == "All"
            or category == selected_category
        )

        date_match = (
            selected_date == expense_date
        )

        if (
            title_match and
            category_match and
            date_match
        ):

            expense_table.insert(
                "",
                "end",
                values=expense
            )


def create_dashboard_cards():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    total_expense = cursor.fetchone()[0]

    if total_expense is None:
        total_expense = 0

    cursor.execute(
        "SELECT COUNT(*) FROM expenses"
    )

    total_records = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(DISTINCT category) FROM expenses"
    )

    total_categories = cursor.fetchone()[0]

    cursor.execute(
        "SELECT MAX(amount) FROM expenses"
    )

    highest_expense = cursor.fetchone()[0]

    if highest_expense is None:
        highest_expense = 0

    conn.close()

    return {
        "total": total_expense,
        "records": total_records,
        "categories": total_categories,
        "highest": highest_expense
    }


def refresh_dashboard_cards():

    data = create_dashboard_cards()

    total_value.configure(
        text=f"₹{data['total']}"
    )

    record_value.configure(
        text=f"{data['records']}"
    )

    category_value.configure(
        text=f"{data['categories']}"
    )

    highest_value.configure(
        text=f"₹{data['highest']}"
    )


# ---------------- APP SETTINGS ---------------- #

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")


# ---------------- MAIN WINDOW ---------------- #

app = ctk.CTk()

app.title("Expense Tracker")

app.geometry("1450x850")


# ---------------- GRID CONFIG ---------------- #

app.grid_columnconfigure(1, weight=1)

app.grid_rowconfigure(0, weight=1)


# ---------------- SIDEBAR ---------------- #

sidebar = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=0
)

sidebar.grid(
    row=0,
    column=0,
    sticky="ns"
)


sidebar_title = ctk.CTkLabel(
    sidebar,
    text="Dashboard",
    font=("Arial", 30, "bold")
)

sidebar_title.pack(pady=30)


view_button = ctk.CTkButton(
    sidebar,
    text="Refresh Expenses",
    width=180,
    command=load_expenses
)

view_button.pack(pady=10)


chart_button = ctk.CTkButton(
    sidebar,
    text="Show Charts",
    width=180,
    command=show_category_chart
)

chart_button.pack(pady=10)


pdf_button = ctk.CTkButton(
    sidebar,
    text="Generate PDF",
    width=180,
    command=generate_pdf
)

pdf_button.pack(pady=10)


# ---------------- MAIN FRAME ---------------- #

main_frame = ctk.CTkFrame(app)

main_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=20,
    pady=20
)


# ---------------- TITLE ---------------- #

title = ctk.CTkLabel(
    main_frame,
    text="Expense Tracker System",
    font=("Arial", 36, "bold")
)

title.pack(pady=20)


# ---------------- DASHBOARD CARDS ---------------- #

dashboard_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

dashboard_frame.pack(
    pady=15
)

card_data = create_dashboard_cards()


# TOTAL CARD

total_card = ctk.CTkFrame(
    dashboard_frame,
    width=220,
    height=120
)

total_card.pack(
    side="left",
    padx=15
)

total_label = ctk.CTkLabel(
    total_card,
    text="Total Expense",
    font=("Arial", 18, "bold")
)

total_label.pack(pady=10)

total_value = ctk.CTkLabel(
    total_card,
    text=f"₹{card_data['total']}",
    font=("Arial", 28, "bold")
)

total_value.pack(pady=10)


# RECORD CARD

record_card = ctk.CTkFrame(
    dashboard_frame,
    width=220,
    height=120
)

record_card.pack(
    side="left",
    padx=15
)

record_label = ctk.CTkLabel(
    record_card,
    text="Total Records",
    font=("Arial", 18, "bold")
)

record_label.pack(pady=10)

record_value = ctk.CTkLabel(
    record_card,
    text=f"{card_data['records']}",
    font=("Arial", 28, "bold")
)

record_value.pack(pady=10)


# CATEGORY CARD

category_card = ctk.CTkFrame(
    dashboard_frame,
    width=220,
    height=120
)

category_card.pack(
    side="left",
    padx=15
)

category_label = ctk.CTkLabel(
    category_card,
    text="Categories",
    font=("Arial", 18, "bold")
)

category_label.pack(pady=10)

category_value = ctk.CTkLabel(
    category_card,
    text=f"{card_data['categories']}",
    font=("Arial", 28, "bold")
)

category_value.pack(pady=10)


# HIGHEST CARD

highest_card = ctk.CTkFrame(
    dashboard_frame,
    width=220,
    height=120
)

highest_card.pack(
    side="left",
    padx=15
)

highest_label = ctk.CTkLabel(
    highest_card,
    text="Highest Expense",
    font=("Arial", 18, "bold")
)

highest_label.pack(pady=10)

highest_value = ctk.CTkLabel(
    highest_card,
    text=f"₹{card_data['highest']}",
    font=("Arial", 28, "bold")
)

highest_value.pack(pady=10)


# ---------------- FORM FRAME ---------------- #

form_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

form_frame.pack(
    pady=15
)

title_entry = ctk.CTkEntry(
    form_frame,
    placeholder_text="Enter Expense Title",
    width=420,
    height=42
)

title_entry.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

amount_entry = ctk.CTkEntry(
    form_frame,
    placeholder_text="Enter Amount",
    width=420,
    height=42
)

amount_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


categories = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Education",
    "Other"
]

category_dropdown = ctk.CTkComboBox(
    form_frame,
    values=categories,
    width=420,
    height=42
)

category_dropdown.set(
    "Select Category"
)

category_dropdown.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


date_entry = DateEntry(
    form_frame,
    width=40,
    background="#1f538d",
    foreground="white",
    borderwidth=2,
    date_pattern="yyyy-mm-dd",
    font=("Arial", 12)
)

date_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# ---------------- STATUS LABEL ---------------- #

status_label = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Arial", 15)
)

status_label.pack(pady=10)


# ---------------- BUTTON FRAME ---------------- #

button_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

button_frame.pack(
    pady=15
)

save_button = ctk.CTkButton(
    button_frame,
    text="Add Expense",
    command=save_expense,
    width=180,
    height=45
)

save_button.pack(
    side="left",
    padx=10
)

update_button = ctk.CTkButton(
    button_frame,
    text="Update Expense",
    command=update_selected_expense,
    width=180,
    height=45
)

update_button.pack(
    side="left",
    padx=10
)

delete_button = ctk.CTkButton(
    button_frame,
    text="Delete Expense",
    command=delete_selected_expense,
    width=180,
    height=45,
    fg_color="darkred",
    hover_color="#8B0000"
)

delete_button.pack(
    side="left",
    padx=10
)


# ---------------- FILTER FRAME ---------------- #

filter_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

filter_frame.pack(
    pady=15
)

search_entry = ctk.CTkEntry(
    filter_frame,
    placeholder_text="Search Title",
    width=260,
    height=40
)

search_entry.pack(
    side="left",
    padx=10
)

category_filter = ctk.CTkComboBox(
    filter_frame,
    values=["All"] + categories,
    width=180,
    height=40
)

category_filter.set("All")

category_filter.pack(
    side="left",
    padx=10
)

date_filter = DateEntry(
    filter_frame,
    width=18,
    background="#1f538d",
    foreground="white",
    date_pattern="yyyy-mm-dd"
)

date_filter.pack(
    side="left",
    padx=10
)

filter_button = ctk.CTkButton(
    filter_frame,
    text="Apply Filter",
    command=filter_expenses,
    width=140,
    height=40
)

filter_button.pack(
    side="left",
    padx=10
)

reset_button = ctk.CTkButton(
    filter_frame,
    text="Reset",
    command=load_expenses,
    width=120,
    height=40
)

reset_button.pack(
    side="left",
    padx=10
)


# ---------------- TABLE FRAME ---------------- #

table_frame = ctk.CTkFrame(
    main_frame
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# ---------------- TREEVIEW STYLE ---------------- #

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="#2b2b2b",
    foreground="white",
    rowheight=35,
    fieldbackground="#2b2b2b",
    borderwidth=0,
    font=("Arial", 12)
)

style.configure(
    "Treeview.Heading",
    background="#1f538d",
    foreground="white",
    font=("Arial", 13, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#347083")]
)


# ---------------- TABLE ---------------- #

columns = (
    "ID",
    "Title",
    "Amount",
    "Category",
    "Date"
)

expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=15
)

expense_table.heading("ID", text="ID")
expense_table.heading("Title", text="Title")
expense_table.heading("Amount", text="Amount")
expense_table.heading("Category", text="Category")
expense_table.heading("Date", text="Date")

expense_table.column(
    "ID",
    width=80,
    anchor="center"
)

expense_table.column(
    "Title",
    width=420,
    anchor="center"
)

expense_table.column(
    "Amount",
    width=180,
    anchor="center"
)

expense_table.column(
    "Category",
    width=220,
    anchor="center"
)

expense_table.column(
    "Date",
    width=220,
    anchor="center"
)


# ---------------- SCROLLBAR ---------------- #

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=expense_table.yview
)

expense_table.configure(
    yscrollcommand=scrollbar.set
)

expense_table.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ---------------- TABLE EVENT ---------------- #

expense_table.bind(
    "<<TreeviewSelect>>",
    select_expense
)


# ---------------- LOAD DATA ---------------- #

load_expenses()


# ---------------- RUN APP ---------------- #

app.mainloop()