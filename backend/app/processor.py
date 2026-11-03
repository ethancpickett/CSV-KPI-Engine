# backend/app/processor.py
import pandas as pd
from sqlalchemy.orm import Session
from app.models import FinancialReportModel

def process_financial_report(file_path: str, db: Session, filename: str) -> FinancialReportModel:
    """
    Reads a financial report (CSV or Excel), computes KPIs, and saves it to the database.
    """
    # 1. Read file using Pandas based on extension
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

    # Expecting standard columns or a key-value mapping in the file
    # Let's map typical line items dynamically or assume standard structure:
    # Example expected columns: 'line_item', 'amount' or a flat record layout.
    # For robust handling, let's look for standard rows/columns:
    data = dict(zip(df.iloc[:, 0].str.lower(), df.iloc[:, 1]))

    # Extract raw values safely with defaults
    current_assets = float(data.get('current assets', 0.0))
    current_liabilities = float(data.get('current liabilities', 0.0))
    total_assets = float(data.get('total assets', 0.0))
    total_liabilities = float(data.get('total liabilities', 0.0))
    total_equity = float(data.get('total equity', 0.0))
    inventory = float(data.get('inventory', 0.0)) # Used for quick ratio

    # Compute Financial KPIs
    working_capital = current_assets - current_liabilities
    
    # Quick Ratio = (Current Assets - Inventory) / Current Liabilities
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities > 0 else 0.0
    
    # Debt-to-Equity = Total Liabilities / Total Equity
    debt_to_equity = total_liabilities / total_equity if total_equity > 0 else 0.0

    # Create database model instance
    report_record = FinancialReportModel(
        filename=filename,
        current_assets=current_assets,
        current_liabilities=current_liabilities,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        total_equity=total_equity,
        working_capital=working_capital,
        quick_ratio=quick_ratio,
        debt_to_equity=debt_to_equity,
        parsing_notes="Successfully parsed and processed via automated engine."
    )

    # Save to database
    db.add(report_record)
    db.commit()
    db.refresh(report_record)

    return report_record