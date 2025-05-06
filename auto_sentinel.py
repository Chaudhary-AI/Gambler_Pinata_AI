from shared_brain import ask_brain
# 🛡️ Auto Sentinel — Surveillance Task Runner
# File: auto_sentinel.py

import time
from pathlib import Path
import logging

# Lock file and log file paths
LOCK_FILE = Path("logs") / "sentinel.lock"
LOG_FILE = Path("logs") / "sentinel.log"

# Logging setup
LOCK_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def sentinel_running():
    if LOCK_FILE.exists():
        lock_time = float(LOCK_FILE.read_text())
        if time.time() - lock_time > 86400:  # 24 hours
            print("ℹ️ Sentinel lock file is outdated.")
            return False
        return True
    return False

def activate_sentinel():
    LOCK_FILE.parent.mkdir(exist_ok=True)
    with open(LOCK_FILE, "w") as f:
        f.write(str(time.time()))
    logging.info("Sentinel Activated")
    print("✅ Sentinel Activated")

def deactivate_sentinel():
    try:
        if sentinel_running():
            LOCK_FILE.unlink()
            logging.info("Sentinel Deactivated")
            print("🛑 Sentinel Deactivated")
        else:
            print("ℹ️ Sentinel was not active.")
    except Exception as e:
        logging.error(f"Error deactivating sentinel: {e}")
        print(f"❌ Error: {e}")

def sentinel_status():
    if sentinel_running():
        print("✅ Sentinel is currently active.")
    else:
        print("ℹ️ Sentinel is not active.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto Sentinel Task Runner")
    parser.add_argument("--activate", action="store_true", help="Activate the sentinel")
    parser.add_argument("--deactivate", action="store_true", help="Deactivate the sentinel")
    parser.add_argument("--status", action="store_true", help="Check sentinel status")
    args = parser.parse_args()

    if args.activate:
        activate_sentinel()
    elif args.deactivate:
        deactivate_sentinel()
    elif args.status:
        sentinel_status()
    else:
        print("ℹ️ Use --activate, --deactivate, or --status")

