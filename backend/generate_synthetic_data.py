"""
TRACE Financial Crime & Insider Risk Intelligence Platform
Synthetic Data Generator
Generates realistic, interconnected datasets for demonstration and detection engine.
"""

import json
import os
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Base Anchor Timestamp for the Suspicious Demo Scenario: 27 OCT 2026
BASE_DATE = datetime(2026, 10, 27, 9, 0, 0)

# ==========================================
# 1. EMPLOYEES (18 Employees)
# ==========================================
employees = [
    {
        "employee_id": "EMP007",
        "name": "Vikram Malhotra",
        "department": "Core Banking Operations",
        "role": "Senior Operations Analyst",
        "privilege_level": 4,  # Escalated from 2
        "status": "ACTIVE",
        "last_login": "2026-10-27T10:02:14",
        "email": "v.malhotra@zenith-bank.internal",
        "location": "Mumbai Operations Hub (Level 3)"
    },
    {
        "employee_id": "EMP001",
        "name": "Sarah Jenkins",
        "department": "Financial Crime & AML",
        "role": "Lead FinCrime Investigator",
        "privilege_level": 5,
        "status": "ACTIVE",
        "last_login": "2026-10-27T08:45:00",
        "email": "s.jenkins@zenith-bank.internal",
        "location": "London Risk Centre"
    },
    {
        "employee_id": "EMP002",
        "name": "Arjun Sharma",
        "department": "Core Banking Operations",
        "role": "Operations Manager",
        "privilege_level": 4,
        "status": "ACTIVE",
        "last_login": "2026-10-27T09:12:00",
        "email": "a.sharma@zenith-bank.internal",
        "location": "Mumbai Operations Hub (Level 3)"
    },
    {
        "employee_id": "EMP003",
        "name": "Elena Rostova",
        "department": "Security Operations",
        "role": "IAM Security Administrator",
        "privilege_level": 5,
        "status": "ACTIVE",
        "last_login": "2026-10-27T08:15:30",
        "email": "e.rostova@zenith-bank.internal",
        "location": "Frankfurt Security Operations"
    },
    {
        "employee_id": "EMP004",
        "name": "Devendra Rao",
        "department": "Private Wealth Management",
        "role": "Senior Portfolio Director",
        "privilege_level": 3,
        "status": "ACTIVE",
        "last_login": "2026-10-27T09:30:10",
        "email": "d.rao@zenith-bank.internal",
        "location": "Singapore Wealth Hub"
    },
    {
        "employee_id": "EMP005",
        "name": "Priya Nambiar",
        "department": "Retail Banking Services",
        "role": "Branch Relationship Officer",
        "privilege_level": 2,
        "status": "ACTIVE",
        "last_login": "2026-10-27T09:05:40",
        "email": "p.nambiar@zenith-bank.internal",
        "location": "Bangalore Commercial Branch"
    },
    {
        "employee_id": "EMP006",
        "name": "Michael Chang",
        "department": "Treasury & Clearing",
        "role": "Settlement Officer",
        "privilege_level": 3,
        "status": "ACTIVE",
        "last_login": "2026-10-27T07:55:00",
        "email": "m.chang@zenith-bank.internal",
        "location": "Hong Kong Clearing Centre"
    },
    {
        "employee_id": "EMP008",
        "name": "Ananya Joshi",
        "department": "Retail Banking Services",
        "role": "Customer Support Representative",
        "privilege_level": 1,
        "status": "ACTIVE",
        "last_login": "2026-10-27T08:50:22",
        "email": "a.joshi@zenith-bank.internal",
        "location": "Pune Support Centre"
    },
    {
        "employee_id": "EMP009",
        "name": "Rohan Mehra",
        "department": "Core Banking Operations",
        "role": "Junior Data Entry Specialist",
        "privilege_level": 1,
        "status": "ACTIVE",
        "last_login": "2026-10-27T09:10:15",
        "email": "r.mehra@zenith-bank.internal",
        "location": "Mumbai Operations Hub (Level 3)"
    },
    {
        "employee_id": "EMP010",
        "name": "Tara Sen",
        "department": "Financial Crime & AML",
        "role": "Senior AML Analyst",
        "privilege_level": 4,
        "status": "ACTIVE",
        "last_login": "2026-10-27T08:40:00",
        "email": "t.sen@zenith-bank.internal",
        "location": "London Risk Centre"
    },
    {
        "employee_id": "EMP011",
        "name": "Zainab Al-Mansoor",
        "department": "Trade Finance Operations",
        "role": "Letter of Credit Auditor",
        "privilege_level": 3,
        "status": "ACTIVE",
        "last_login": "2026-10-26T17:22:00",
        "email": "z.mansoor@zenith-bank.internal",
        "location": "Dubai Regional Centre"
    },
    {
        "employee_id": "EMP012",
        "name": "Karthik Varma",
        "department": "IT Infrastructure",
        "role": "Database Operations Engineer",
        "privilege_level": 4,
        "status": "ACTIVE",
        "last_login": "2026-10-27T06:30:00",
        "email": "k.varma@zenith-bank.internal",
        "location": "Hyderabad Tech Centre"
    },
    {
        "employee_id": "EMP013",
        "name": "Samantha Ward",
        "department": "Compliance & Audit",
        "role": "Internal Audit Specialist",
        "privilege_level": 3,
        "status": "ACTIVE",
        "last_login": "2026-10-27T09:15:00",
        "email": "s.ward@zenith-bank.internal",
        "location": "London Risk Centre"
    },
    {
        "employee_id": "EMP014",
        "name": "Kabir Das",
        "department": "Core Banking Operations",
        "role": "Wire Transfer Operator",
        "privilege_level": 2,
        "status": "ACTIVE",
        "last_login": "2026-10-27T08:00:10",
        "email": "k.das@zenith-bank.internal",
        "location": "Mumbai Operations Hub (Level 3)"
    },
    {
        "employee_id": "EMP015",
        "name": "Amina Touré",
        "department": "Global Client Onboarding",
        "role": "KYC Specialist",
        "privilege_level": 2,
        "status": "ACTIVE",
        "last_login": "2026-10-27T09:45:00",
        "email": "a.toure@zenith-bank.internal",
        "location": "Paris Office"
    },
    {
        "employee_id": "EMP016",
        "name": "Nikhil Agarwal",
        "department": "Retail Banking Services",
        "role": "Branch Assistant",
        "privilege_level": 1,
        "status": "SUSPENDED",
        "last_login": "2026-10-24T14:10:00",
        "email": "n.agarwal@zenith-bank.internal",
        "location": "Delhi Branch"
    },
    {
        "employee_id": "EMP017",
        "name": "David Meyer",
        "department": "Cyber Threat Intelligence",
        "role": "Threat Hunting Lead",
        "privilege_level": 4,
        "status": "ACTIVE",
        "last_login": "2026-10-27T07:00:00",
        "email": "d.meyer@zenith-bank.internal",
        "location": "Frankfurt Security Operations"
    },
    {
        "employee_id": "EMP018",
        "name": "Siddharth Menon",
        "department": "Private Wealth Management",
        "role": "Private Banker",
        "privilege_level": 3,
        "status": "ACTIVE",
        "last_login": "2026-10-27T09:20:00",
        "email": "s.menon@zenith-bank.internal",
        "location": "Mumbai Operations Hub (Level 3)"
    }
]

