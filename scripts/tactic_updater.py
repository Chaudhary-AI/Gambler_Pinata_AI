# 🧠 Tactic Updater Engine
# File: tactic_updater.py

from pathlib import Path
import json

TACTIC_FILE = Path("ruleset") / "tactic.json"

def update_tactic(name="default", strategy=None):
    TACTIC_FILE.parent.mkdir(exist_ok=True)
    tactics = {"name": name, "strategy": strategy or "hold-until-multiplier"}
    with open(TACTIC_FILE, "w") as f:
        json.dump(tactics, f, indent=2)
    print(f"🧠 Updated tactic: {tactics}")

if __name__ == "__main__":
    update_tactic("greedy-bet", "raise-on-x50")
