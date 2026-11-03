# backend/app/processor.py
import pandas as pd
from sqlalchemy.orm import Session
from app.models import FinancialReportModel

def process_financial_report(file_path: str, db: Session, filename: str) -> FinancialReportModel:
    """
    Reads a financial report (CSV or Excel), computes expanded KPIs, and saves to database.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

    data = dict(zip(df.iloc[:, 0].str.lower().str.strip(), df.iloc[:, 1]))

    # Extract raw values safely
    current_assets = float(data.get('current assets', 0.0))
    current_liabilities = float(data.get('current liabilities', 0.0))
    total_assets = float(data.get('total assets', 0.0))
    total_liabilities = float(data.get('total liabilities', 0.0))
    total_equity = float(data.get('total equity', 0.0))
    inventory = float(data.get('inventory', 0.0))
    cash = float(data.get('cash', 0.0))
    revenue = float(data.get('revenue', 0.0))
    operating_income = float(data.get('operating income', 0.0))
    net_income = float(data.get('net income', 0.0))

    # Compute Standard & Expanded Financial KPIs
    working_capital = current_assets - current_liabilities
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities > 0 else 0.0
    debt_to_equity = total_liabilities / total_equity if total_equity > 0 else 0.0
    
    # New Metrics
    cash_ratio = cash / current_liabilities if current_liabilities > 0 else 0.0
    operating_margin = operating_income / revenue if revenue > 0 else 0.0
    return_on_equity = net_income / total_equity if total_equity > 0 else 0.0

    report_record = FinancialReportModel(
        filename=filename,
        current_assets=current_assets,
        current_liabilities=current_liabilities,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        total_equity=total_equity,
        inventory=inventory,
        cash=cash,
        revenue=revenue,
        operating_income=operating_income,
        net_income=net_income,
        working_capital=working_capital,
        quick_ratio=quick_ratio,
        debt_to_equity=debt_to_equity,
        cash_ratio=cash_ratio,
        operating_margin=operating_margin,
        return_on_equity=return_on_equity,
        parsing_notes="Successfully parsed with expanded metric suite."
    )

    db.add(report_record)
    db.commit()
    db.refresh(report_record)

    return report_record
