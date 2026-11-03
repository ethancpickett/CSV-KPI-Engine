# backend/tests/test_api.py
import io

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Financial KPI Engine API" in response.json()["message"]

def test_upload_report_endpoint(client):
    csv_content = b"line_item,amount\ncurrent assets,200000\ncurrent liabilities,80000\ntotal assets,500000\ntotal liabilities,200000\ntotal equity,300000\ninventory,40000\ncash,50000\nrevenue,400000\noperating income,100000\nnet income,60000"
    
    response = client.post(
        "/reports/upload",
        files={"file": ("financials.csv", io.BytesIO(csv_content), "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "financials.csv"
    assert data["working_capital"] == 120000.0
    assert data["quick_ratio"] == 2.0

def test_portfolio_summary_endpoint(client):
    # Upload a report first
    csv_content = b"line_item,amount\ncurrent assets,200000\ncurrent liabilities,80000\ntotal assets,500000\ntotal liabilities,200000\ntotal equity,300000\ninventory,40000\ncash,50000\nrevenue,400000\noperating income,100000\nnet income,60000"
    client.post(
        "/reports/upload",
        files={"file": ("financials.csv", io.BytesIO(csv_content), "text/csv")}
    )

    # Fetch portfolio summary
    response = client.get("/portfolio/summary")
    assert response.status_code == 200
    summary = response.json()
    assert summary["total_reports_analyzed"] == 1
    assert summary["average_working_capital"] == 120000.0