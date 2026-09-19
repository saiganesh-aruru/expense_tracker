from dataclasses import asdict
import json

from models import Expense


filename = "expenses_data.json"


def save_expenses(expenses, filename="expenses_data.json"):
    data = [asdict(exp) for exp in expenses]
    with open(filename,"w",encoding="utf-8") as f :
        json.dump(data,f)

def load_expenses(filename="expenses_data.json"):
    try :
        with open(filename,"r",encoding="utf-8") as f :
            data = json.load(f)
            expenses = [Expense(**exp) for exp in data]
            return expenses
    except FileNotFoundError :
        return []
    except json.JSONDecodeError :
        print("Error decoding JSON data. Returning empty list.")
        return []