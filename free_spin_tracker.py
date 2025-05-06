from pathlib import Path
import json
from datetime import datetime
import argparse

FREE_SPIN_FILE = Path("memory") / "freespins.json"

def log_free_spin(status="won"):
    """
    Logs a free spin with the given status.
    """
    FREE_SPIN_FILE.parent.mkdir(exist_ok=True)
    try:
        with open(FREE_SPIN_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append({
        "spin": "free",
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    })

    with open(FREE_SPIN_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Free spin logged with status: {status}.")

def generate_summary():
    """
    Generates a summary of all logged free spins.
    """
    if not FREE_SPIN_FILE.exists():
        print("⚠️ No free spins logged yet.")
        return

    with open(FREE_SPIN_FILE, "r") as f:
        data = json.load(f)

    total_spins = len(data)
    won_spins = sum(1 for spin in data if spin["status"] == "won")
    print(f"📊 Total Spins: {total_spins}, Wins: {won_spins}, Losses: {total_spins - won_spins}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Free Spin Tracker")
    parser.add_argument("--status", choices=["won", "lost"], default="won", help="Status of the free spin")
    parser.add_argument("--summary", action="store_true", help="Generate summary of free spins")
    args = parser.parse_args()

    if args.summary:
        generate_summary()
    else:
        log_free_spin(status=args.status)