# ==========================================
# 2. CUSTOMERS (36 Customers)
# ==========================================
customers = [
    # Demo Key Characters
    {
        "customer_id": "CUST-401",
        "name": "Aarav Singhania",
        "risk_level": "HIGH",
        "account_ids": ["ACC-9011", "ACC-9012"],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Ultra High Net Worth",
        "residence": "Worli, Mumbai",
        "phone": "+91 98200 11099" # Changed at 10:21 by EMP007
    },
    {
        "customer_id": "CUST-402",
        "name": "Maya Overseas & Export Ltd",
        "risk_level": "HIGH",
        "account_ids": ["ACC-9042"],
        "status": "ACTIVE",
        "kyc_status": "FLAGGED",
        "segment": "Commercial Trade",
        "residence": "Andheri East, Mumbai",
        "phone": "+91 98112 40019"
    },
    {
        "customer_id": "CUST-403",
        "name": "Kavita Patel",
        "risk_level": "HIGH",
        "account_ids": ["ACC-9088"],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Retail Business",
        "residence": "Bandra West, Mumbai",
        "phone": "+91 98334 77201"
    },
    # Secondary scenario customers
    {
        "customer_id": "CUST-404",
        "name": "Apex Holdings Pte Ltd",
        "risk_level": "MEDIUM",
        "account_ids": ["ACC-9101", "ACC-9102"],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Institutional Holding",
        "residence": "Singapore",
        "phone": "+65 6712 8890"
    },
    {
        "customer_id": "CUST-405",
        "name": "Dormant Trust B-11",
        "risk_level": "HIGH",
        "account_ids": ["ACC-9105"],
        "status": "RESTRICTED",
        "kyc_status": "EXPIRED",
        "segment": "Legacy Trust",
        "residence": "Geneva, Switzerland",
        "phone": "+41 22 819 0044"
    },
    {
        "customer_id": "CUST-406",
        "name": "Crestline Logistics",
        "risk_level": "MEDIUM",
        "account_ids": ["ACC-9109"],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Commercial Fleet",
        "residence": "Navi Mumbai",
        "phone": "+91 98221 44500"
    },
    {
        "customer_id": "CUST-407",
        "name": "Sunita Rao",
        "risk_level": "LOW",
        "account_ids": ["ACC-9112"],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Retail Premier",
        "residence": "Bengaluru",
        "phone": "+91 98440 22341"
    },
    {
        "customer_id": "CUST-408",
        "name": "Rajeshwari Iyer",
        "risk_level": "LOW",
        "account_ids": ["ACC-9115"],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Salaried Professional",
        "residence": "Chennai",
        "phone": "+91 94441 55620"
    },
    {
        "customer_id": "CUST-409",
        "name": "Blue Horizon Commodities",
        "risk_level": "HIGH",
        "account_ids": ["ACC-9120", "ACC-9121"],
        "status": "ACTIVE",
        "kyc_status": "ENHANCED_DUE_DILIGENCE",
        "segment": "Commodities Broking",
        "residence": "Dubai",
        "phone": "+971 4 332 9981"
    },
    {
        "customer_id": "CUST-410",
        "name": "Tariq Mansoor",
        "risk_level": "MEDIUM",
        "account_ids": ["ACC-9125"],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Commercial Real Estate",
        "residence": "Abu Dhabi",
        "phone": "+971 2 445 1120"
    }
]

# Add more synthetic customers (411 - 435) to reach 35 customers
first_names = ["Aditya", "Neha", "Rahul", "Meera", "Sanjay", "Anil", "Deepa", "Sameer", "Ritu", "Gaurav", 
               "Swati", "Karan", "Pooja", "Varun", "Shruti", "Tarun", "Divya", "Manish", "Bhavna", "Alok",
               "Pallavi", "Naveen", "Ishaan", "Rhea", "Harish"]
last_names = ["Kulkarni", "Deshmukh", "Nair", "Reddy", "Chatterjee", "Bose", "Menon", "Kapoor", "Bhatia", "Chauhan",
              "Mukherjee", "Saxena", "Chawla", "Trivedi", "Pandey", "Dutta", "Nigam", "Mehta", "Bansal", "Goel",
              "Srivastava", "Sen", "Pillai", "Goswami", "Vaidya"]

