# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.database import Base

class FinancialReportModel(Base):
    __tablename__ = "financial_reports"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Raw extracted totals
    current_assets = Column(Float, default=0.0)
    current_liabilities = Column(Float, default=0.0)
    total_assets = Column(Float, default=0.0)
    total_liabilities = Column(Float, default=0.0)
    total_equity = Column(Float, default=0.0)
    
    # Computed Financial Ratios
    working_capital = Column(Float, default=0.0)
    quick_ratio = Column(Float, default=0.0)
    debt_to_equity = Column(Float, default=0.0)
    
    # Optional text blob for parsing logs or notes
    parsing_notes = Column(Text, nullable=True)