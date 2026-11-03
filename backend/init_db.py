# backend/init_db.py
from app.database import engine, Base
from app.models import FinancialReportModel

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database table created successfully!")

if __name__ == "__main__":
    init_db()