for i in range(25):
    cid = f"CUST-{411 + i}"
    acc_id = f"ACC-{9130 + i}"
    fname = first_names[i % len(first_names)]
    lname = last_names[i % len(last_names)]
    customers.append({
        "customer_id": cid,
        "name": f"{fname} {lname}",
        "risk_level": "LOW" if i % 4 != 0 else ("MEDIUM" if i % 8 != 0 else "HIGH"),
        "account_ids": [acc_id],
        "status": "ACTIVE",
        "kyc_status": "VERIFIED",
        "segment": "Retail Standard",
        "residence": f"Sector {i+1}, Metropolitan Region",
        "phone": f"+91 98{i:02d}0 {10000 + i*137}"
    })

# ==========================================
# 3. ACCOUNTS (50 Accounts)
# ==========================================
accounts = [
    # Demo Key Accounts
    {
        "account_id": "ACC-9011",
        "customer_id": "CUST-401",
        "account_type": "Private Wealth Current",
        "balance": 18450000.0,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2022-04-15",
        "branch": "Nariman Point Wealth Branch",
        "label": "Account A (Singhania Core)"
    },
    {
        "account_id": "ACC-9012",
        "customer_id": "CUST-401",
        "account_type": "Fixed Escrow",
        "balance": 5200000.0,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2023-01-10",
        "branch": "Nariman Point Wealth Branch",
        "label": "Account A-2 (Singhania Escrow)"
    },
    {
        "account_id": "ACC-9042",
        "customer_id": "CUST-402",
        "account_type": "Commercial Current",
        "balance": 820000.0,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2025-08-19",
        "branch": "Andheri SME Branch",
        "label": "Account B (Maya Overseas Shell)"
    },
    {
        "account_id": "ACC-9088",
        "customer_id": "CUST-403",
        "account_type": "Savings Premier",
        "balance": 430000.0,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2024-11-02",
        "branch": "Bandra Retail Branch",
        "label": "Account C (Kavita Patel Conduit)"
    },
    {
        "account_id": "ACC-9101",
        "customer_id": "CUST-404",
        "account_type": "Corporate Multi-Currency",
        "balance": 9400000.0,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2021-06-20",
        "branch": "International Banking Unit",
        "label": "Apex Holdings Core"
    },
    {
        "account_id": "ACC-9105",
        "customer_id": "CUST-405",
        "account_type": "Dormant Trust",
        "balance": 7500000.0,
        "currency": "INR",
        "status": "RESTRICTED",
        "opened_date": "2018-03-12",
        "branch": "Geneva Wealth Desk",
        "label": "Legacy Dormant Trust B-11"
    },
    {
        "account_id": "ACC-9109",
        "customer_id": "CUST-406",
        "account_type": "Commercial Fleet Operational",
        "balance": 1450000.0,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2023-09-01",
        "branch": "Navi Mumbai Commercial",
        "label": "Crestline Operational"
    },
    {
        "account_id": "ACC-9120",
        "customer_id": "CUST-409",
        "account_type": "Trade Clearing Escrow",
        "balance": 12800000.0,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2022-12-14",
        "branch": "Dubai Branch Unit",
        "label": "Blue Horizon Escrow"
    }
]

# Generate rest of accounts matching the 25 auto-generated customers plus extra accounts
for i in range(25):
    cid = f"CUST-{411 + i}"
    acc_id = f"ACC-{9130 + i}"
    accounts.append({
        "account_id": acc_id,
        "customer_id": cid,
        "account_type": "Savings Classic" if i % 2 == 0 else "Current Business",
        "balance": round(random.uniform(50000, 2500000), 2),
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": (datetime(2023, 1, 1) + timedelta(days=i*45)).strftime("%Y-%m-%d"),
        "branch": "Metropolitan Central Hub",
        "label": f"Standard Retail {acc_id}"
    })

# Add 10 additional accounts for realistic transaction counter-parties
extra_accs = [
    ("ACC-9181", "CUST-401", "Investment Liquidity Account", 4200000.0),
    ("ACC-9182", "CUST-402", "Export Factoring Sub-Account", 150000.0),
    ("ACC-9183", "CUST-404", "Treasury Liquidity Reserve", 28000000.0),
    ("ACC-9184", "CUST-409", "Foreign Exchange Spot Pool", 19500000.0),
    ("ACC-9185", "CUST-411", "Personal Recurring Deposit", 340000.0),
    ("ACC-9186", "CUST-414", "Emergency Liquid Fund", 890000.0),
    ("ACC-9187", "CUST-418", "Term Deposit Account", 1250000.0),
    ("ACC-9188", "CUST-422", "High-Yield Savings", 670000.0),
    ("ACC-9189", "CUST-425", "Overdraft Facility Account", 2200000.0),
    ("ACC-9190", "CUST-430", "Digital Wallets Holding Pool", 450000.0)
]
for acc_id, cid, atype, bal in extra_accs:
    accounts.append({
        "account_id": acc_id,
        "customer_id": cid,
        "account_type": atype,
        "balance": bal,
        "currency": "INR",
        "status": "ACTIVE",
        "opened_date": "2024-02-18",
        "branch": "Metropolitan Central Hub",
        "label": f"{atype} ({acc_id})"
    })

