# backend/app/aggregator.py
from sqlalchemy.orm import Session
from app.models import FinancialReportModel

def get_portfolio_summary(db: Session, user_id: int):
    # Filter reports specifically for the logged-in user
    reports = db.query(FinancialReportModel).filter(FinancialReportModel.user_id == user_id).all()
    
    total_reports = len(reports)
    
    if total_reports == 0:
        return {
            "total_reports_analyzed": 0,
            "average_working_capital": 0.0,
            "average_quick_ratio": 0.0
        }
    
    total_wc = sum(r.working_capital for r in reports)
    total_qr = sum(r.quick_ratio for r in reports)
    
    return {
        "total_reports_analyzed": total_reports,
        "average_working_capital": total_wc / total_reports,
        "average_quick_ratio": total_qr / total_reports
    }
