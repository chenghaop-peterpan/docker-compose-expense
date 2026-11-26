from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)        # 消費項目
    amount = Column(Float, nullable=False)       # 金額
    category = Column(String, default="一般")     # 分類
    created_at = Column(DateTime, default=datetime.now)