# ==========================================
# 4. PRIVILEGE CHANGES & ROLES
# ==========================================
privilege_changes = [
    # Key Scenario: EMP007 escalation at 10:05
    {
        "change_id": "PRV-801",
        "employee_id": "EMP007",
        "previous_level": 2,
        "new_level": 4,
        "privilege_name": "TIER_4_DIRECT_OVERRIDE_AND_LEDGER_MUTATION",
        "granted_at": "2026-10-27T10:05:00",
        "granted_by": "SYSTEM_EMERGENCY_OVERRIDE_BYPASS",
        "approval_ticket": "SEC-TICKET-99214-UNAUTH",
        "reason": "Emergency Batch Settlement (Unverified Claim)",
        "ip_address": "10.14.88.107 (Mumbai Ops Level 3)",
        "is_suspicious": True
    },
    # Routine privilege grants
    {
        "change_id": "PRV-782",
        "employee_id": "EMP002",
        "previous_level": 3,
        "new_level": 4,
        "privilege_name": "OPERATIONS_SUPERVISOR_SIGN_OFF",
        "granted_at": "2026-10-20T14:30:00",
        "granted_by": "EMP003",
        "approval_ticket": "IAM-2026-8941",
        "reason": "Scheduled Annual Role Elevation",
        "ip_address": "10.14.88.12",
        "is_suspicious": False
    },
    {
        "change_id": "PRV-771",
        "employee_id": "EMP014",
        "previous_level": 1,
        "new_level": 2,
        "privilege_name": "DOMESTIC_RTGS_OPERATOR",
        "granted_at": "2026-10-15T11:00:00",
        "granted_by": "EMP002",
        "approval_ticket": "IAM-2026-8712",
        "reason": "Operational Roster Rotation",
        "ip_address": "10.14.88.55",
        "is_suspicious": False
    },
    {
        "change_id": "PRV-765",
        "employee_id": "EMP010",
        "previous_level": 3,
        "new_level": 4,
        "privilege_name": "AML_CASE_DISMISSAL_AND_SAR_FILING",
        "granted_at": "2026-10-10T09:20:00",
        "granted_by": "EMP001",
        "approval_ticket": "IAM-2026-8430",
        "reason": "Promotion to Senior AML Specialist",
        "ip_address": "10.20.12.44",
        "is_suspicious": False
    },
    {
        "change_id": "PRV-752",
        "employee_id": "EMP005",
        "previous_level": 1,
        "new_level": 2,
        "privilege_name": "RETAIL_KYC_DOC_VERIFICATION",
        "granted_at": "2026-10-02T16:15:00",
        "granted_by": "EMP002",
        "approval_ticket": "IAM-2026-8109",
        "reason": "Branch Support Expansion",
        "ip_address": "10.16.4.19",
        "is_suspicious": False
    }
]

# ==========================================
# 5. ACCESS EVENTS
# ==========================================
access_events = [
    # Key Scenario: EMP007 accesses Account A (ACC-9011) at 10:17
    {
        "access_id": "ACC-EV-5001",
        "employee_id": "EMP007",
        "account_id": "ACC-9011",
        "timestamp": "2026-10-27T10:17:42",
        "action": "DEEP_LEDGER_QUERY_AND_NOTIFICATION_BYPASS",
        "device_id": "WS-MUM-OPS-074",
        "session_id": "SESS-90021-AUTH-BYPASS",
        "ip_address": "10.14.88.107",
        "is_suspicious": True,
        "anomaly_reason": "Employee never previously accessed Private Wealth portfolio; outside geographic and departmental tier."
    },
    # EMP007 also queried ACC-9042 and ACC-9088 to verify conduit readiness
    {
        "access_id": "ACC-EV-5002",
        "employee_id": "EMP007",
        "account_id": "ACC-9042",
        "timestamp": "2026-10-27T10:19:15",
        "action": "ACCOUNT_STATUS_VERIFICATION",
        "device_id": "WS-MUM-OPS-074",
        "session_id": "SESS-90021-AUTH-BYPASS",
        "ip_address": "10.14.88.107",
        "is_suspicious": True,
        "anomaly_reason": "Queried dormant commercial conduit account within 2 minutes of accessing Account A."
    },
    {
        "access_id": "ACC-EV-5003",
        "employee_id": "EMP007",
        "account_id": "ACC-9088",
        "timestamp": "2026-10-27T10:20:05",
        "action": "ACCOUNT_STATUS_VERIFICATION",
        "device_id": "WS-MUM-OPS-074",
        "session_id": "SESS-90021-AUTH-BYPASS",
        "ip_address": "10.14.88.107",
        "is_suspicious": True,
        "anomaly_reason": "Sequential reconnaissance across destination holding accounts."
    },
    # Secondary suspicious access: EMP012 accessing dormant trust
    {
        "access_id": "ACC-EV-5010",
        "employee_id": "EMP012",
        "account_id": "ACC-9105",
        "timestamp": "2026-10-26T23:42:10",
        "action": "DIRECT_DATABASE_SCHEMA_READ",
        "device_id": "SRV-HYD-DB-02",
        "session_id": "SESS-DBA-9912",
        "ip_address": "10.18.99.2",
        "is_suspicious": True,
        "anomaly_reason": "After-hours direct database query on dormant high-value entity."
    }
]

# Add routine employee access events
routine_actions = ["VIEW_BALANCE", "CUSTOMER_SERVICE_QUERY", "STATEMENT_GENERATION", "STANDARD_KYC_CHECK", "ADDRESS_VERIFICATION_READ"]
for i in range(35):
    emp = employees[i % len(employees)]
    acc = accounts[i % len(accounts)]
    h = 9 + (i % 8)
    m = (i * 7) % 60
    access_events.append({
        "access_id": f"ACC-EV-50{20 + i}",
        "employee_id": emp["employee_id"],
        "account_id": acc["account_id"],
        "timestamp": f"2026-10-27T{h:02d}:{m:02d}:{random.randint(10, 59)}",
        "action": routine_actions[i % len(routine_actions)],
        "device_id": f"WS-BRN-{100 + i}",
        "session_id": f"SESS-REG-{4000 + i}",
        "ip_address": f"10.14.{(i*3)%100}.{10 + (i%50)}",
        "is_suspicious": False,
        "anomaly_reason": None
    })

