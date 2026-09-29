"""
TRACE Intelligence Platform - Evidence API
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas import Evidence
from app.services.data_store import data_store

router = APIRouter(prefix="/evidence", tags=["Evidence"])

@router.get("", response_model=List[Evidence])
def list_evidence(
    type: Optional[str] = Query(None, description="Filter by evidence type"),
    entity: Optional[str] = Query(None, description="Filter by related entity"),
    search: Optional[str] = Query(None, description="Search keyword in description or source")
):
    all_ev = data_store.get_all_evidence()
    res = []
    for e in all_ev:
        if type and e.get("evidence_type") != type:
            continue
        if entity and e.get("related_entity") != entity:
            continue
        if search:
            s = search.lower()
            text = f"{e.get('evidence_id', '')} {e.get('description', '')} {e.get('source', '')}".lower()
            if s not in text:
                continue
        res.append(Evidence(**e))
    return res

@router.get("/{evidence_id}", response_model=Evidence)
def get_evidence(evidence_id: str):
    e = data_store.get_evidence(evidence_id)
    if not e:
        raise HTTPException(status_code=404, detail="Evidence item not found")
    return Evidence(**e)
