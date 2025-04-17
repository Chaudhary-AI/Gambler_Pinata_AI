# 📊 Report Generator
# File: report_generator.py

import json
from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path("logs")
MEMORY_FILE = Path("memory") / "experience_log.json"

def generate_report():
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = REPORTS_DIR / f"report_{timestamp}.json"

    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"error": "No memory log found"}

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"📁 Report saved to: {output_file}")

if __name__ == "__main__":
    generate_report()