# ==========================================
# 6. PROFILE CHANGES
# ==========================================
profile_changes = [
    # Key Scenario: Customer profile modification at 10:21 by EMP007
    {
        "change_id": "CHG-301",
        "employee_id": "EMP007",
        "customer_id": "CUST-401",
        "timestamp": "2026-10-27T10:21:30",
        "field_changed": "PRIMARY_CONTACT_PHONE_AND_2FA_DISPATCH",
        "old_value": "+91 98200 99410 (Aarav Singhania Private Line)",
        "new_value": "+91 98200 11099 (Burner SIM registered 24h ago)",
        "channel": "INTERNAL_ADMIN_CONSOLE_DIRECT",
        "supervisor_override": "BYPASS_TOKEN_EMERGENCY",
        "is_suspicious": True,
        "reason": "Client travel notification bypass override (falsified)"
    },
    {
        "change_id": "CHG-302",
        "employee_id": "EMP007",
        "customer_id": "CUST-401",
        "timestamp": "2026-10-27T10:23:05",
        "field_changed": "OUTBOUND_TRANSACTION_LIMIT_PER_DAY",
        "old_value": "INR 1,00,000",
        "new_value": "INR 50,00,000",
        "channel": "INTERNAL_ADMIN_CONSOLE_DIRECT",
        "supervisor_override": "BYPASS_TOKEN_EMERGENCY",
        "is_suspicious": True,
        "reason": "Ad-hoc limit surge without compliance risk questionnaire"
    },
    # Secondary suspicious profile modification: Dormant trust KYC bypass
    {
        "change_id": "CHG-305",
        "employee_id": "EMP012",
        "customer_id": "CUST-405",
        "timestamp": "2026-10-26T23:55:00",
        "field_changed": "KYC_EXPIRY_DATE",
        "old_value": "2024-03-31",
        "new_value": "2028-12-31",
        "channel": "DIRECT_DB_MUTATION",
        "supervisor_override": "NONE",
        "is_suspicious": True,
        "reason": "Direct SQL alteration bypassing front-office audit controls"
    },
    # Routine profile changes
    {
        "change_id": "CHG-288",
        "employee_id": "EMP005",
        "customer_id": "CUST-407",
        "timestamp": "2026-10-25T11:20:00",
        "field_changed": "MAILING_ADDRESS",
        "old_value": "Flat 4, Lavelle Road, Bengaluru",
        "new_value": "Penthouse 12, Indiranagar, Bengaluru",
        "channel": "BRANCH_CUSTOMER_REQUEST",
        "supervisor_override": "EMP002",
        "is_suspicious": False,
        "reason": "Customer relocation with lease agreement proof"
    },
    {
        "change_id": "CHG-281",
        "employee_id": "EMP015",
        "customer_id": "CUST-408",
        "timestamp": "2026-10-22T14:40:00",
        "field_changed": "NOMINEE_NAME",
        "old_value": "None Listed",
        "new_value": "Suresh Iyer (Spouse)",
        "channel": "NET_BANKING_PORTAL",
        "supervisor_override": "AUTOMATED_OTP_VERIFIED",
        "is_suspicious": False,
        "reason": "Nomination form submission"
    }
]

# ==========================================
# 7. TRANSACTIONS (~150 Transactions)
# ==========================================
transactions = []

# --- Key Demo Scenario: The Circular Transfer Loop ---
# 10:27  ₹4.6L transferred A → B
# 10:31  ₹4.2L transferred B → C
# 10:38  ₹4.0L transferred C → A
transactions.append({
    "transaction_id": "TXN-CIRC-001",
    "source_account": "ACC-9011",
    "destination_account": "ACC-9042",
    "amount": 460000.0,
    "currency": "INR",
    "timestamp": "2026-10-27T10:27:14",
    "transaction_type": "IMMEDIATE_SETTLEMENT_RTGS",
    "status": "COMPLETED",
    "reference": "CONSULTING_ADVANCE_INV_908",
    "channel": "INTERNAL_OPERATIONS_OVERRIDE",
    "initiated_by_employee": "EMP007",
    "is_suspicious": True,
    "scenario_tag": "CIRCULAR_FLOW_LEG_1"
})

transactions.append({
    "transaction_id": "TXN-CIRC-002",
    "source_account": "ACC-9042",
    "destination_account": "ACC-9088",
    "amount": 420000.0,
    "currency": "INR",
    "timestamp": "2026-10-27T10:31:48",
    "transaction_type": "IMMEDIATE_SETTLEMENT_IMPS",
    "status": "COMPLETED",
    "reference": "SUPPLY_CHAIN_VENDOR_DISBURSEMENT",
    "channel": "INTERNAL_OPERATIONS_OVERRIDE",
    "initiated_by_employee": "EMP007",
    "is_suspicious": True,
    "scenario_tag": "CIRCULAR_FLOW_LEG_2"
})

transactions.append({
    "transaction_id": "TXN-CIRC-003",
    "source_account": "ACC-9088",
    "destination_account": "ACC-9011",
    "amount": 400000.0,
    "currency": "INR",
    "timestamp": "2026-10-27T10:38:22",
    "transaction_type": "IMMEDIATE_SETTLEMENT_RTGS",
    "status": "COMPLETED",
    "reference": "LOAN_REFUND_RETURN_LEG",
    "channel": "INTERNAL_OPERATIONS_OVERRIDE",
    "initiated_by_employee": "EMP007",
    "is_suspicious": True,
    "scenario_tag": "CIRCULAR_FLOW_LEG_3"
})

# --- Scenario 2: Structured Splitting / Smurfing on ACC-9120 ---
for idx, (min_offset, amt) in enumerate([(2, 95000), (5, 98000), (8, 92000), (12, 99500), (16, 94000)]):
    transactions.append({
        "transaction_id": f"TXN-SPLIT-{idx+1:03d}",
        "source_account": "ACC-9120",
        "destination_account": f"ACC-{9130 + idx}",
        "amount": float(amt),
        "currency": "INR",
        "timestamp": f"2026-10-27T07:{10 + min_offset:02d}:15",
        "transaction_type": "RAPID_NEFT_SPLIT",
        "status": "COMPLETED",
        "reference": f"RETAIL_REBATE_TRANCHE_{idx+1}",
        "channel": "API_BULK_GATEWAY",
        "initiated_by_employee": None,
        "is_suspicious": True,
        "scenario_tag": "STRUCTURING_SMURFING"
    })

