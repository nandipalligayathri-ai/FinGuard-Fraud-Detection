from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
import matplotlib.pyplot as plt
from analysis import load_data

OUT = Path(__file__).resolve().parents[1] / "reports"
OUT.mkdir(exist_ok=True)

def create_charts():
    df = load_data()
    if df.empty:
        print("No data available for charts.")
        return
    df["transaction_datetime"] = __import__("pandas").to_datetime(df["transaction_datetime"])
    daily = df.groupby(df["transaction_datetime"].dt.date).size()
    plt.figure(figsize=(9, 4))
    daily.plot(kind="line", marker="o")
    plt.title("Transaction Volume by Day")
    plt.xlabel("Date"); plt.ylabel("Transactions")
    plt.tight_layout(); plt.savefig(OUT / "transaction_trend.png"); plt.close()

    flagged = df[df["risk_score"].notna()]
    if not flagged.empty:
        plt.figure(figsize=(8, 4))
        flagged["risk_score"].plot(kind="hist", bins=10)
        plt.title("Risk Score Distribution")
        plt.xlabel("Risk score"); plt.ylabel("Alert count")
        plt.tight_layout(); plt.savefig(OUT / "risk_score_distribution.png"); plt.close()
    print(f"Charts saved in {OUT}")

if __name__ == "__main__":
    create_charts()
