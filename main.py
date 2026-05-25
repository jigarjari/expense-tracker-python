from expense_manager import add_expense

while True:

    print("\n--- Expense Tracker ---")

    print("1. Add Expense")
    print("2. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        title = input("Enter title: ")

        amount = float(input("Enter amount: "))

        category = input("Enter category: ")

        date = input("Enter date: ")

        add_expense(title, amount, category, date)

    elif choice == "2":
        break

    else:
        print("Invalid choice")