# --- Scenario 3: Dormant Account Rapid Drainage ---
transactions.append({
    "transaction_id": "TXN-DORM-001",
    "source_account": "ACC-9105",
    "destination_account": "ACC-9101",
    "amount": 3500000.0,
    "currency": "INR",
    "timestamp": "2026-10-27T01:15:00",
    "transaction_type": "SWIFT_INTERNATIONAL_WIRE",
    "status": "COMPLETED",
    "reference": "OFFSHORE_CORRESPONDENT_CLEARING",
    "channel": "SWIFT_FIN_GATEWAY",
    "initiated_by_employee": "EMP012",
    "is_suspicious": True,
    "scenario_tag": "DORMANT_DRAIN"
})

# --- Baseline Normal Transactions (120+ transactions across 24-27 Oct) ---
txn_counter = 100
categories = [
    ("SALARY_DISBURSEMENT_OCT", 45000, 180000, "CORPORATE_PAYROLL"),
    ("SUPPLIER_INVOICE_SETTLEMENT", 120000, 750000, "COMMERCIAL_B2B"),
    ("UTILITY_MAINTENANCE_PAYMENT", 5000, 35000, "RETAIL_BILLER"),
    ("DIVIDEND_CREDIT_Q3", 25000, 150000, "EQUITY_CLEARING"),
    ("INTER-BRANCH_RECONCILIATION", 300000, 1200000, "TREASURY_TRANSFER"),
    ("RETAIL_ATM_WITHDRAWAL", 4000, 20000, "ATM_NETWORK"),
    ("ONLINE_MERCHANT_PURCHASE", 1200, 48000, "E_COMMERCE_GATEWAY")
]

for day in [24, 25, 26, 27]:
    for i in range(32):
        txn_counter += 1
        src = random.choice(accounts)["account_id"]
        dst = random.choice(accounts)["account_id"]
        while dst == src:
            dst = random.choice(accounts)["account_id"]
        
        cat_name, min_a, max_a, t_type = random.choice(categories)
        amount = round(random.uniform(min_a, max_a), 2)
        hour = random.randint(8, 19)
        minute = random.randint(0, 59)
        sec = random.randint(0, 59)

        transactions.append({
            "transaction_id": f"TXN-NORM-{txn_counter}",
            "source_account": src,
            "destination_account": dst,
            "amount": amount,
            "currency": "INR",
            "timestamp": f"2026-10-{day:02d}T{hour:02d}:{minute:02d}:{sec:02d}",
            "transaction_type": t_type,
            "status": "COMPLETED",
            "reference": f"{cat_name}_{random.randint(1000, 9999)}",
            "channel": "SYSTEM_AUTOMATED_BATCH",
            "initiated_by_employee": None,
            "is_suspicious": False,
            "scenario_tag": "BASELINE_NORMAL"
        })

# ==========================================
# 8. EVIDENCE ITEMS
# ==========================================
evidence = [
    {
        "evidence_id": "E001",
        "evidence_type": "IAM_PRIVILEGE_LOG",
        "source": "Active Directory & CyberArk PAM Vault",
        "timestamp": "2026-10-27T10:05:00",
        "description": "EMP007 (Vikram Malhotra) escalated to Tier 4 Admin Override via Emergency Token SEC-TICKET-99214-UNAUTH with zero secondary approval.",
        "related_entity": "EMP007",
        "related_event": "PRV-801",
        "hash_signature": "sha256:4a8f9c2d1b0e3e5a6f7d8c9b0a1c2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R05 — Privilege Escalation: Employee obtained high-level write authority immediately prior to ledger activities."
    },
    {
        "evidence_id": "E002",
        "evidence_type": "ACCESS_AUDIT_LOG",
        "source": "Core Banking API Gateway (Audit-Stream-3)",
        "timestamp": "2026-10-27T10:17:42",
        "description": "EMP007 performed deep record inspection of Account ACC-9011 (Aarav Singhania Private Wealth) from workstation WS-MUM-OPS-074 outside his portfolio assignment.",
        "related_entity": "ACC-9011",
        "related_event": "ACC-EV-5001",
        "hash_signature": "sha256:7b1e2c3d4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R06 — Unusual Access: Access pattern deviates 100% from employee 90-day baseline; zero legitimate customer interaction documented."
    },
    {
        "evidence_id": "E003",
        "evidence_type": "CUSTOMER_PROFILE_MUTATION",
        "source": "CRM Customer Master Journal",
        "timestamp": "2026-10-27T10:21:30",
        "description": "EMP007 altered CUST-401 primary telephone number to +91 98200 11099 and bypassed SMS/email transaction alerts under travel waiver pretence.",
        "related_entity": "CUST-401",
        "related_event": "CHG-301",
        "hash_signature": "sha256:9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R07 — Profile Change Before Transaction: Direct suppression of transaction alerts 6 minutes prior to large fund movement."
    },
    {
        "evidence_id": "E004",
        "evidence_type": "TRANSACTION_EVENT",
        "source": "RTGS Real-Time Settlement Engine",
        "timestamp": "2026-10-27T10:27:14",
        "description": "Outbound RTGS transfer of ₹4,60,000 from ACC-9011 to ACC-9042 (Maya Overseas). Initiated directly with EMP007 operator credential bypass.",
        "related_entity": "TXN-CIRC-001",
        "related_event": "TXN-CIRC-001",
        "hash_signature": "sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R01 — Large Transaction & R04 Rapid Transfer Chain: Abrupt high-value debit draining 25% of liquid balance."
    },
    {
        "evidence_id": "E005",
        "evidence_type": "TRANSACTION_EVENT",
        "source": "IMPS Switch Clearing Engine",
        "timestamp": "2026-10-27T10:31:48",
        "description": "Subsequent transfer of ₹4,20,000 from ACC-9042 to ACC-9088 (Kavita Patel). Occurred 4 minutes after credit arrival with minimal retention fee.",
        "related_entity": "TXN-CIRC-002",
        "related_event": "TXN-CIRC-002",
        "hash_signature": "sha256:2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R04 — Rapid Transfer Chain: Immediate pass-through hop characteristic of conduit/layering technique."
    },
    {
        "evidence_id": "E006",
        "evidence_type": "TRANSACTION_EVENT",
        "source": "RTGS Real-Time Settlement Engine",
        "timestamp": "2026-10-27T10:38:22",
        "description": "Closing transfer of ₹4,00,000 from ACC-9088 returning directly back to ACC-9011. Closed transaction cycle completed in 11 minutes total.",
        "related_entity": "TXN-CIRC-003",
        "related_event": "TXN-CIRC-003",
        "hash_signature": "sha256:3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R03 — Circular Transfer: A → B → C → A closed cycle confirming synthetic volume creation or money laundering loop."
    },
    {
        "evidence_id": "E007",
        "evidence_type": "DATABASE_QUERY_TELEMETRY",
        "source": "Oracle Database Firewall Audit",
        "timestamp": "2026-10-26T23:42:10",
        "description": "Direct SELECT query on dormant trust ACC-9105 balance by DBA credential EMP012 outside authorized change window.",
        "related_entity": "ACC-9105",
        "related_event": "ACC-EV-5010",
        "hash_signature": "sha256:8899aabbccddeeff00112233445566778899aabbccddeeff0011223344556677",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R08 — Dormant Account Activation & R10 Unusual Timing"
    },
    {
        "evidence_id": "E008",
        "evidence_type": "TRANSACTION_EVENT",
        "source": "SWIFT Alliance Gateway",
        "timestamp": "2026-10-27T01:15:00",
        "description": "Offshore SWIFT message MT103 transferring ₹35,00,000 from dormant account ACC-9105 to Singapore entity ACC-9101.",
        "related_entity": "TXN-DORM-001",
        "related_event": "TXN-DORM-001",
        "hash_signature": "sha256:aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899",
        "confidence": "VERIFIED_HIGH",
        "relationship_to_alert": "R08 — Dormant Account Liquidation"
    }
]

