from models import Expense
from storage import load_expenses, save_expenses

expenses = load_expenses()
next_id = max(expense.id for expense in expenses) + 1 if expenses else 1

def show_menu():
    print("1. Add Expense")
    print("2. Delete Expenses")
    print("3. List Expenses")
    print("4. Total")
    print("5. Exit")

def add_expense(expenses, next_id):
    name = input("Enter expense name :")
    try:
        amount = float(input("Enter expense amount :"))
    except ValueError:
        print("Invalid input. Enter a valid amount")
        return next_id
    
    if amount < 0:
        print("Amount cannot be negative. Enter a valid amount")
        return next_id

    expenses.append(Expense(next_id, name, amount))
    save_expenses(expenses)

    return next_id + 1

def delete_expense(expenses):
    try:
        delete_id = int(input("Enter expense id to delete :"))
    except ValueError :
        print("Invalid input.Enter a valid id")
        return expenses
    
    old_length = len(expenses)
    expenses = [exp for exp in expenses if exp.id != delete_id]


    if old_length == len(expenses) :
        print("Expense not found")
        return expenses
    save_expenses(expenses)
    return expenses

def list_expenses(expenses) :
    if len(expenses) == 0 :
        print("No expenses found")
        return
    for exp in expenses:
        print(f"{exp.id} {exp.name} {exp.amount}")

def total(expenses) :
    total_amount = sum(exp.amount for exp in expenses)
    return total_amount

while True :
    show_menu()
    try :
        choice = int(input("Enter your choice :"))
    except ValueError :
        print("Invalid input.Enter a valid choice")
        continue


    if choice == 1:
        next_id = add_expense(expenses, next_id)

    elif choice == 2:
        expenses = delete_expense(expenses)

    elif choice == 3:
        list_expenses(expenses)

    elif choice == 4:
        print("Total expense :" + str(total(expenses)))

    elif choice == 5:
        print("Exiting...")
        break

    else :
        print("Invalid choice. Enter a valid choice")