# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os

from app.database import get_db, engine, Base
from app.models import FinancialReportModel
from app.processor import process_financial_report
from app.aggregator import get_portfolio_summary
from app.insights import generate_financial_insights

# Ensure tables exist on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial KPI Engine",
    description="Professional-grade financial report parser and KPI analytics API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial KPI Engine API. Navigate to /docs for interactive documentation."}

@app.post("/reports/upload", summary="Upload and process a financial statement (CSV/Excel)")
def upload_report(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process report using our ingestion engine
        record = process_financial_report(temp_file_path, db, filename=file.filename)
        return {
            "message": "File successfully uploaded and processed.",
            "report_id": record.id,
            "filename": record.filename,
            "working_capital": record.working_capital,
            "quick_ratio": record.quick_ratio,
            "debt_to_equity": record.debt_to_equity
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/portfolio/summary", summary="Get aggregated portfolio financial statistics")
def portfolio_summary(db: Session = Depends(get_db)):
    return get_portfolio_summary(db)

@app.get("/reports/{report_id}/insights", summary="Get automated financial health grade and executive insights")
def get_report_insights(report_id: int, db: Session = Depends(get_db)):
    report = db.query(FinancialReportModel).filter(FinancialReportModel.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Financial report not found.")
    return generate_financial_insights(report)
