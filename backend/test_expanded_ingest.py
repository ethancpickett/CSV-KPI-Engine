# backend/test_expanded_ingest.py
import pandas as pd
from app.database import SessionLocal
from app.processor import process_financial_report
import os

def run_expanded_test():
    # Create a sample CSV including our new line items
    sample_data = {
        "line_item": [
            "current assets", "current liabilities", "total assets", 
            "total liabilities", "total equity", "inventory", 
            "cash", "revenue", "operating income", "net income"
        ],
        "amount": [
            200000.0, 80000.0, 600000.0, 
            250000.0, 350000.0, 40000.0, 
            50000.0, 500000.0, 120000.0, 75000.0
        ]
    }
    df = pd.DataFrame(sample_data)
    csv_path = "sample_expanded_financials.csv"
    df.to_csv(csv_path, index=False)

    # Open a database session and run the processor
    db = SessionLocal()
    try:
        record = process_financial_report(csv_path, db, filename="sample_expanded_financials.csv")
        print("--- Expanded Financial KPI Engine Test ---")
        print(f"Successfully processed and stored record ID: {record.id}")
        print(f"Working Capital: ${record.working_capital:,.2f}")
        print(f"Quick Ratio: {record.quick_ratio:.2f}")
        print(f"Debt-to-Equity: {record.debt_to_equity:.2f}")
        print(f"Cash Ratio: {record.cash_ratio:.2f}")
        print(f"Operating Margin: {record.operating_margin * 100:.2f}%")
        print(f"Return on Equity (ROE): {record.return_on_equity * 100:.2f}%")
    finally:
        db.close()
        # Clean up test file
        if os.path.exists(csv_path):
            os.remove(csv_path)

if __name__ == "__main__":
    run_expanded_test()