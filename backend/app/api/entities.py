"""
TRACE Intelligence Platform - Entities API
Endpoints for Employees, Customers, Accounts, Transactions, Access Events.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas import Employee, Customer, Account, Transaction, AccessEvent, PrivilegeChange, ProfileChange
from app.services.data_store import data_store

router = APIRouter(tags=["Core Entities"])

# --- Employees ---
@router.get("/employees", response_model=List[Employee])
def list_employees():
    return [Employee(**e) for e in data_store.get_all_employees()]

@router.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: str):
    emp = data_store.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return Employee(**emp)

# --- Customers ---
@router.get("/customers", response_model=List[Customer])
def list_customers():
    return [Customer(**c) for c in data_store.get_all_customers()]

@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: str):
    c = data_store.get_customer(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return Customer(**c)

# --- Accounts ---
@router.get("/accounts", response_model=List[Account])
def list_accounts():
    return [Account(**a) for a in data_store.get_all_accounts()]

@router.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: str):
    a = data_store.get_account(account_id)
    if not a:
        raise HTTPException(status_code=404, detail="Account not found")
    return Account(**a)

# --- Transactions ---
@router.get("/transactions", response_model=List[Transaction])
def list_transactions(
    suspicious_only: bool = Query(False),
    account_id: Optional[str] = Query(None)
):
    txns = data_store.get_all_transactions()
    res = []
    for t in txns:
        if suspicious_only and not t.get("is_suspicious"):
            continue
        if account_id and t.get("source_account") != account_id and t.get("destination_account") != account_id:
            continue
        res.append(Transaction(**t))
    return res

@router.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: str):
    t = data_store.get_transaction(transaction_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return Transaction(**t)

# --- Access Events ---
@router.get("/access-events", response_model=List[AccessEvent])
def list_access_events(employee_id: Optional[str] = None):
    evs = list(data_store.access_events.values())
    if employee_id:
        evs = [e for e in evs if e.get("employee_id") == employee_id]
    return [AccessEvent(**e) for e in sorted(evs, key=lambda x: x.get("timestamp", ""), reverse=True)]

# --- Privilege Changes ---
@router.get("/privilege-changes", response_model=List[PrivilegeChange])
def list_privilege_changes():
    prvs = list(data_store.privilege_changes.values())
    return [PrivilegeChange(**p) for p in sorted(prvs, key=lambda x: x.get("granted_at", ""), reverse=True)]

# --- Profile Changes ---
@router.get("/profile-changes", response_model=List[ProfileChange])
def list_profile_changes():
    pcs = list(data_store.profile_changes.values())
    return [ProfileChange(**pc) for pc in sorted(pcs, key=lambda x: x.get("timestamp", ""), reverse=True)]
