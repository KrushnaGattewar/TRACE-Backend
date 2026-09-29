"""
TRACE Intelligence Platform - Case Management API
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from app.schemas import (
    Case, CaseCreateRequest, CaseUpdateRequest, AddNoteRequest,
    AttachEvidenceRequest, CaseNote
)
from app.services.data_store import data_store

router = APIRouter(prefix="/cases", tags=["Case Management"])

@router.get("", response_model=List[Case])
def list_cases(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    investigator: Optional[str] = Query(None, description="Filter by assigned investigator"),
    search: Optional[str] = Query(None, description="Search keyword in title or targets")
):
    cases = data_store.get_all_cases()
    res = []
    for c in cases:
        if status and c.get("status") != status.upper():
            continue
        if priority and c.get("priority") != priority.upper():
            continue
        if investigator and c.get("assigned_investigator") != investigator:
            continue
        if search:
            s = search.lower()
            text = f"{c.get('case_id', '')} {c.get('title', '')} {c.get('target_employee', '')}".lower()
            if s not in text:
                continue
        res.append(Case(**c))
    return res

@router.get("/{case_id}", response_model=Case)
def get_case(case_id: str):
    c = data_store.get_case(case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    return Case(**c)

@router.post("", response_model=Case)
def create_case(payload: CaseCreateRequest):
    new_c = data_store.create_case(
        title=payload.title,
        priority=payload.priority,
        alert_id=payload.alert_id,
        assigned_investigator=payload.assigned_investigator,
        initial_note=payload.initial_note
    )
    return Case(**new_c)

@router.patch("/{case_id}", response_model=Case)
def update_case(case_id: str, payload: CaseUpdateRequest):
    upd = data_store.update_case(
        case_id=case_id,
        status=payload.status,
        priority=payload.priority,
        assigned_investigator=payload.assigned_investigator,
        resolution=payload.resolution
    )
    if not upd:
        raise HTTPException(status_code=404, detail="Case not found")
    return Case(**upd)

@router.post("/{case_id}/notes", response_model=CaseNote)
def add_note(case_id: str, payload: AddNoteRequest):
    author = payload.author or "Sarah Jenkins (Lead FinCrime Investigator)"
    note = data_store.add_case_note(case_id, author, payload.content)
    if not note:
        raise HTTPException(status_code=404, detail="Case not found")
    return CaseNote(**note)

@router.post("/{case_id}/evidence", response_model=Case)
def attach_evidence(case_id: str, payload: AttachEvidenceRequest):
    c = data_store.attach_case_evidence(case_id, payload.evidence_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    return Case(**c)

@router.get("/{case_id}/export")
def export_case_dossier(case_id: str) -> Dict[str, Any]:
    c = data_store.get_case(case_id)
    if not c:
        # maybe it's an alert id
        a = data_store.get_alert(case_id)
        if not a:
            raise HTTPException(status_code=404, detail="Record not found")
    return data_store.export_investigation_dossier(case_id)
