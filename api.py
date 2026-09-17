from fastapi import FastAPI, HTTPException 
from dataclasses import asdict
from pydantic import BaseModel , Field

from storage import load_expenses , save_expenses
from models import Expense

app = FastAPI()

class ExpenseCreate(BaseModel):
    name: str
    amount: float = Field(..., gt=0.0, description="Amount must be greater than zero")

@app.get("/expenses")
def get_expenses():
    expenses = load_expenses()
    return [asdict(expense) for expense in expenses]


@app.get("/expenses/{id}")
def get_expense(id: int):
    expenses = load_expenses()

    result = next((asdict(expense) for expense in expenses if expense.id == id),None)
    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return result

@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseCreate):
    expenses = load_expenses()
    next_id = max(exp.id for exp in expenses) + 1 if expenses else 1
    new_expense = Expense(next_id , expense.name , expense.amount)
    expenses.append(new_expense)
    save_expenses(expenses)
    return asdict(new_expense)