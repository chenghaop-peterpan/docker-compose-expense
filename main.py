import os
import time
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.expense import Base, Expense

# 從環境變數讀取資料庫連線字串
# 注意主機名稱是 "db"（對應 docker-compose.yml 裡的服務名稱，而非 localhost！）
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:supersecretpassword@db:5432/expense_db",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 等待資料庫就緒並自動建立資料表
for _ in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except Exception:
        time.sleep(2)

app = FastAPI(title="Docker Compose 記帳系統 API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ExpenseCreate(BaseModel):
    item: str
    amount: float
    category: Optional[str] = "飲食"


@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI + PostgreSQL 多容器服務運行中"}


@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(
        item=expense.item,
        amount=expense.amount,
        category=expense.category,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses")
def list_expenses(db: Session = Depends(get_db)):
    records = db.query(Expense).order_by(Expense.id.desc()).all()
    total_amount = sum(r.amount for r in records)
    return {
        "count": len(records),
        "total_amount": total_amount,
        "records": records,
    }