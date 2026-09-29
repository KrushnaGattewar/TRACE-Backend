# TRACE — Financial Crime & Insider Risk Intelligence Platform

> **"Financial crime hides in the connections."**
> TRACE connects employee activity, privileged access logs, customer identity shifts, account relationships, and financial transactions into one explainable investigation graph.

---

## 1. Architectural Overview

```text
React 19 + TypeScript Frontend (Port 5173)
           │ (Vite Dev Server, Cytoscape.js, Editorial Broadsheet Design)
           ▼
     FastAPI Backend (Port 8000)
           │
   ┌───────┼────────────────┐
   ▼       ▼                ▼
Detection Investigation   Case Management
Engine    Engine (Graph)  Engine
(R01-R10) (1-3 Hops)      (Dossier Export)
   │       │                │
   └───────┼────────────────┘
           ▼
   Structured Data Layer (JSON + In-Memory Thread-Safe Indexes)
   • 18 Employees  • 35 Customers  • 43 Accounts
   • 137 Transactions  • 39 Access Events  • Privilege Logs
   • Profile Audit Logs  • 8 Forensic Evidence Items
```

---

## 2. Henry Editorial Broadsheet Design System

The visual identity follows an **editorial investigative dossier / financial intelligence broadsheet**:

### Warm Monochrome Palette
* **Paper**: `#fafafa`
* **Headline Ink**: `#2a2722`
* **Hairline Rule**: `#eeeeee`
* **Midstone**: `#9f9f9f`
* **Ash**: `#666666`
* **Pebble**: `#b3b3b3`
* **Sepia**: `#3e3b36`
* **Inverted Dark Sections**: Background `#2a2722`, Text `#fafafa`

### Typography Hierarchy
* **Editorial Headlines**: *Fraunces* (Editorial display serif)
* **Body / Navigation / Controls**: *Inter* (Neue Montreal fallback)
* **Giant Section Displays**: *Antonio* (Ultra-condensed broadside headers)
* **Telemetry & Hash Signatures**: *JetBrains Mono* (Audit timestamps & SHA-256 signatures)

### Restraint Principles
* **Zero Chromatic Accents**: No blue, no green, no red, no rainbow charts.
* **Typographic Hierarchy**: Hierarchy is communicated strictly via type scale, weight, paper/ink inversion, and hairline rules.
* **12px Radius Only**: Clean rectilinear structure with 12px border radius only when cards are genuinely useful. Zero box-shadows or glow effects.

---

## 3. The Demonstration Scenario (ALT-10482)

The platform demonstrates the complete investigative journey:
**DATA → CONNECTION → DETECTION → EXPLANATION → EVIDENCE → INVESTIGATION → CASE**

### Incident Chronology
```text
EMP007 (Vikram Malhotra - Senior Operations Analyst)
  ↓
10:05  PRIVILEGE ESCALATION [E001]
       Elevated to Tier 4 Admin Override via emergency bypass token SEC-TICKET-99214-UNAUTH
  ↓
10:17  UNUSUAL ACCOUNT ACCESS [E002]
       Deep ledger query of Account A (ACC-9011 - Aarav Singhania Private Wealth)
  ↓
10:21  CUSTOMER PROFILE MODIFICATION [E003]
       CUST-401 primary telephone altered to burner line +91 98200 11099, SMS alerts bypassed
  ↓
10:27  TRANSACTION [E004]
       ₹4,60,000 transferred ACC-9011 (A) → ACC-9042 (B, Maya Overseas Shell)
  ↓
10:31  TRANSACTION [E005]
       ₹4,20,000 transferred ACC-9042 (B) → ACC-9088 (C, Kavita Patel Conduit)
  ↓
10:38  TRANSACTION [E006]
       ₹4,00,000 transferred ACC-9088 (C) → ACC-9011 (A)
```

