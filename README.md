# Financial Risk Analysis and Rule-Based Fraud Detection System

A full-stack educational application that analyzes **synthetic** financial transactions and raises explainable alerts for manual review. An alert is not proof of fraud.

## Features
- FastAPI REST API with interactive Swagger docs
- MySQL storage for customers, accounts, transactions, alerts, users and audit logs
- Token-based login and protected API routes
- Configurable rules for unusual amount, transaction frequency and region changes
- Risk score from 0–100 with transparent weights
- Alert review workflow: PENDING, UNDER_REVIEW, CLEARED, CLOSED
- CSV transaction import
- Dashboard summary and Pandas/NumPy/Matplotlib analysis
- Pytest starter tests

## Risk rules
| Rule | Default weight | Trigger |
|---|---:|---|
| Unusual amount | 40 | Amount greater than 50,000 |
| High frequency | 35 | At least 5 earlier transactions in the previous 10 minutes |
| Region change | 25 | Region differs from the latest earlier transaction |

Weights and thresholds are educational defaults, not banking standards. They should be tuned and evaluated against labelled synthetic data. False positives and false negatives are expected.

## Requirements
- Python 3.10+
- MySQL 8+
- A modern browser
- Git (for version control)

## Setup
1. Create a MySQL database by running `database/schema.sql` in MySQL Workbench or the MySQL CLI.
2. Run `database/seed_data.sql` to create two demo customers and accounts.
3. Open a terminal in `backend/` and create a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to a new root-level file named `.env` and update the MySQL password and SECRET_KEY. Keep `.env` in the project root; the backend and analytics scripts load settings from there.
6. Start the API: `uvicorn app.main:app --reload`
7. Open `http://127.0.0.1:8000/docs` to inspect and test the API.
8. In another terminal, from the project root run: `python -m http.server 5500 --directory frontend`
9. Open `http://127.0.0.1:5500/login.html`. Create a demo account, then sign in.
10. Import `data/sample_transactions.csv` from the dashboard. The CSV uses account IDs 1 and 2 created by the seed script.

## Analytics
From the project root, activate the same virtual environment and run:
- `python analytics/analysis.py`
- `python analytics/charts.py`
- `python analytics/reports.py`

Generated charts and JSON summary are saved under `reports/`.

## Tests
From `backend/` with the virtual environment active:
`pytest ../tests -q`

## API endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/transactions/`
- `POST /api/transactions/`
- `POST /api/transactions/import`
- `GET /api/alerts/`
- `PATCH /api/alerts/{alert_id}`
- `GET /api/dashboard/summary`

## Important limitations and responsible use
- All included data is synthetic. Never upload real banking or payment data.
- Rule-based alerts are indicators for human review, not confirmed fraud.
- Static thresholds may not generalize across customers, regions or transaction types.
- False positives can inconvenience legitimate users; false negatives can miss suspicious activity.
- This educational demo is not production-ready. Production systems require stronger secrets management, authorization roles, rate limiting, encryption, privacy controls, monitoring, migration management and independent security review.
