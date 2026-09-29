"""
TRACE Intelligence Platform - Detection Engine API
"""

from fastapi import APIRouter
from app.detection.rules import detection_engine

router = APIRouter(prefix="/detection", tags=["Detection Engine"])

@router.get("/rules")
def get_rules_status():
    return detection_engine.run_all_checks()

@router.post("/run")
def trigger_detection_run():
    return detection_engine.run_all_checks()
