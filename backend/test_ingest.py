# backend/test_ingest.py
import pandas as pd
from app.database import SessionLocal
from app.processor import process_financial_report
import os

def run_test():
    # Create a quick sample CSV file for testing
    sample_data = {
        "line_item": ["current assets", "current liabilities", "total assets", "total liabilities", "total equity", "inventory"],
        "amount": [150000.0, 50000.0, 500000.0, 200000.0, 300000.0, 30000.0]
    }
    df = pd.DataFrame(sample_data)
    csv_path = "sample_financials.csv"
    df.to_csv(csv_path, index=False)

    # Open a database session and run the processor
    db = SessionLocal()
    try:
        record = process_financial_report(csv_path, db, filename="sample_financials.csv")
        print(f"Successfully processed and stored record ID: {record.id}")
        print(f"Computed Working Capital: ${record.working_capital:,.2f}")
        print(f"Computed Quick Ratio: {record.quick_ratio:.2f}")
        print(f"Computed Debt-to-Equity: {record.debt_to_equity:.2f}")
    finally:
        db.close()
        # Clean up test file
        if os.path.exists(csv_path):
            os.remove(csv_path)

if __name__ == "__main__":
    run_test()