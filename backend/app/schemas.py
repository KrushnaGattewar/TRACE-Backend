"""
TRACE Intelligence Platform - Schemas and Data Models
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime

# ==========================================
# 1. CORE ENTITY SCHEMAS
# ==========================================

class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    role: str
    privilege_level: int
    status: str
    last_login: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None

class Customer(BaseModel):
    customer_id: str
    name: str
    risk_level: str
    account_ids: List[str]
    status: str
    kyc_status: Optional[str] = None
    segment: Optional[str] = None
    residence: Optional[str] = None
    phone: Optional[str] = None

class Account(BaseModel):
    account_id: str
    customer_id: str
    account_type: str
    balance: float
    currency: str = "INR"
    status: str
    opened_date: str
    branch: Optional[str] = None
    label: Optional[str] = None

class Transaction(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str = "INR"
    timestamp: str
    transaction_type: str
    status: str
    reference: Optional[str] = None
    channel: Optional[str] = None
    initiated_by_employee: Optional[str] = None
    is_suspicious: bool = False
    scenario_tag: Optional[str] = None

class PrivilegeChange(BaseModel):
    change_id: str
    employee_id: str
    previous_level: Optional[int] = None
    new_level: int
    privilege_name: str
    granted_at: str
    granted_by: str
    approval_ticket: Optional[str] = None
    reason: Optional[str] = None
    ip_address: Optional[str] = None
    is_suspicious: bool = False

class AccessEvent(BaseModel):
    access_id: str
    employee_id: str
    account_id: str
    timestamp: str
    action: str
    device_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    is_suspicious: bool = False
    anomaly_reason: Optional[str] = None

class ProfileChange(BaseModel):
    change_id: str
    employee_id: str
    customer_id: str
    timestamp: str
    field_changed: str
    old_value: str
    new_value: str
    channel: Optional[str] = None
    supervisor_override: Optional[str] = None
    is_suspicious: bool = False
    reason: Optional[str] = None

# ==========================================
# 2. EVIDENCE & ALERTS
# ==========================================

class Evidence(BaseModel):
    evidence_id: str
    evidence_type: str
    source: str
    timestamp: str
    description: str
    related_entity: str
    related_event: Optional[str] = None
    hash_signature: Optional[str] = None
    confidence: Optional[str] = "VERIFIED_HIGH"
    relationship_to_alert: Optional[str] = None

class RiskContributor(BaseModel):
    name: str
    score: int
    evidence_id: Optional[str] = None
    rule: Optional[str] = None

class Alert(BaseModel):
    alert_id: str
    alert_type: str
    risk_level: str
    risk_score: int
    status: str
    created_at: str
    related_employee: Optional[str] = None
    related_accounts: List[str] = []
    related_customers: List[str] = []
    summary: str
    risk_contributors: List[RiskContributor] = []
    evidence_ids: List[str] = []

# ==========================================
# 3. CASE MANAGEMENT
# ==========================================

class CaseNote(BaseModel):
    note_id: str
    author: str
    timestamp: str
    content: str

class Case(BaseModel):
    case_id: str
    title: str
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    status: str    # OPEN, INVESTIGATING, ESCALATED, RESOLVED, CLOSED, FALSE_POSITIVE
    assigned_investigator: Optional[str] = None
    created_at: str
    related_alerts: List[str] = []
    target_employee: Optional[str] = None
    target_accounts: List[str] = []
    evidence: List[str] = []
    notes: List[CaseNote] = []
    resolution: Optional[str] = None

class CaseCreateRequest(BaseModel):
    title: str
    priority: str = "HIGH"
    alert_id: Optional[str] = None
    assigned_investigator: Optional[str] = "EMP001"
    initial_note: Optional[str] = None

class CaseUpdateRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_investigator: Optional[str] = None
    resolution: Optional[str] = None

class AddNoteRequest(BaseModel):
    content: str
    author: Optional[str] = "Sarah Jenkins (Lead FinCrime Investigator)"

class AttachEvidenceRequest(BaseModel):
    evidence_id: str

# ==========================================
# 4. UNIFIED TIMELINE & INVESTIGATION
# ==========================================

class TimelineEvent(BaseModel):
    event_id: str
    timestamp: str
    event_type: str  # PRIVILEGE_CHANGE, ACCOUNT_ACCESS, PROFILE_CHANGE, TRANSACTION, ALERT_TRIGGER
    title: str
    description: str
    actor: Optional[str] = None
    target: Optional[str] = None
    amount: Optional[float] = None
    evidence_id: Optional[str] = None
    is_suspicious: bool = False
    metadata: Dict[str, Any] = {}

class InvestigationDetail(BaseModel):
    alert: Alert
    risk_contributors: List[RiskContributor]
    timeline: List[TimelineEvent]
    evidence_list: List[Evidence]
    related_case: Optional[Case] = None
    summary_stats: Dict[str, Any] = {}

# ==========================================
# 5. GRAPH SCHEMAS
# ==========================================

class GraphNode(BaseModel):
    id: str
    label: str
    entity_type: str  # EMPLOYEE, CUSTOMER, ACCOUNT, PRIVILEGE, TRANSACTION
    risk_level: Optional[str] = "NORMAL"
    subtitle: Optional[str] = None
    properties: Dict[str, Any] = {}

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship: str  # HAS_PRIVILEGE, ACCESSED, MODIFIED, OWNS, TRANSFERRED_TO
    label: Optional[str] = None
    amount: Optional[float] = None
    timestamp: Optional[str] = None
    is_suspicious: bool = False
    evidence_id: Optional[str] = None
    properties: Dict[str, Any] = {}

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

# ==========================================
# 6. DASHBOARD & AUTH SCHEMAS
# ==========================================

class DashboardSummary(BaseModel):
    alerts_today: int
    open_cases: int
    high_risk_alerts: int
    suspicious_volume_inr: float
    active_investigations: int
    recent_alerts: List[Alert]
    recent_cases: List[Case]

class LoginRequest(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    employee_id: str
    name: str
    role: str
    department: str
    privilege_level: int
    token: str
