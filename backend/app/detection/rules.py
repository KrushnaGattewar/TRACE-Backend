"""
TRACE Intelligence Platform - Detection Engine
Implements transparent rule-based detection with explainable risk breakdown and structured evidence.
Rules:
  R01 - Large Transaction
  R02 - Transaction Splitting (Smurfing)
  R03 - Circular Transfer (Cycle Detection)
  R04 - Rapid Transfer Chain
  R05 - Privilege Escalation
  R06 - Unusual Access
  R07 - Profile Change Before Transaction
  R08 - Dormant Account Activation
  R09 - Employee-Account Relationship Anomaly
  R10 - Unusual Timing
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime
from collections import defaultdict
from app.services.data_store import data_store

class DetectionEngine:
    def __init__(self, large_txn_threshold: float = 400000.0):
        self.large_txn_threshold = large_txn_threshold

    def parse_dt(self, ts_str: str) -> datetime:
        try:
            return datetime.fromisoformat(ts_str.replace("Z", ""))
        except Exception:
            return datetime(2026, 10, 27, 10, 0, 0)

    # -------------------------------------------------------------
    # R01: Large Transaction
    # -------------------------------------------------------------
    def check_r01_large_transaction(self, txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        for t in txns:
            if t.get("amount", 0) >= self.large_txn_threshold:
                findings.append({
                    "rule": "R01",
                    "name": "Large Transaction",
                    "score": 20,
                    "target": t["transaction_id"],
                    "description": f"Transaction {t['transaction_id']} of ₹{t['amount']:,.2f} exceeds threshold ₹{self.large_txn_threshold:,.2f} ({t['source_account']} → {t['destination_account']}).",
                    "transaction_id": t["transaction_id"],
                    "accounts": [t["source_account"], t["destination_account"]]
                })
        return findings

    # -------------------------------------------------------------
    # R02: Transaction Splitting (Smurfing)
    # -------------------------------------------------------------
    def check_r02_splitting(self, txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        # Group by source account within 30 min window
        by_src = defaultdict(list)
        for t in txns:
            by_src[t["source_account"]].append(t)

        for src_acc, acc_txns in by_src.items():
            if len(acc_txns) < 3:
                continue
            sorted_t = sorted(acc_txns, key=lambda x: self.parse_dt(x["timestamp"]))
            for i in range(len(sorted_t) - 2):
                cluster = [sorted_t[i]]
                t0 = self.parse_dt(sorted_t[i]["timestamp"])
                for j in range(i + 1, len(sorted_t)):
                    tj = self.parse_dt(sorted_t[j]["timestamp"])
                    if (tj - t0).total_seconds() <= 1800:  # 30 mins
                        cluster.append(sorted_t[j])
                    else:
                        break
                if len(cluster) >= 3:
                    total_amt = sum(c.get("amount", 0) for c in cluster)
                    # if individual txns are below 100k but sum is > 300k
                    if total_amt >= 300000 and any(c.get("amount", 0) < 100000 for c in cluster):
                        findings.append({
                            "rule": "R02",
                            "name": "Transaction Splitting (Smurfing)",
                            "score": 35,
                            "target": src_acc,
                            "description": f"Source {src_acc} disbursed {len(cluster)} transactions totaling ₹{total_amt:,.2f} within 30 minutes.",
                            "transaction_ids": [c["transaction_id"] for c in cluster],
                            "accounts": [src_acc] + [c["destination_account"] for c in cluster]
                        })
                        break
        return findings

    # -------------------------------------------------------------
    # R03: Circular Transfer Loops (Graph Cycle Search)
    # -------------------------------------------------------------
    def check_r03_circular_transfer(self, txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        # Directed graph of accounts
        adj = defaultdict(list)
        for t in txns:
            adj[t["source_account"]].append((t["destination_account"], t))

        # Detect cycles of length 2 to 5 within a reasonable time window
        cycles_found = set()

        def dfs(curr, start, path, path_txns, visited):
            if len(path) > 5:
                return
            for nxt, txn in adj.get(curr, []):
                if nxt == start and len(path) >= 3:
                    cycle_key = tuple(sorted(path))
                    if cycle_key not in cycles_found:
                        cycles_found.add(cycle_key)
                        all_txns = path_txns + [txn]
                        findings.append({
                            "rule": "R03",
                            "name": "Circular Money Flow",
                            "score": 15,
                            "target": f"{' → '.join(path)} → {start}",
                            "description": f"Detected closed money cycle across {len(path)} accounts: {' → '.join(path)} → {start}.",
                            "loop_accounts": path,
                            "transaction_ids": [tx["transaction_id"] for tx in all_txns]
                        })
                    return
                if nxt not in visited and len(path) < 4:
                    visited.add(nxt)
                    dfs(nxt, start, path + [nxt], path_txns + [txn], visited)
                    visited.remove(nxt)

        all_nodes = list(adj.keys())
        for node in all_nodes:
            dfs(node, node, [node], [], {node})

        return findings

    # -------------------------------------------------------------
    # R04: Rapid Transfer Chain
    # -------------------------------------------------------------
    def check_r04_rapid_transfer_chain(self, txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        # Look for hop sequence where destination of txn 1 is source of txn 2 within 15 mins
        by_src = defaultdict(list)
        for t in txns:
            by_src[t["source_account"]].append(t)

        for t1 in txns:
            dst = t1["destination_account"]
            if dst in by_src:
                t1_time = self.parse_dt(t1["timestamp"])
                for t2 in by_src[dst]:
                    t2_time = self.parse_dt(t2["timestamp"])
                    diff = (t2_time - t1_time).total_seconds()
                    if 0 < diff <= 600:  # within 10 mins
                        findings.append({
                            "rule": "R04",
                            "name": "Rapid Transfer Chain",
                            "score": 15,
                            "target": f"{t1['source_account']} → {dst} → {t2['destination_account']}",
                            "description": f"Pass-through hop: ₹{t1['amount']:,.2f} received by {dst} and ₹{t2['amount']:,.2f} forwarded within {int(diff/60)} minutes.",
                            "transaction_ids": [t1["transaction_id"], t2["transaction_id"]],
                            "accounts": [t1["source_account"], dst, t2["destination_account"]]
                        })
        return findings

    # -------------------------------------------------------------
    # R05: Privilege Escalation
    # -------------------------------------------------------------
    def check_r05_privilege_escalation(self, prvs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        for p in prvs:
            prev = p.get("previous_level") or 1
            curr = p.get("new_level", 1)
            is_suspicious = p.get("is_suspicious", False) or (curr - prev >= 2) or ("UNAUTH" in p.get("approval_ticket", ""))
            if is_suspicious:
                findings.append({
                    "rule": "R05",
                    "name": "Privilege Escalation",
                    "score": 20,
                    "target": p["employee_id"],
                    "description": f"Employee {p['employee_id']} elevated from Level {prev} to Level {curr} ({p['privilege_name']}) via {p.get('granted_by', 'UNKNOWN')}.",
                    "employee_id": p["employee_id"],
                    "change_id": p["change_id"]
                })
        return findings

    # -------------------------------------------------------------
    # R06: Unusual Access
    # -------------------------------------------------------------
    def check_r06_unusual_access(self, acc_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        for ev in acc_events:
            if ev.get("is_suspicious", False) or ev.get("anomaly_reason"):
                findings.append({
                    "rule": "R06",
                    "name": "Unusual Employee Access",
                    "score": 25,
                    "target": f"{ev['employee_id']} → {ev['account_id']}",
                    "description": ev.get("anomaly_reason") or f"Unauthorized ledger access by {ev['employee_id']} on {ev['account_id']}.",
                    "employee_id": ev["employee_id"],
                    "account_id": ev["account_id"],
                    "access_id": ev["access_id"]
                })
        return findings

    # -------------------------------------------------------------
    # R07: Profile Change Before Transaction
    # -------------------------------------------------------------
    def check_r07_profile_change_before_txn(
        self,
        prof_changes: List[Dict[str, Any]],
        txns: List[Dict[str, Any]],
        accounts: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        findings = []
        for chg in prof_changes:
            chg_time = self.parse_dt(chg["timestamp"])
            cid = chg["customer_id"]
            # find accounts owned by this customer
            cust_accs = [aid for aid, a in accounts.items() if a.get("customer_id") == cid]
            for t in txns:
                if t.get("source_account") in cust_accs:
                    t_time = self.parse_dt(t["timestamp"])
                    diff = (t_time - chg_time).total_seconds()
                    if 0 <= diff <= 3600:  # within 1 hour
                        findings.append({
                            "rule": "R07",
                            "name": "Profile Modification Before Transaction",
                            "score": 10,
                            "target": cid,
                            "description": f"Field '{chg['field_changed']}' modified by {chg['employee_id']} {int(diff/60)}m prior to outbound transfer ₹{t['amount']:,.2f}.",
                            "employee_id": chg["employee_id"],
                            "customer_id": cid,
                            "account_id": t["source_account"],
                            "transaction_id": t["transaction_id"]
                        })
        return findings

    # -------------------------------------------------------------
    # R08: Dormant Account Activation
    # -------------------------------------------------------------
    def check_r08_dormant_activation(
        self,
        txns: List[Dict[str, Any]],
        accounts: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        findings = []
        for t in txns:
            src = t.get("source_account")
            if src in accounts:
                acc = accounts[src]
                if acc.get("status") == "RESTRICTED" or "Dormant" in acc.get("account_type", ""):
                    findings.append({
                        "rule": "R08",
                        "name": "Dormant Account Activation",
                        "score": 35,
                        "target": src,
                        "description": f"Dormant/Restricted account {src} initiated transfer of ₹{t['amount']:,.2f} to {t['destination_account']}.",
                        "account_id": src,
                        "transaction_id": t["transaction_id"]
                    })
        return findings

    # -------------------------------------------------------------
    # R09: Employee-Account Relationship Anomaly
    # -------------------------------------------------------------
    def check_r09_relationship_anomaly(
        self,
        employees: Dict[str, Dict[str, Any]],
        access_events: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        findings = []
        for ev in access_events:
            emp = employees.get(ev.get("employee_id"))
            if emp and emp.get("status") == "SUSPENDED":
                findings.append({
                    "rule": "R09",
                    "name": "Employee-Account Relationship Anomaly",
                    "score": 40,
                    "target": ev["employee_id"],
                    "description": f"Suspended employee {emp['name']} recorded interaction on account {ev['account_id']}.",
                    "employee_id": ev["employee_id"],
                    "account_id": ev["account_id"]
                })
        return findings

    # -------------------------------------------------------------
    # R10: Unusual Timing
    # -------------------------------------------------------------
    def check_r10_unusual_timing(self, txns: List[Dict[str, Any]], acc_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        for t in txns:
            dt = self.parse_dt(t["timestamp"])
            if dt.hour >= 23 or dt.hour <= 5:
                findings.append({
                    "rule": "R10",
                    "name": "Unusual Timing",
                    "score": 10,
                    "target": t["transaction_id"],
                    "description": f"Nocturnal transfer executed at {dt.strftime('%H:%M:%S')} (outside standard banking operations window).",
                    "transaction_id": t["transaction_id"]
                })
        return findings

    # -------------------------------------------------------------
    # Master Evaluation
    # -------------------------------------------------------------
    def run_all_checks(self) -> Dict[str, Any]:
        txns = data_store.get_all_transactions()
        prvs = list(data_store.privilege_changes.values())
        acc_events = list(data_store.access_events.values())
        prof_changes = list(data_store.profile_changes.values())
        accounts = data_store.accounts
        employees = data_store.employees

        r01 = self.check_r01_large_transaction(txns)
        r02 = self.check_r02_splitting(txns)
        r03 = self.check_r03_circular_transfer(txns)
        r04 = self.check_r04_rapid_transfer_chain(txns)
        r05 = self.check_r05_privilege_escalation(prvs)
        r06 = self.check_r06_unusual_access(acc_events)
        r07 = self.check_r07_profile_change_before_txn(prof_changes, txns, accounts)
        r08 = self.check_r08_dormant_activation(txns, accounts)
        r09 = self.check_r09_relationship_anomaly(employees, acc_events)
        r10 = self.check_r10_unusual_timing(txns, acc_events)

        total_rules = 10
        total_findings = len(r01) + len(r02) + len(r03) + len(r04) + len(r05) + len(r06) + len(r07) + len(r08) + len(r09) + len(r10)

        return {
            "status": "COMPLETED",
            "evaluated_at": "2026-10-27T11:45:00",
            "total_rules": total_rules,
            "total_findings": total_findings,
            "rules_breakdown": {
                "R01_LargeTransaction": len(r01),
                "R02_TransactionSplitting": len(r02),
                "R03_CircularTransfer": len(r03),
                "R04_RapidTransferChain": len(r04),
                "R05_PrivilegeEscalation": len(r05),
                "R06_UnusualAccess": len(r06),
                "R07_ProfileChangeBeforeTxn": len(r07),
                "R08_DormantAccountActivation": len(r08),
                "R09_RelationshipAnomaly": len(r09),
                "R10_UnusualTiming": len(r10)
            },
            "findings": {
                "R01": r01,
                "R02": r02,
                "R03": r03,
                "R04": r04,
                "R05": r05,
                "R06": r06,
                "R07": r07,
                "R08": r08,
                "R09": r09,
                "R10": r10
            }
        }

detection_engine = DetectionEngine()
