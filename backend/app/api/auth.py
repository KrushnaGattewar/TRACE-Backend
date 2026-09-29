"""
TRACE Intelligence Platform - Authentication Endpoints
"""

from fastapi import APIRouter, HTTPException
from app.schemas import LoginRequest, UserProfile

router = APIRouter(prefix="/auth", tags=["Authentication"])

DEMO_USERS = {
    "s.jenkins@zenith-bank.internal": {
        "employee_id": "EMP001",
        "name": "Sarah Jenkins",
        "role": "Lead FinCrime Investigator",
        "department": "Financial Crime & AML",
        "privilege_level": 5,
        "token": "tok_auth_lead_investigator_8912"
    },
    "v.malhotra@zenith-bank.internal": {
        "employee_id": "EMP007",
        "name": "Vikram Malhotra",
        "role": "Senior Operations Analyst",
        "department": "Core Banking Operations",
        "privilege_level": 4,
        "token": "tok_auth_analyst_007"
    }
}

@router.post("/login", response_model=UserProfile)
def login(payload: LoginRequest):
    # For prototype convenience, allow demo login with either standard password or direct click
    email = payload.username.strip().lower()
    if email in DEMO_USERS:
        return UserProfile(**DEMO_USERS[email])
    
    # Allow fallback demo login
    return UserProfile(
        employee_id="EMP001",
        name="Sarah Jenkins",
        role="Lead FinCrime Investigator",
        department="Financial Crime & AML",
        privilege_level=5,
        token="tok_auth_lead_investigator_8912"
    )

@router.get("/me", response_model=UserProfile)
def get_current_user():
    return UserProfile(
        employee_id="EMP001",
        name="Sarah Jenkins",
        role="Lead FinCrime Investigator",
        department="Financial Crime & AML",
        privilege_level=5,
        token="tok_auth_lead_investigator_8912"
    )
