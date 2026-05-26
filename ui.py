import customtkinter as ctk
from tkinter import ttk
from expense_manager import add_expense, view_expenses
from database import get_connection
from charts import show_category_chart
from reports import generate_pdf_report
import os

def save_expense():

    title = title_entry.get()

    amount = amount_entry.get()

    category = category_entry.get()

    date = date_entry.get()

    if (
        title == "" or
        amount == "" or
        category == "" or
        date == ""
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
            date
        )

        status_label.configure(
            text="Expense Added Successfully",
            text_color="green"
        )

        title_entry.delete(0, "end")

        amount_entry.delete(0, "end")

        category_entry.delete(0, "end")

        date_entry.delete(0, "end")

    except ValueError:

        status_label.configure(
            text="Invalid Amount",
            text_color="red"
        )
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
def generate_pdf():

    pdf_path = generate_pdf_report()

    if os.path.exists(pdf_path):

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
# ---------------- APP SETTINGS ---------------- #

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")


# ---------------- MAIN WINDOW ---------------- #

app = ctk.CTk()

app.title("Expense Tracker")

app.geometry("1000x600")


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
    font=("Arial", 28, "bold")
)

sidebar_title.pack(pady=30)


view_button = ctk.CTkButton(
    sidebar,
    text="View Expenses",
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
    command=lambda: generate_pdf()
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
    font=("Arial", 32, "bold")
)

title.pack(pady=20)


# ---------------- INPUT FIELDS ---------------- #

title_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Enter Expense Title",
    width=350,
    height=40
)

title_entry.pack(pady=10)


amount_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Enter Amount",
    width=350,
    height=40
)

amount_entry.pack(pady=10)


category_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Enter Category",
    width=350,
    height=40
)

category_entry.pack(pady=10)


date_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Enter Date (YYYY-MM-DD)",
    width=350,
    height=40
)

date_entry.pack(pady=10)


# ---------------- STATUS LABEL ---------------- #

status_label = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Arial", 16)
)

status_label.pack(pady=10)

# ---------------- SAVE BUTTON ---------------- #

save_button = ctk.CTkButton(
    main_frame,
    text="Add Expense",
    command=save_expense,
    width=250,
    height=45,
    font=("Arial", 18, "bold")
)

save_button.pack(pady=20)

table_frame = ctk.CTkFrame(
    main_frame
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

columns = (
    "ID",
    "Title",
    "Amount",
    "Category",
    "Date"
)

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="#2b2b2b",
    foreground="white",
    rowheight=30,
    fieldbackground="#2b2b2b",
    bordercolor="#343638",
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
    height=8
)

expense_table.heading("ID", text="ID")
expense_table.heading("Title", text="Title")
expense_table.heading("Amount", text="Amount")
expense_table.heading("Category", text="Category")
expense_table.heading("Date", text="Date")

expense_table.column("ID", width=60, anchor="center")
expense_table.column("Title", width=220, anchor="center")
expense_table.column("Amount", width=120, anchor="center")
expense_table.column("Category", width=160, anchor="center")
expense_table.column("Date", width=160, anchor="center")

expense_table.pack(
    fill="both",
    expand=True
)

# ---------------- RUN APP ---------------- #

app.mainloop()