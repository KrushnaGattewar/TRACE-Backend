"""
TRACE Intelligence Platform - Data Store Service
In-memory indexed store with JSON file backing and thread safety.
"""

import json
import os
import threading
from typing import Dict, List, Optional, Any
from app.schemas import (
    Employee, Customer, Account, Transaction, PrivilegeChange,
    AccessEvent, ProfileChange, Alert, Case, Evidence, CaseNote
)

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

class DataStore:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DataStore, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        self.employees: Dict[str, Dict[str, Any]] = {}
        self.customers: Dict[str, Dict[str, Any]] = {}
        self.accounts: Dict[str, Dict[str, Any]] = {}
        self.transactions: Dict[str, Dict[str, Any]] = {}
        self.privilege_changes: Dict[str, Dict[str, Any]] = {}
        self.access_events: Dict[str, Dict[str, Any]] = {}
        self.profile_changes: Dict[str, Dict[str, Any]] = {}
        self.alerts: Dict[str, Dict[str, Any]] = {}
        self.cases: Dict[str, Dict[str, Any]] = {}
        self.evidence: Dict[str, Dict[str, Any]] = {}

        self.reload_data()

    def reload_data(self):
        """Loads or reloads all datasets from JSON files."""
        def load_file(filename: str):
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []

        emps = load_file("employees.json")
        self.employees = {e["employee_id"]: e for e in emps}

        custs = load_file("customers.json")
        self.customers = {c["customer_id"]: c for c in custs}

        accs = load_file("accounts.json")
        self.accounts = {a["account_id"]: a for a in accs}

        txns = load_file("transactions.json")
        self.transactions = {t["transaction_id"]: t for t in txns}

        prvs = load_file("privilege_changes.json")
        self.privilege_changes = {p["change_id"]: p for p in prvs}

        acc_evs = load_file("access_events.json")
        self.access_events = {ev["access_id"]: ev for ev in acc_evs}

        prof_chgs = load_file("profile_changes.json")
        self.profile_changes = {pc["change_id"]: pc for pc in prof_chgs}

        alrts = load_file("alerts.json")
        self.alerts = {a["alert_id"]: a for a in alrts}

        css = load_file("cases.json")
        self.cases = {c["case_id"]: c for c in css}

        evds = load_file("evidence.json")
        self.evidence = {e["evidence_id"]: e for e in evds}

    def save_cases(self):
        """Saves current cases back to file."""
        filepath = os.path.join(DATA_DIR, "cases.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(list(self.cases.values()), f, indent=2)

    def save_alerts(self):
        """Saves current alerts back to file."""
        filepath = os.path.join(DATA_DIR, "alerts.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(list(self.alerts.values()), f, indent=2)

    # ==========================================
    # QUERIES
    # ==========================================

    def get_all_employees(self) -> List[Dict[str, Any]]:
        return list(self.employees.values())

    def get_employee(self, emp_id: str) -> Optional[Dict[str, Any]]:
        return self.employees.get(emp_id)

    def get_all_customers(self) -> List[Dict[str, Any]]:
        return list(self.customers.values())

    def get_customer(self, cust_id: str) -> Optional[Dict[str, Any]]:
        return self.customers.get(cust_id)

    def get_all_accounts(self) -> List[Dict[str, Any]]:
        return list(self.accounts.values())

    def get_account(self, acc_id: str) -> Optional[Dict[str, Any]]:
        return self.accounts.get(acc_id)

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        # Return sorted by timestamp desc
        return sorted(self.transactions.values(), key=lambda x: x.get("timestamp", ""), reverse=True)

    def get_transaction(self, txn_id: str) -> Optional[Dict[str, Any]]:
        return self.transactions.get(txn_id)

    def get_all_alerts(self) -> List[Dict[str, Any]]:
        return sorted(self.alerts.values(), key=lambda x: x.get("created_at", ""), reverse=True)

    def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        return self.alerts.get(alert_id)

    def get_all_cases(self) -> List[Dict[str, Any]]:
        return sorted(self.cases.values(), key=lambda x: x.get("created_at", ""), reverse=True)

    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        return self.cases.get(case_id)

    def get_all_evidence(self) -> List[Dict[str, Any]]:
        return sorted(self.evidence.values(), key=lambda x: x.get("timestamp", ""), reverse=True)

    def get_evidence(self, ev_id: str) -> Optional[Dict[str, Any]]:
        return self.evidence.get(ev_id)

    # ==========================================
    # CASE MANAGEMENT OPERATIONS
    # ==========================================

    def create_case(
        self,
        title: str,
        priority: str = "HIGH",
        alert_id: Optional[str] = None,
        assigned_investigator: Optional[str] = "EMP001",
        initial_note: Optional[str] = None
    ) -> Dict[str, Any]:
        with self._lock:
            # Generate next case ID
            existing_ids = [int(cid.split("-")[1]) for cid in self.cases.keys() if cid.startswith("CAS-")]
            next_num = max(existing_ids, default=8800) + 1
            case_id = f"CAS-{next_num}"

            related_alerts = [alert_id] if alert_id else []
            target_emp = None
            target_accs = []
            ev_ids = []

            if alert_id and alert_id in self.alerts:
                al = self.alerts[alert_id]
                target_emp = al.get("related_employee")
                target_accs = al.get("related_accounts", [])
                ev_ids = list(al.get("evidence_ids", []))
                # Update alert status
                al["status"] = "INVESTIGATING"
                self.save_alerts()

            notes = []
            if initial_note:
                notes.append({
                    "note_id": f"NOT-{len(notes)+1:02d}",
                    "author": "Sarah Jenkins (Lead FinCrime Investigator)",
                    "timestamp": "2026-10-27T10:50:00",
                    "content": initial_note
                })

            new_case = {
                "case_id": case_id,
                "title": title,
                "priority": priority,
                "status": "OPEN",
                "assigned_investigator": assigned_investigator,
                "created_at": "2026-10-27T10:46:00",
                "related_alerts": related_alerts,
                "target_employee": target_emp,
                "target_accounts": target_accs,
                "evidence": ev_ids,
                "notes": notes,
                "resolution": None
            }

            self.cases[case_id] = new_case
            self.save_cases()
            return new_case

    def update_case(
        self,
        case_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_investigator: Optional[str] = None,
        resolution: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        with self._lock:
            if case_id not in self.cases:
                return None
            case = self.cases[case_id]
            if status:
                case["status"] = status
            if priority:
                case["priority"] = priority
            if assigned_investigator:
                case["assigned_investigator"] = assigned_investigator
            if resolution is not None:
                case["resolution"] = resolution

            self.save_cases()
            return case

    def add_case_note(self, case_id: str, author: str, content: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if case_id not in self.cases:
                return None
            case = self.cases[case_id]
            notes = case.setdefault("notes", [])
            new_note = {
                "note_id": f"NOT-{len(notes)+1:02d}",
                "author": author,
                "timestamp": "2026-10-27T11:05:00",
                "content": content
            }
            notes.append(new_note)
            self.save_cases()
            return new_note

    def attach_case_evidence(self, case_id: str, evidence_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if case_id not in self.cases:
                return None
            case = self.cases[case_id]
            ev_list = case.setdefault("evidence", [])
            if evidence_id not in ev_list:
                ev_list.append(evidence_id)
            self.save_cases()
            return case

    def export_investigation_dossier(self, case_id_or_alert_id: str) -> Dict[str, Any]:
        """Generates a complete structured investigation report/dossier."""
        # Find case or alert
        case = self.cases.get(case_id_or_alert_id)
        alert = self.alerts.get(case_id_or_alert_id)

        if not alert and case and case.get("related_alerts"):
            alert = self.alerts.get(case["related_alerts"][0])
        elif not case and alert:
            # find if any case links this alert
            for c in self.cases.values():
                if alert["alert_id"] in c.get("related_alerts", []):
                    case = c
                    break

        evidence_items = []
        target_ev_ids = set()
        if alert:
            target_ev_ids.update(alert.get("evidence_ids", []))
        if case:
            target_ev_ids.update(case.get("evidence", []))

        for eid in target_ev_ids:
            if eid in self.evidence:
                evidence_items.append(self.evidence[eid])

        # Related transactions
        related_txns = []
        if alert:
            acc_set = set(alert.get("related_accounts", []))
            for t in self.transactions.values():
                if t.get("source_account") in acc_set or t.get("destination_account") in acc_set:
                    related_txns.append(t)

        return {
            "dossier_id": f"DOSSIER-{case_id_or_alert_id}",
            "generated_at": "2026-10-27T11:30:00Z",
            "classification": "ZENITH BANK SPECIAL INVESTIGATIONS UNIT - STRICTLY CONFIDENTIAL",
            "case": case,
            "alert": alert,
            "evidence": evidence_items,
            "transactions": related_txns,
            "investigator_sign_off": {
                "name": "Sarah Jenkins",
                "role": "Lead FinCrime Investigator",
                "department": "Special Financial Intelligence & Forensic Units",
                "recommendation": "IMMEDIATE ESCALATION TO FINANCIAL INTELLIGENCE UNIT (FIU) & LAW ENFORCEMENT"
            }
        }

# Global singleton
data_store = DataStore()
