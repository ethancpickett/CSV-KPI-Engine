# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class FinancialReportModel(Base):
    __tablename__ = "financial_reports"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Raw Balance Sheet & Income Statement line items
    current_assets = Column(Float, default=0.0)
    current_liabilities = Column(Float, default=0.0)
    total_assets = Column(Float, default=0.0)
    total_liabilities = Column(Float, default=0.0)
    total_equity = Column(Float, default=0.0)
    inventory = Column(Float, default=0.0)
    cash = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    operating_income = Column(Float, default=0.0)
    net_income = Column(Float, default=0.0)

    # Computed KPIs
    working_capital = Column(Float, default=0.0)
    quick_ratio = Column(Float, default=0.0)
    debt_to_equity = Column(Float, default=0.0)
    cash_ratio = Column(Float, default=0.0)
    operating_margin = Column(Float, default=0.0)
    return_on_equity = Column(Float, default=0.0)

    parsing_notes = Column(String, nullable=True)
