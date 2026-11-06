import json
from pathlib import Path
from analysis import load_data, summarize

if __name__ == "__main__":
    output = Path(__file__).resolve().parents[1] / "reports"
    output.mkdir(exist_ok=True)
    report = summarize(load_data())
    (output / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
