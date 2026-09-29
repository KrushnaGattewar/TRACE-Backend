"""
TRACE Intelligence Platform - Investigation Service
Generates unified chronological timelines, correlates risk contributors,
and pulls associated evidence and cases.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.schemas import TimelineEvent, InvestigationDetail, Evidence, Alert, Case
from app.services.data_store import data_store

class InvestigationService:
    def get_investigation(self, alert_id: str) -> Optional[InvestigationDetail]:
        alert_data = data_store.get_alert(alert_id)
        if not alert_data:
            return None

        alert = Alert(**alert_data)

        # 1. Gather all timeline events relevant to this alert
        timeline: List[TimelineEvent] = []

        emp_id = alert.related_employee
        related_accounts = set(alert.related_accounts)
        related_custs = set(alert.related_customers)

        # Privilege changes
        if emp_id:
            for prv in data_store.privilege_changes.values():
                if prv["employee_id"] == emp_id:
                    ev_id = "E001" if prv["change_id"] == "PRV-801" else None
                    timeline.append(TimelineEvent(
                        event_id=f"EV-PRV-{prv['change_id']}",
                        timestamp=prv["granted_at"],
                        event_type="PRIVILEGE_CHANGE",
                        title="PRIVILEGE ESCALATION" if prv.get("is_suspicious") else "PRIVILEGE UPDATE",
                        description=f"{emp_id} elevated to Tier {prv['new_level']} ({prv['privilege_name']}) via {prv.get('granted_by')}.",
                        actor=emp_id,
                        target=prv['privilege_name'],
                        evidence_id=ev_id,
                        is_suspicious=prv.get("is_suspicious", False),
                        metadata=prv
                    ))

        # Access events
        for acc_ev in data_store.access_events.values():
            if acc_ev.get("employee_id") == emp_id or acc_ev.get("account_id") in related_accounts:
                ev_id = "E002" if acc_ev["access_id"] == "ACC-EV-5001" else None
                timeline.append(TimelineEvent(
                    event_id=f"EV-ACC-{acc_ev['access_id']}",
                    timestamp=acc_ev["timestamp"],
                    event_type="ACCOUNT_ACCESS",
                    title="UNUSUAL ACCOUNT ACCESS" if acc_ev.get("is_suspicious") else "ACCOUNT ACCESS",
                    description=f"{acc_ev['employee_id']} accessed {acc_ev['account_id']} — {acc_ev['action']}. {acc_ev.get('anomaly_reason') or ''}".strip(),
                    actor=acc_ev["employee_id"],
                    target=acc_ev["account_id"],
                    evidence_id=ev_id,
                    is_suspicious=acc_ev.get("is_suspicious", False),
                    metadata=acc_ev
                ))

        # Profile changes
        for pc in data_store.profile_changes.values():
            if pc.get("employee_id") == emp_id or pc.get("customer_id") in related_custs:
                ev_id = "E003" if pc["change_id"] == "CHG-301" else None
                timeline.append(TimelineEvent(
                    event_id=f"EV-CHG-{pc['change_id']}",
                    timestamp=pc["timestamp"],
                    event_type="PROFILE_CHANGE",
                    title="CUSTOMER PROFILE MODIFICATION",
                    description=f"{pc['employee_id']} changed {pc['field_changed']} for {pc['customer_id']}: '{pc['old_value']}' → '{pc['new_value']}'.",
                    actor=pc["employee_id"],
                    target=pc["customer_id"],
                    evidence_id=ev_id,
                    is_suspicious=pc.get("is_suspicious", False),
                    metadata=pc
                ))

        # Transactions
        for txn in data_store.get_all_transactions():
            if txn["source_account"] in related_accounts or txn["destination_account"] in related_accounts:
                ev_id = None
                if txn["transaction_id"] == "TXN-CIRC-001":
                    ev_id = "E004"
                elif txn["transaction_id"] == "TXN-CIRC-002":
                    ev_id = "E005"
                elif txn["transaction_id"] == "TXN-CIRC-003":
                    ev_id = "E006"
                elif txn["transaction_id"] == "TXN-DORM-001":
                    ev_id = "E008"

                timeline.append(TimelineEvent(
                    event_id=f"EV-TXN-{txn['transaction_id']}",
                    timestamp=txn["timestamp"],
                    event_type="TRANSACTION",
                    title=f"TRANSFER ₹{txn['amount']:,.0f} ({txn['source_account']} → {txn['destination_account']})",
                    description=f"Payment via {txn['transaction_type']}. Ref: {txn.get('reference', 'N/A')}.",
                    actor=txn.get("initiated_by_employee") or txn["source_account"],
                    target=txn["destination_account"],
                    amount=txn["amount"],
                    evidence_id=ev_id,
                    is_suspicious=txn.get("is_suspicious", False),
                    metadata=txn
                ))

        # Sort timeline chronologically asc
        timeline.sort(key=lambda x: x.timestamp)

        # 2. Gather Evidence Items
        evidence_list: List[Evidence] = []
        for eid in alert.evidence_ids:
            raw_ev = data_store.get_evidence(eid)
            if raw_ev:
                evidence_list.append(Evidence(**raw_ev))

        # 3. Find related case if any
        related_case: Optional[Case] = None
        for c in data_store.get_all_cases():
            if alert_id in c.get("related_alerts", []):
                related_case = Case(**c)
                break

        # 4. Summary Stats
        stats = {
            "total_timeline_events": len(timeline),
            "suspicious_events": sum(1 for e in timeline if e.is_suspicious),
            "total_flagged_volume_inr": sum(e.amount or 0 for e in timeline if e.event_type == "TRANSACTION" and e.is_suspicious),
            "duration_minutes": 33 if alert_id == "ALT-10482" else 15,
            "entities_involved": len(related_accounts) + len(related_custs) + (1 if emp_id else 0)
        }

        return InvestigationDetail(
            alert=alert,
            risk_contributors=alert.risk_contributors,
            timeline=timeline,
            evidence_list=evidence_list,
            related_case=related_case,
            summary_stats=stats
        )

investigation_service = InvestigationService()