# ==========================================
# 9. ALERTS
# ==========================================
alerts = [
    {
        "alert_id": "ALT-10482",
        "alert_type": "INSIDER ACCESS / CIRCULAR FLOW",
        "risk_level": "HIGH",
        "risk_score": 95,
        "status": "OPEN",
        "created_at": "2026-10-27T10:40:00",
        "related_employee": "EMP007",
        "related_accounts": ["ACC-9011", "ACC-9042", "ACC-9088"],
        "related_customers": ["CUST-401", "CUST-402", "CUST-403"],
        "summary": "Correlated insider escalation followed by unauthorized account reconnaissance, alert contact suppression, and a ₹4.6L A → B → C → A circular money cycle in 11 minutes.",
        "risk_contributors": [
            {"name": "Unusual employee access", "score": 25, "evidence_id": "E002", "rule": "R06"},
            {"name": "Privilege escalation", "score": 20, "evidence_id": "E001", "rule": "R05"},
            {"name": "Large transaction", "score": 20, "evidence_id": "E004", "rule": "R01"},
            {"name": "Circular money flow", "score": 15, "evidence_id": "E006", "rule": "R03"},
            {"name": "Profile modification", "score": 10, "evidence_id": "E003", "rule": "R07"},
            {"name": "Rapid transfer chain", "score": 5, "evidence_id": "E005", "rule": "R04"}
        ],
        "evidence_ids": ["E001", "E002", "E003", "E004", "E005", "E006"]
    },
    {
        "alert_id": "ALT-10477",
        "alert_type": "UNUSUAL ACCOUNT ACCESS",
        "risk_level": "MEDIUM",
        "risk_score": 68,
        "status": "INVESTIGATING",
        "created_at": "2026-10-27T08:15:00",
        "related_employee": "EMP014",
        "related_accounts": ["ACC-9101"],
        "related_customers": ["CUST-404"],
        "summary": "Operator queried institutional multi-currency ledger without an open settlement ticket or client instruction.",
        "risk_contributors": [
            {"name": "Unusual employee access", "score": 35, "evidence_id": None, "rule": "R06"},
            {"name": "Employee-Account Relationship Anomaly", "score": 20, "evidence_id": None, "rule": "R09"},
            {"name": "Unusual timing", "score": 13, "evidence_id": None, "rule": "R10"}
        ],
        "evidence_ids": []
    },
    {
        "alert_id": "ALT-10461",
        "alert_type": "RAPID TRANSFER CHAIN",
        "risk_level": "HIGH",
        "risk_score": 86,
        "status": "OPEN",
        "created_at": "2026-10-27T07:35:00",
        "related_employee": None,
        "related_accounts": ["ACC-9120", "ACC-9130", "ACC-9131", "ACC-9132", "ACC-9133", "ACC-9134"],
        "related_customers": ["CUST-409"],
        "summary": "Multiple sub-threshold wire disbursements structured within 16 minutes from Blue Horizon Escrow across 5 individual retail accounts.",
        "risk_contributors": [
            {"name": "Transaction Splitting (Smurfing)", "score": 35, "evidence_id": None, "rule": "R02"},
            {"name": "Rapid transfer chain", "score": 30, "evidence_id": None, "rule": "R04"},
            {"name": "Unusual timing (Dawn surge)", "score": 21, "evidence_id": None, "rule": "R10"}
        ],
        "evidence_ids": []
    },
    {
        "alert_id": "ALT-10455",
        "alert_type": "DORMANT ACCOUNT ACTIVATION",
        "risk_level": "HIGH",
        "risk_score": 89,
        "status": "OPEN",
        "created_at": "2026-10-27T01:30:00",
        "related_employee": "EMP012",
        "related_accounts": ["ACC-9105", "ACC-9101"],
        "related_customers": ["CUST-405", "CUST-404"],
        "summary": "Dormant trust account inactive since 2018 altered via direct DBA query and drained of ₹35.0L via nocturnal offshore wire.",
        "risk_contributors": [
            {"name": "Dormant Account Activation", "score": 35, "evidence_id": "E008", "rule": "R08"},
            {"name": "Unusual timing (01:15 AM wire)", "score": 25, "evidence_id": "E008", "rule": "R10"},
            {"name": "Large transaction", "score": 20, "evidence_id": "E008", "rule": "R01"},
            {"name": "Unusual employee access", "score": 9, "evidence_id": "E007", "rule": "R06"}
        ],
        "evidence_ids": ["E007", "E008"]
    },
    {
        "alert_id": "ALT-10449",
        "alert_type": "LARGE TRANSACTION ANOMALY",
        "risk_level": "LOW",
        "risk_score": 38,
        "status": "RESOLVED",
        "created_at": "2026-10-26T16:45:00",
        "related_employee": None,
        "related_accounts": ["ACC-9109"],
        "related_customers": ["CUST-406"],
        "summary": "Commercial fleet fuel settlement above typical monthly mean; verified against corporate dispatch schedule.",
        "risk_contributors": [
            {"name": "Large transaction", "score": 25, "evidence_id": None, "rule": "R01"},
            {"name": "Velocity variance", "score": 13, "evidence_id": None, "rule": "R04"}
        ],
        "evidence_ids": []
    },
    {
        "alert_id": "ALT-10438",
        "alert_type": "EMPLOYEE-CUSTOMER RELATIONSHIP ANOMALY",
        "risk_level": "MEDIUM",
        "risk_score": 62,
        "status": "OPEN",
        "created_at": "2026-10-26T11:20:00",
        "related_employee": "EMP016",
        "related_accounts": ["ACC-9189"],
        "related_customers": ["CUST-425"],
        "summary": "Suspended branch assistant shared common registered residential postal code with recent loan applicant.",
        "risk_contributors": [
            {"name": "Employee-Account Relationship Anomaly", "score": 40, "evidence_id": None, "rule": "R09"},
            {"name": "Profile modification", "score": 22, "evidence_id": None, "rule": "R07"}
        ],
        "evidence_ids": []
    }
]

