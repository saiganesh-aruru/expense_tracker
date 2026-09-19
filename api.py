from fastapi import FastAPI, HTTPException 
from dataclasses import asdict
from pydantic import BaseModel , Field

from storage import load_expenses , save_expenses
from models import Expense

STORAGE_FILE = "expenses_data.json"

app = FastAPI()

class ExpenseCreate(BaseModel):
    name: str
    amount: float = Field(..., gt=0.0, description="Amount must be greater than zero")

class ExpenseUpdate(BaseModel):
    name: str | None = None
    amount: float | None = Field(default=None,gt=0.0,description="Amount must be greater than zero")

@app.get("/expenses")
def get_expenses():
    expenses = load_expenses(STORAGE_FILE)
    return [asdict(expense) for expense in expenses]


@app.get("/expenses/{id}")
def get_expense(id: int):
    expenses = load_expenses(STORAGE_FILE)

    result = next((asdict(expense) for expense in expenses if expense.id == id),None)
    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return result

@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseCreate):
    expenses = load_expenses(STORAGE_FILE)

    next_id = max(exp.id for exp in expenses) + 1 if expenses else 1
    new_expense = Expense(next_id , expense.name , expense.amount)
    expenses.append(new_expense)
    save_expenses(expenses, STORAGE_FILE)
    return asdict(new_expense)

@app.patch("/expenses/{id}")
def update_expense(id: int, expense: ExpenseUpdate):
    expenses = load_expenses(STORAGE_FILE)

    current_expense = next((exp for exp in expenses if exp.id == id), None)
    if current_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    updates = expense.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(current_expense, field, value)
    save_expenses(expenses, STORAGE_FILE)
    return asdict(current_expense)

@app.put("/expenses/{id}")
def replace_expense(id: int, expense: ExpenseCreate):
    expenses = load_expenses(STORAGE_FILE)

    current_expense = next((exp for exp in expenses if exp.id == id), None)
    if current_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    current_expense.name = expense.name
    current_expense.amount = expense.amount
    save_expenses(expenses, STORAGE_FILE)
    return asdict(current_expense)

@app.delete("/expenses/{id}")
def delete_expense(id: int) :
    expenses = load_expenses(STORAGE_FILE)

    current_expense = next((exp for exp in expenses if exp.id == id), None)
    if current_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    expenses.remove(current_expense)
    save_expenses(expenses, STORAGE_FILE)
    return {"detail": "Expense deleted"}