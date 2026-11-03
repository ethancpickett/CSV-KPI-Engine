# backend/app/insights.py
from app.models import FinancialReportModel

def generate_financial_insights(report: FinancialReportModel) -> dict:
    """
    Evaluates financial KPIs against industry benchmarks, assigns a health grade,
    and generates automated executive recommendations.
    """
    strengths = []
    risks = []
    score = 100

    # 1. Quick Ratio Benchmark (Ideal: >= 1.0)
    if report.quick_ratio >= 1.5:
        strengths.append(f"Strong short-term liquidity with a Quick Ratio of {report.quick_ratio:.2f}.")
    elif report.quick_ratio >= 1.0:
        strengths.append(f"Adequate liquidity position (Quick Ratio: {report.quick_ratio:.2f}).")
    else:
        risks.append(f"Low short-term liquidity (Quick Ratio: {report.quick_ratio:.2f} is below the 1.0 benchmark).")
        score -= 20

    # 2. Debt-to-Equity Benchmark (Ideal: < 1.5)
    if report.debt_to_equity <= 1.0:
        strengths.append(f"Conservative financial leverage (Debt-to-Equity: {report.debt_to_equity:.2f}).")
    elif report.debt_to_equity <= 2.0:
        strengths.append(f"Moderate financial leverage (Debt-to-Equity: {report.debt_to_equity:.2f}).")
    else:
        risks.append(f"High financial leverage (Debt-to-Equity: {report.debt_to_equity:.2f} indicates high creditor risk).")
        score -= 25

    # 3. Operating Margin Benchmark (Ideal: > 15%)
    if report.operating_margin >= 0.20:
        strengths.append(f"Excellent operating profitability (Operating Margin: {report.operating_margin * 100:.1f}%).")
    elif report.operating_margin >= 0.10:
        strengths.append(f"Healthy operating profitability (Operating Margin: {report.operating_margin * 100:.1f}%).")
    else:
        risks.append(f"Low operational efficiency (Operating Margin: {report.operating_margin * 100:.1f}%).")
        score -= 25

    # 4. Return on Equity Benchmark (Ideal: > 12%)
    if report.return_on_equity >= 0.15:
        strengths.append(f"Strong shareholder value creation (ROE: {report.return_on_equity * 100:.1f}%).")
    elif report.return_on_equity >= 0.08:
        strengths.append(f"Acceptable return on equity (ROE: {report.return_on_equity * 100:.1f}%).")
    else:
        risks.append(f"Subpar return on equity (ROE: {report.return_on_equity * 100:.1f}%).")
        score -= 30

    # Determine Health Grade
    score = max(0, score)
    if score >= 85:
        grade = "A (Strong Financial Health)"
    elif score >= 70:
        grade = "B (Stable / Moderate Health)"
    elif score >= 50:
        grade = "C (Caution Required)"
    else:
        grade = "D (High Risk / Distressed)"

    return {
        "report_id": report.id,
        "filename": report.filename,
        "health_score": score,
        "health_grade": grade,
        "key_strengths": strengths,
        "identified_risks": risks
    }