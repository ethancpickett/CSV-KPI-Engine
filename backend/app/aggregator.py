# backend/app/aggregator.py
from sqlalchemy.orm import Session
from app.models import FinancialReportModel
import pandas as pd

def get_portfolio_summary(db: Session) -> dict:
    """
    Queries all stored financial reports and calculates aggregate statistics 
    like portfolio averages and liquidity benchmarks.
    """
    reports = db.query(FinancialReportModel).all()
    
    if not reports:
        return {"message": "No financial reports found in the database."}

    # Load database records into a Pandas DataFrame for statistical crunching
    data = [{
        "id": r.id,
        "filename": r.filename,
        "created_at": r.created_at,
        "current_assets": r.current_assets,
        "current_liabilities": r.current_liabilities,
        "working_capital": r.working_capital,
        "quick_ratio": r.quick_ratio,
        "debt_to_equity": r.debt_to_equity
    } for r in reports]
    
    df = pd.DataFrame(data)

    # Compute aggregate portfolio metrics
    summary = {
        "total_reports_analyzed": int(len(df)),
        "average_working_capital": float(df["working_capital"].mean()),
        "average_quick_ratio": float(df["quick_ratio"].mean()),
        "average_debt_to_equity": float(df["debt_to_equity"].mean()),
        "min_quick_ratio": float(df["quick_ratio"].min()),
        "max_quick_ratio": float(df["quick_ratio"].max()),
    }

    return summary