# backend/test_aggregate.py
from app.database import SessionLocal
from app.aggregator import get_portfolio_summary

def run_aggregation_test():
    db = SessionLocal()
    try:
        summary = get_portfolio_summary(db)
        print("--- Portfolio Financial Aggregation Summary ---")
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"{key}: {value:,.2f}")
            else:
                print(f"{key}: {value}")
    finally:
        db.close()

if __name__ == "__main__":
    run_aggregation_test()