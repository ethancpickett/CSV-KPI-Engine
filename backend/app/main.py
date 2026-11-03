# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base, FinancialReportModel, UserModel
from app.processor import process_financial_report
from app.aggregator import get_portfolio_summary
from app.insights import generate_financial_insights
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial KPI Engine API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for user registration
class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/register", summary="Register a new user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pwd = get_password_hash(user.password)
    new_user = UserModel(username=user.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/token", summary="OAuth2 compatible token login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/reports/upload", summary="Upload and process financial report CSV for current user")
def upload_report(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    report_record = process_financial_report(file_path, db, filename=file.filename)
    report_record.user_id = current_user.id
    db.commit()
    
    return {
        "message": "File successfully uploaded and processed.",
        "report_id": report_record.id,
        "filename": report_record.filename,
        "working_capital": report_record.working_capital,
        "quick_ratio": report_record.quick_ratio,
        "debt_to_equity": report_record.debt_to_equity
    }

@app.get("/portfolio/summary", summary="Get aggregated portfolio metrics for current user")
def portfolio_summary(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return get_portfolio_summary(db, user_id=current_user.id)

@app.get("/portfolio/history", summary="Get chronological financial history for current user")
def get_portfolio_history(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    reports = db.query(FinancialReportModel).filter(FinancialReportModel.user_id == current_user.id).order_by(FinancialReportModel.id.asc()).all()
    history = []
    for r in reports:
        history.append({
            "id": r.id,
            "filename": r.filename,
            "working_capital": r.working_capital,
            "quick_ratio": r.quick_ratio,
            "debt_to_equity": r.debt_to_equity,
            "operating_margin": r.operating_margin,
            "return_on_equity": r.return_on_equity
        })
    return history

@app.get("/reports/{report_id}/insights", summary="Get automated financial insights and health score")
def get_report_insights(report_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    report = db.query(FinancialReportModel).filter(FinancialReportModel.id == report_id, FinancialReportModel.user_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Financial report not found or unauthorized")
    return generate_financial_insights(report)
