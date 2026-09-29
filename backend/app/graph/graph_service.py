"""
TRACE Intelligence Platform - Graph Service
Builds and traverses entity relationship graphs:
- Employee HAS_PRIVILEGE Privilege
- Employee ACCESSED Account
- Employee MODIFIED Customer
- Customer OWNS Account
- Account TRANSFERRED_TO Account
Supports multi-hop neighborhood expansion (1-hop, 2-hop, 3-hop) and evidence linking.
"""

from typing import List, Dict, Any, Set, Optional
from collections import deque
from app.schemas import GraphNode, GraphEdge, GraphData
from app.services.data_store import data_store

class GraphService:
    def build_full_graph(self) -> GraphData:
        nodes: Dict[str, GraphNode] = {}
        edges: Dict[str, GraphEdge] = {}

        # 1. Employees
        for emp in data_store.get_all_employees():
            eid = emp["employee_id"]
            risk = "HIGH" if eid == "EMP007" else ("MEDIUM" if emp.get("status") == "SUSPENDED" else "NORMAL")
            nodes[eid] = GraphNode(
                id=eid,
                label=emp["name"],
                entity_type="EMPLOYEE",
                risk_level=risk,
                subtitle=f"{emp['role']} | L{emp['privilege_level']}",
                properties=emp
            )

        # 2. Customers
        for cust in data_store.get_all_customers():
            cid = cust["customer_id"]
            nodes[cid] = GraphNode(
                id=cid,
                label=cust["name"],
                entity_type="CUSTOMER",
                risk_level=cust.get("risk_level", "NORMAL"),
                subtitle=cust.get("segment", "Customer"),
                properties=cust
            )

        # 3. Accounts
        for acc in data_store.get_all_accounts():
            aid = acc["account_id"]
            # Highlight target demo accounts
            is_demo = aid in ["ACC-9011", "ACC-9042", "ACC-9088"]
            nodes[aid] = GraphNode(
                id=aid,
                label=acc.get("label") or aid,
                entity_type="ACCOUNT",
                risk_level="HIGH" if is_demo else ("MEDIUM" if acc.get("status") == "RESTRICTED" else "NORMAL"),
                subtitle=f"₹{acc.get('balance', 0):,.0f} | {acc.get('account_type', '')}",
                properties=acc
            )

            # Customer OWNS Account edge
            cid = acc.get("customer_id")
            if cid and cid in nodes:
                edge_id = f"OWNS-{cid}-{aid}"
                edges[edge_id] = GraphEdge(
                    id=edge_id,
                    source=cid,
                    target=aid,
                    relationship="OWNS",
                    label="OWNS",
                    is_suspicious=False,
                    properties={"status": acc.get("status")}
                )

        # 4. Privilege Changes -> HAS_PRIVILEGE
        for prv in data_store.privilege_changes.values():
            emp_id = prv["employee_id"]
            prv_node_id = f"PRV-NODE-{prv['change_id']}"
            if prv_node_id not in nodes:
                nodes[prv_node_id] = GraphNode(
                    id=prv_node_id,
                    label=prv["privilege_name"].replace("_", " "),
                    entity_type="PRIVILEGE",
                    risk_level="HIGH" if prv.get("is_suspicious") else "NORMAL",
                    subtitle=f"Level {prv['new_level']} | Granted {prv['granted_at'].split('T')[1]}",
                    properties=prv
                )
            if emp_id in nodes:
                edge_id = f"EDGE-{prv['change_id']}"
                edges[edge_id] = GraphEdge(
                    id=edge_id,
                    source=emp_id,
                    target=prv_node_id,
                    relationship="HAS_PRIVILEGE",
                    label="ESCALATED TO" if prv.get("is_suspicious") else "GRANTED",
                    is_suspicious=prv.get("is_suspicious", False),
                    evidence_id="E001" if prv["change_id"] == "PRV-801" else None,
                    timestamp=prv["granted_at"],
                    properties=prv
                )

        # 5. Access Events -> ACCESSED
        for ev in data_store.access_events.values():
            emp_id = ev["employee_id"]
            acc_id = ev["account_id"]
            if emp_id in nodes and acc_id in nodes:
                edge_id = f"EDGE-{ev['access_id']}"
                edges[edge_id] = GraphEdge(
                    id=edge_id,
                    source=emp_id,
                    target=acc_id,
                    relationship="ACCESSED",
                    label=ev["action"].replace("_", " "),
                    is_suspicious=ev.get("is_suspicious", False),
                    evidence_id="E002" if ev["access_id"] == "ACC-EV-5001" else None,
                    timestamp=ev["timestamp"],
                    properties=ev
                )

        # 6. Profile Changes -> MODIFIED
        for pc in data_store.profile_changes.values():
            emp_id = pc["employee_id"]
            cust_id = pc["customer_id"]
            if emp_id in nodes and cust_id in nodes:
                edge_id = f"EDGE-{pc['change_id']}"
                edges[edge_id] = GraphEdge(
                    id=edge_id,
                    source=emp_id,
                    target=cust_id,
                    relationship="MODIFIED",
                    label=f"MODIFIED ({pc['field_changed']})",
                    is_suspicious=pc.get("is_suspicious", False),
                    evidence_id="E003" if pc["change_id"] == "CHG-301" else None,
                    timestamp=pc["timestamp"],
                    properties=pc
                )

        # 7. Transactions -> TRANSFERRED_TO
        # Include all suspicious txns + sample of baseline txns to avoid graph clutter
        for txn in data_store.get_all_transactions():
            src = txn["source_account"]
            dst = txn["destination_account"]
            if src in nodes and dst in nodes:
                # Always add suspicious; add normal only if both endpoints exist and max 40 normal
                if txn.get("is_suspicious") or len(edges) < 80:
                    edge_id = f"TXN-EDGE-{txn['transaction_id']}"
                    ev_id = None
                    if txn["transaction_id"] == "TXN-CIRC-001":
                        ev_id = "E004"
                    elif txn["transaction_id"] == "TXN-CIRC-002":
                        ev_id = "E005"
                    elif txn["transaction_id"] == "TXN-CIRC-003":
                        ev_id = "E006"
                    elif txn["transaction_id"] == "TXN-DORM-001":
                        ev_id = "E008"

                    edges[edge_id] = GraphEdge(
                        id=edge_id,
                        source=src,
                        target=dst,
                        relationship="TRANSFERRED_TO",
                        label=f"₹{txn['amount']:,.0f}",
                        amount=txn["amount"],
                        timestamp=txn["timestamp"],
                        is_suspicious=txn.get("is_suspicious", False),
                        evidence_id=ev_id,
                        properties=txn
                    )

        return GraphData(nodes=list(nodes.values()), edges=list(edges.values()))

    def get_subgraph(
        self,
        center_id: str,
        hops: int = 2,
        entity_types: Optional[List[str]] = None,
        only_suspicious: bool = False
    ) -> GraphData:
        full_graph = self.build_full_graph()
        node_map = {n.id: n for n in full_graph.nodes}
        edge_map = {e.id: e for e in full_graph.edges}

        # Build adjacency
        adj: Dict[str, Set[str]] = {}
        for edge in full_graph.edges:
            adj.setdefault(edge.source, set()).add(edge.target)
            adj.setdefault(edge.target, set()).add(edge.source)

        if center_id not in node_map:
            # If center_id is an alert, pick its related employee or first related account
            alert = data_store.get_alert(center_id)
            if alert:
                center_id = alert.get("related_employee") or (alert.get("related_accounts", [None])[0])
            if not center_id or center_id not in node_map:
                center_id = "EMP007"  # Default fallback to primary demo entity

        # BFS expansion up to 'hops'
        visited_nodes: Set[str] = {center_id}
        queue = deque([(center_id, 0)])

        while queue:
            curr, dist = queue.popleft()
            if dist < hops:
                for neighbor in adj.get(curr, set()):
                    if neighbor not in visited_nodes:
                        visited_nodes.add(neighbor)
                        queue.append((neighbor, dist + 1))

        # Filter nodes by entity type if specified
        filtered_nodes = []
        for nid in visited_nodes:
            n = node_map.get(nid)
            if n:
                if entity_types and n.entity_type not in entity_types:
                    continue
                filtered_nodes.append(n)

        filtered_node_ids = {n.id for n in filtered_nodes}

        # Filter edges between selected nodes
        filtered_edges = []
        for edge in full_graph.edges:
            if edge.source in filtered_node_ids and edge.target in filtered_node_ids:
                if only_suspicious and not edge.is_suspicious:
                    continue
                filtered_edges.append(edge)

        return GraphData(nodes=filtered_nodes, edges=filtered_edges)

    def get_alert_investigation_graph(self, alert_id: str) -> GraphData:
        """Returns the specific focused subgraph for an alert investigation."""
        alert = data_store.get_alert(alert_id)
        if not alert:
            return self.get_subgraph("EMP007", hops=2)

        # For the premier alert ALT-10482, build the exact high-fidelity circular flow subgraph
        if alert_id == "ALT-10482":
            sub = self.get_subgraph("EMP007", hops=3)
            # Ensure the circular nodes and edges are strictly present
            critical_ids = {"EMP007", "ACC-9011", "ACC-9042", "ACC-9088", "CUST-401", "CUST-402", "CUST-403", "PRV-NODE-PRV-801"}
            full_graph = self.build_full_graph()
            n_map = {n.id: n for n in full_graph.nodes}
            e_map = {e.id: e for e in full_graph.edges}

            res_nodes = {n.id: n for n in sub.nodes}
            for cid in critical_ids:
                if cid in n_map:
                    res_nodes[cid] = n_map[cid]

            res_edges = {e.id: e for e in sub.edges}
            for e in full_graph.edges:
                if e.source in res_nodes and e.target in res_nodes:
                    if e.is_suspicious or e.relationship in ["OWNS", "HAS_PRIVILEGE", "ACCESSED", "MODIFIED"]:
                        res_edges[e.id] = e

            return GraphData(nodes=list(res_nodes.values()), edges=list(res_edges.values()))

        # For other alerts, use related employee or accounts
        center = alert.get("related_employee") or (alert.get("related_accounts", [None])[0]) or "EMP007"
        return self.get_subgraph(center, hops=2)

graph_service = GraphService()
