from expense_manager import (
    add_expense,
    view_expenses,
    delete_expense,
    update_expense
)
while True:

    print("\n--- Expense Tracker ---")

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Update Expense")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        title = input("Enter title: ")
        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("Invalid amount")
            continue
        category = input("Enter category: ")

        date = input("Enter date: ")

        add_expense(title, amount, category, date)

    elif choice == "2":

        view_expenses()
    elif choice == "3":

        try:
            expense_id = int(input("Enter Expense ID to delete: "))
            delete_expense(expense_id)
        except ValueError:
            print("Invalid ID")    
    
    elif choice == "4":

        try:

            expense_id = int(input("Enter Expense ID to update: "))

            new_title = input("Enter new title: ")

            new_amount = float(input("Enter new amount: "))

            new_category = input("Enter new category: ")

            new_date = input("Enter new date: ")

            update_expense(
            expense_id,
            new_title,
            new_amount,
            new_category,
            new_date
            )

        except ValueError:

            print("Invalid input")
    elif choice == "5":

        print("Exiting...")
        break

    else:
        print("Invalid choice")