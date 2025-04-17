# 🧠 Brain Backup Logger
# File: brain_backup.py

import json
from datetime import datetime
from pathlib import Path

MEMORY_PATH = Path("memory") / "experience_log.json"
BACKUP_PATH = Path("memory") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

def backup_brain():
    if MEMORY_PATH.exists():
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)

        BACKUP_PATH.parent.mkdir(exist_ok=True)
        with open(BACKUP_PATH, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Brain backup saved to {BACKUP_PATH}")
    else:
        print("⚠️ No brain memory file to backup.")

if __name__ == "__main__":
    backup_brain()