### Explainable Risk Contributors (Score: 95/100)
* `+25` Unusual employee access (Rule R06, Evidence E002)
* `+20` Privilege escalation (Rule R05, Evidence E001)
* `+20` Large transaction (Rule R01, Evidence E004)
* `+15` Circular money flow (Rule R03, Evidence E006)
* `+10` Profile modification (Rule R07, Evidence E003)
* `+05` Rapid transfer chain (Rule R04, Evidence E005)

---

## 4. Detection Engine Rules (R01–R10)

| Rule ID | Rule Name | Description |
|---|---|---|
| **R01** | Large Transaction | Transactions exceeding configurable threshold (≥ ₹4,00,000) |
| **R02** | Transaction Splitting (Smurfing) | Multiple sub-₹1,00,000 transactions exceeding aggregate threshold within 30 min |
| **R03** | Circular Transfer | Graph DFS cycle detection identifying closed loop transaction paths (A → B → C → A) |
| **R04** | Rapid Transfer Chain | Multiple pass-through transfers across accounts within 10 minutes |
| **R05** | Privilege Escalation | Sudden privilege jumps (Level 2 → 4) or unauthorized emergency ticket grants |
| **R06** | Unusual Access | Account ledger inspection outside employee portfolio and working baseline |
| **R07** | Profile Change Before Txn | Contact or limit mutation within 60 minutes of outbound transaction |
| **R08** | Dormant Account Activation | Activity on inactive or restricted trust accounts (e.g. ACC-9105) |
| **R09** | Relationship Anomaly | Suspended employees or unlinked staff accessing customer accounts |
| **R10** | Unusual Timing | High-value settlements executed during night hours (23:00 - 05:00) |

---

## 5. Main Application Screens

1. **Overview / Intelligence Dashboard**: Broadsheet layout with large typography metrics, active priority queue, inverted axiom hero, and live rule evaluation.
2. **Alert Investigation Screen**: Correlated incident header, explainable risk breakdown (+25, +20, etc.), interactive Cytoscape relationship graph, unified chronological timeline, and action bar.
3. **Case Management Screen**: Formal case dossiers, status lifecycle (`OPEN` → `INVESTIGATING` → `ESCALATED` → `RESOLVED` → `CLOSED` → `FALSE_POSITIVE`), investigator notes journal, and evidence attachments.
4. **Graph Network Explorer**: Dedicated full-screen relationship canvas with 1-hop, 2-hop, and 3-hop expansion, entity filters, and node/edge inspector.
5. **Evidence Telemetry Vault**: First-class evidence artifacts with SHA-256 cryptographic hashes, telemetry source tracking, and confidence verification.
6. **Core Ledger & Entities**: Real-time explorer for Employees, Customers, Accounts, and Transactions.
7. **Dossier Export Engine**: Structured investigation report generator with confidential broadsheet printable view and complete JSON download.

---

## 6. How to Run Locally

Open two PowerShell terminals at the repository root.

### Start Backend (FastAPI)
```powershell
cd .\backend
python -m pip install fastapi uvicorn pydantic
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
The package installation is needed once per Python environment. Backend Swagger documentation: `http://127.0.0.1:8000/docs`.

### Start Frontend (Vite + React)
```powershell
cd .\frontend
npm install
npm run dev
```
Run `npm install` once. Open the URL printed by Vite, usually `http://localhost:5173/`.

## 7. Deploying the Frontend to Netlify

The Vite frontend can be hosted on Netlify. The FastAPI backend must be deployed separately; Netlify does not run this backend as a web service.

### Deploy the Backend

For example, create a Render Web Service from this repository with the repository root as its root directory. Keeping the root directory matters because the backend loads its JSON files from the top-level `data/` directory.

```text
Build command: pip install -r backend/requirements.txt
Start command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Copy the public backend URL after it deploys, such as `https://your-service.onrender.com`.

### Deploy the Frontend

Import this repository into Netlify. It reads the build and publish settings from `netlify.toml`. In the Netlify site's environment variables, add:

```text
VITE_API_BASE_URL=https://your-service.onrender.com
```

Replace the example URL with your backend URL, then trigger a new deploy. The API URL should not include a trailing slash. The frontend uses `http://127.0.0.1:8000` as its API URL when developing locally.
