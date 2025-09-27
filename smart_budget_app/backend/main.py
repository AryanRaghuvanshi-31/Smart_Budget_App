from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import math
import sqlite3
import os

# --- Configuration ---
DATABASE_URL = "budget.db"
# React Dev Server origins
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]


# --- Database Initialization ---

def get_db_connection():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def create_tables():
    """Creates the necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Budget/Session Table (to link all expenses to a budget entry)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monthly_budget REAL NOT NULL,
            date_recorded TEXT NOT NULL
        );
    """)

    # 2. Expenses Table (linked to the budget table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget_id INTEGER,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            date_incurred TEXT NOT NULL,
            category TEXT,
            split_with TEXT,
            your_share REAL NOT NULL,
            FOREIGN KEY (budget_id) REFERENCES budgets (id)
        );
    """)
    conn.commit()
    conn.close()

# Initialize tables when the app starts
create_tables()


# --- Pydantic Models for Data Validation ---

class ExpenseItem(BaseModel):
    id: int
    amount: float
    description: str
    date: datetime.datetime 
    category: str
    splitWith: List[int]
    yourShare: float

class BudgetDataInput(BaseModel):
    budget: float
    expenses: List[ExpenseItem]

class PredictionOutput(BaseModel):
    type: str
    message: str
    details: str
    dailyAverageSpending: float
    projectedMonthlySpending: float
    willExceedBy20th: bool
    spendingBy20th: float


# --- FastAPI App Initialization ---

app = FastAPI(title="Smart Budget ML API with SQLite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Prediction Logic (ML/Business Logic) ---

def calculate_budget_prediction(budget: float, expenses: List[ExpenseItem]) -> Dict[str, Any]:
    current_date = datetime.date.today()
    current_month = current_date.month
    current_year = current_date.year
    day_of_month = current_date.day
    
    # Calculate days in current month
    next_month = current_month % 12 + 1
    next_year = current_year if next_month != 1 else current_year + 1
    days_in_month = (datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)).day

    # Filter expenses for current month
    current_month_expenses = [
        e for e in expenses
        if e.date.month == current_month and e.date.year == current_year
    ]

    total_spent = sum(expense.yourShare for expense in current_month_expenses)
    remaining_budget = budget - total_spent

    # Core Prediction Calculations
    if day_of_month == 0 or total_spent == 0:
        daily_average_spending = 0
    else:
        daily_average_spending = total_spent / day_of_month
        
    projected_monthly_spending = daily_average_spending * days_in_month
    projected_overspend = projected_monthly_spending - budget
    overspend_percentage = (projected_overspend / budget) * 100 if budget > 0 else 0

    # 20th Date Projection
    spending_by_20th = daily_average_spending * 20
    will_exceed_by_20th = spending_by_20th > budget

    # Determine status and message
    if will_exceed_by_20th:
        status_type = 'critical'
        message = "🚨 WARNING: You will overspend by the 20th of the month!"
        excess_by_20th = spending_by_20th - budget
        percentage_excess_by20th = (excess_by_20th / budget) * 100 if budget > 0 else 0
        details = (
            f"At current spending rate (${daily_average_spending:.2f}/day), "
            f"you'll spend ${spending_by_20th:.2f} by the 20th - "
            f"exceeding budget by ${excess_by_20th:.2f} ({percentage_excess_by20th:.1f}%)"
        )
    elif projected_overspend > 0 and daily_average_spending > 0:
        days_until_overspend = remaining_budget / daily_average_spending
        budget_exhaustion_day = day_of_month + days_until_overspend
        status_type = 'danger'
        message = f"🔴 CRITICAL: Budget will be exceeded by day {math.ceil(budget_exhaustion_day)}!"
        details = (
            f"At current rate (${daily_average_spending:.2f}/day), "
            f"you'll overspend the monthly budget by ~${projected_overspend:.2f} "
            f"({overspend_percentage:.1f}%)"
        )
    else:
        status_type = 'success'
        message = '✅ On track to stay within budget!'
        remaining_by_20th = budget - spending_by_20th
        details = (
            f"By the 20th: ${spending_by_20th:.2f} spent, ${remaining_by_20th:.2f} remaining | "
            f"Monthly projection: ${projected_monthly_spending:.2f}"
        )

    return {
        "type": status_type,
        "message": message,
        "details": details,
        "dailyAverageSpending": daily_average_spending,
        "projectedMonthlySpending": projected_monthly_spending,
        "willExceedBy20th": will_exceed_by_20th,
        "spendingBy20th": spending_by_20th
    }


# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "FastAPI Budget ML Backend with SQLite Running"}

@app.post("/predict_budget", response_model=PredictionOutput)
def predict_budget(data: BudgetDataInput):
    """
    Endpoint for React to request a budget prediction status.
    """
    prediction_result = calculate_budget_prediction(data.budget, data.expenses)
    return prediction_result

@app.post("/save_data")
def save_budget_data(data: BudgetDataInput):
    """
    Endpoint for React to save the current budget and all expenses to DB.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Insert into budgets table
        cursor.execute(
            "INSERT INTO budgets (monthly_budget, date_recorded) VALUES (?, ?)",
            (data.budget, datetime.datetime.now().isoformat())
        )
        budget_id = cursor.lastrowid
        
        # 2. Insert all expenses linked to this budget
        expense_records = []
        for expense in data.expenses:
            # Convert splitWith list of integers back to a string for storage
            split_str = ",".join(map(str, expense.splitWith))
            
            expense_records.append((
                budget_id,
                expense.amount,
                expense.description,
                expense.date.isoformat(),
                expense.category,
                split_str,
                expense.yourShare
            ))

        cursor.executemany(
            """
            INSERT INTO expenses (budget_id, amount, description, date_incurred, category, split_with, your_share)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            expense_records
        )
        
        conn.commit()
        return {"status": "success", "message": f"Budget and {len(data.expenses)} expenses saved successfully with budget_id: {budget_id}"}
        
    except Exception as e:
        conn.rollback()
        # Log the error for debugging
        print(f"SQLITE ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

# --- To Run ---
# uvicorn main:app --reload --port 8000