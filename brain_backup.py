# 🧠 Brain Backup Logger
# File: brain_backup.py

import json
from datetime import datetime
from pathlib import Path
import logging

# Paths
MEMORY_PATH = Path("memory") / "experience_log.json"
BACKUP_PATH = Path("memory") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
LOG_FILE = Path("memory") / "backup.log"

# Logging setup
LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def backup_brain():
    if MEMORY_PATH.exists():
        try:
            with open(MEMORY_PATH, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Invalid JSON format in experience_log.json")
            logging.error("Failed to backup: Invalid JSON format")
            return

        BACKUP_PATH.parent.mkdir(exist_ok=True)
        with open(BACKUP_PATH, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Brain backup saved to {BACKUP_PATH}")
        logging.info(f"Backup saved to {BACKUP_PATH}")
    else:
        print("⚠️ No brain memory file to backup.")
        logging.warning("No brain memory file to backup.")

def cleanup_old_backups(max_backups=5):
    backups = sorted(BACKUP_PATH.parent.glob("backup_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    for old_backup in backups[max_backups:]:
        old_backup.unlink()
        logging.info(f"Deleted old backup: {old_backup}")
        print(f"🗑️ Deleted old backup: {old_backup}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Brain Backup Logger")
    parser.add_argument("--backup", action="store_true", help="Create a new backup")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup old backups")
    args = parser.parse_args()

    if args.backup:
        backup_brain()
    if args.cleanup:
        cleanup_old_backups()