# ==========================================
# 10. CASES
# ==========================================
cases = [
    {
        "case_id": "CAS-8821",
        "title": "Operation Glass Ring: Coordinated Insider Intrusion & Rapid Circular Laundering",
        "priority": "CRITICAL",
        "status": "OPEN",
        "assigned_investigator": "EMP001",  # Sarah Jenkins
        "created_at": "2026-10-27T10:45:00",
        "related_alerts": ["ALT-10482"],
        "target_employee": "EMP007",
        "target_accounts": ["ACC-9011", "ACC-9042", "ACC-9088"],
        "evidence": ["E001", "E002", "E003", "E004", "E005", "E006"],
        "notes": [
            {
                "note_id": "NOT-01",
                "author": "Sarah Jenkins (Lead FinCrime Investigator)",
                "timestamp": "2026-10-27T10:48:12",
                "content": "Immediate preservation order initiated for workstation WS-MUM-OPS-074. PAM emergency token SEC-TICKET-99214 traced to unauthorized privileged injection. Circular money loop demonstrates synthetic round-tripping."
            }
        ],
        "resolution": None
    },
    {
        "case_id": "CAS-8819",
        "title": "Swiss Trust Dormant Liquidation Review",
        "priority": "HIGH",
        "status": "INVESTIGATING",
        "assigned_investigator": "EMP010",  # Tara Sen
        "created_at": "2026-10-27T02:00:00",
        "related_alerts": ["ALT-10455"],
        "target_employee": "EMP012",
        "target_accounts": ["ACC-9105", "ACC-9101"],
        "evidence": ["E007", "E008"],
        "notes": [
            {
                "note_id": "NOT-02",
                "author": "Tara Sen (Senior AML Analyst)",
                "timestamp": "2026-10-27T02:15:30",
                "content": "Requested correspondent bank in Singapore to freeze beneficiary account ACC-9101 pending beneficiary ultimate beneficial owner verification."
            }
        ],
        "resolution": None
    },
    {
        "case_id": "CAS-8804",
        "title": "Structured Merchant Payout Ring",
        "priority": "MEDIUM",
        "status": "INVESTIGATING",
        "assigned_investigator": "EMP001",
        "created_at": "2026-10-27T08:00:00",
        "related_alerts": ["ALT-10461"],
        "target_employee": None,
        "target_accounts": ["ACC-9120", "ACC-9130"],
        "evidence": [],
        "notes": [
            {
                "note_id": "NOT-03",
                "author": "Sarah Jenkins",
                "timestamp": "2026-10-27T08:20:00",
                "content": "Escrow account exhibiting classic smurfing distribution. Awaiting KYC document refresh."
            }
        ],
        "resolution": None
    },
    {
        "case_id": "CAS-8790",
        "title": "Logistics Fuel Settlement Batch Review",
        "priority": "LOW",
        "status": "RESOLVED",
        "assigned_investigator": "EMP010",
        "created_at": "2026-10-26T17:00:00",
        "related_alerts": ["ALT-10449"],
        "target_employee": None,
        "target_accounts": ["ACC-9109"],
        "evidence": [],
        "notes": [
            {
                "note_id": "NOT-04",
                "author": "Tara Sen",
                "timestamp": "2026-10-26T17:30:00",
                "content": "Invoices cross-checked against fleet GPS logs. Normal seasonal surge. False positive confirmed."
            }
        ],
        "resolution": "RESOLVED_FALSE_POSITIVE"
    }
]

# Write all entities to JSON files
files_to_write = {
    "employees.json": employees,
    "customers.json": customers,
    "accounts.json": accounts,
    "privilege_changes.json": privilege_changes,
    "access_events.json": access_events,
    "profile_changes.json": profile_changes,
    "transactions.json": transactions,
    "evidence.json": evidence,
    "alerts.json": alerts,
    "cases.json": cases
}

for filename, content in files_to_write.items():
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"Generated {filename}: {len(content)} items")

print("\nSuccessfully generated all synthetic datasets in", DATA_DIR)
