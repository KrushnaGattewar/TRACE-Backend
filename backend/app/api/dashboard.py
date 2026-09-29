"""
TRACE Intelligence Platform - Dashboard Summary API
"""

from fastapi import APIRouter
from app.schemas import DashboardSummary, Alert, Case
from app.services.data_store import data_store

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    all_alerts = data_store.get_all_alerts()
    all_cases = data_store.get_all_cases()
    all_txns = data_store.get_all_transactions()

    high_risk_alerts = [a for a in all_alerts if a.get("risk_level") == "HIGH"]
    open_cases = [c for c in all_cases if c.get("status") in ["OPEN", "INVESTIGATING", "ESCALATED"]]
    active_inv = [a for a in all_alerts if a.get("status") in ["OPEN", "INVESTIGATING"]]

    # Total flagged volume across suspicious transactions
    suspicious_volume = sum(t.get("amount", 0) for t in all_txns if t.get("is_suspicious"))

    return DashboardSummary(
        alerts_today=len(all_alerts),
        open_cases=len(open_cases),
        high_risk_alerts=len(high_risk_alerts),
        suspicious_volume_inr=suspicious_volume,
        active_investigations=len(active_inv),
        recent_alerts=[Alert(**a) for a in all_alerts[:6]],
        recent_cases=[Case(**c) for c in all_cases[:4]]
    )
