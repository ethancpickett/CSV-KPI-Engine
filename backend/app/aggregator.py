# backend/app/aggregator.py
from sqlalchemy.orm import Session
from app.models import FinancialReportModel
import pandas as pd

def get_portfolio_summary(db: Session) -> dict:
    reports = db.query(FinancialReportModel).all()
    
    if not reports:
        return {"message": "No financial reports found in the database."}

    data = [{
        "working_capital": r.working_capital,
        "quick_ratio": r.quick_ratio,
        "debt_to_equity": r.debt_to_equity,
        "cash_ratio": r.cash_ratio,
        "operating_margin": r.operating_margin,
        "return_on_equity": r.return_on_equity
    } for r in reports]
    
    df = pd.DataFrame(data)

    summary = {
        "total_reports_analyzed": int(len(df)),
        "average_working_capital": float(df["working_capital"].mean()),
        "average_quick_ratio": float(df["quick_ratio"].mean()),
        "average_debt_to_equity": float(df["debt_to_equity"].mean()),
        "average_cash_ratio": float(df["cash_ratio"].mean()),
        "average_operating_margin": float(df["operating_margin"].mean()),
        "average_return_on_equity": float(df["return_on_equity"].mean()),
    }

    return summary
