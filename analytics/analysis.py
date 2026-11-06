"""Run summary analysis against the configured database."""
import os
from pathlib import Path
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/financial_risk_db")

def load_data():
    engine = create_engine(DB_URL, pool_pre_ping=True)
    return pd.read_sql("""
        SELECT t.transaction_id, t.transaction_datetime, t.amount, t.transaction_type,
               t.channel, t.region, a.risk_score, a.review_status
        FROM transactions t LEFT JOIN alerts a ON t.transaction_id = a.transaction_id
    """, engine)

def summarize(df):
    if df.empty:
        return {"message": "No transaction data found"}
    amounts = pd.to_numeric(df["amount"], errors="coerce").dropna()
    return {
        "rows": int(len(df)),
        "average_amount": round(float(amounts.mean()), 2),
        "median_amount": round(float(amounts.median()), 2),
        "amount_std_dev": round(float(np.std(amounts)), 2),
        "flagged_rows": int(df["risk_score"].notna().sum()),
        "flag_rate_percent": round(float(df["risk_score"].notna().mean() * 100), 2)
    }

if __name__ == "__main__":
    data = load_data()
    print(summarize(data))
