# 🎰 Free Spin Tracker
# File: free_spin_tracker.py

from pathlib import Path
import json

FREE_SPIN_FILE = Path("memory") / "freespins.json"

def log_free_spin():
    FREE_SPIN_FILE.parent.mkdir(exist_ok=True)
    data = []
    if FREE_SPIN_FILE.exists():
        with open(FREE_SPIN_FILE, "r") as f:
            data = json.load(f)
    data.append({"spin": "free", "status": "won"})
    with open(FREE_SPIN_FILE, "w") as f:
        json.dump(data, f)
    print("✅ Free spin logged.")

if __name__ == "__main__":
    log_free_spin()
