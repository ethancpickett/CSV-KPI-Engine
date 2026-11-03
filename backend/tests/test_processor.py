# backend/tests/test_processor.py
import pandas as pd
from app.processor import process_financial_report

def test_process_financial_report(db_session, tmp_path):
    # Create a temporary sample CSV file
    csv_file = tmp_path / "test_financials.csv"
    df = pd.DataFrame({
        "line_item": [
            "current assets", "current liabilities", "total assets", 
            "total liabilities", "total equity", "inventory", 
            "cash", "revenue", "operating income", "net income"
        ],
        "amount": [
            300000.0, 100000.0, 800000.0, 
            300000.0, 500000.0, 50000.0, 
            80000.0, 600000.0, 150000.0, 90000.0
        ]
    })
    df.to_csv(csv_file, index=False)

    # Run the processor
    record = process_financial_report(str(csv_file), db_session, filename="test_financials.csv")

    # Assert correct calculations
    assert record.id is not None
    assert record.working_capital == 200000.0  # 300k - 100k
    assert record.quick_ratio == 2.5           # (300k - 50k) / 100k
    assert record.debt_to_equity == 0.6        # 300k / 500k
    assert record.cash_ratio == 0.8            # 80k / 100k
    assert record.operating_margin == 0.25     # 150k / 600k
    assert record.return_on_equity == 0.18     # 90k / 500k