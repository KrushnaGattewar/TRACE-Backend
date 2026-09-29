"""
TRACE Intelligence Platform - Alerts API
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas import Alert, InvestigationDetail
from app.services.data_store import data_store
from app.investigations.investigation_service import investigation_service

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[Alert])
def list_alerts(
    risk: Optional[str] = Query(None, description="Filter by risk level (HIGH, MEDIUM, LOW)"),
    status: Optional[str] = Query(None, description="Filter by status (OPEN, INVESTIGATING, RESOLVED)"),
    employee: Optional[str] = Query(None, description="Filter by related employee ID"),
    search: Optional[str] = Query(None, description="Search keyword in summary or type")
):
    alerts = data_store.get_all_alerts()
    res = []
    for a in alerts:
        if risk and a.get("risk_level") != risk.upper():
            continue
        if status and a.get("status") != status.upper():
            continue
        if employee and a.get("related_employee") != employee.upper():
            continue
        if search:
            s = search.lower()
            text = f"{a.get('alert_id', '')} {a.get('alert_type', '')} {a.get('summary', '')} {a.get('related_employee', '')}".lower()
            if s not in text:
                continue
        res.append(Alert(**a))
    return res

@router.get("/{alert_id}/investigation", response_model=InvestigationDetail)
def get_alert_investigation(alert_id: str):
    detail = investigation_service.get_investigation(alert_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Alert investigation not found")
    return detail

@router.get("/{alert_id}", response_model=Alert)
def get_alert(alert_id: str):
    a = data_store.get_alert(alert_id)
    if not a:
        raise HTTPException(status_code=404, detail="Alert not found")
    return Alert(**a)
