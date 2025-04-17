from shared_brain import ask_brain
# 🛡️ Auto Sentinel — Surveillance Task Runner
# File: auto_sentinel.py

import time
from pathlib import Path

LOCK_FILE = Path("logs") / "sentinel.lock"

def sentinel_running():
    return LOCK_FILE.exists()

def activate_sentinel():
    LOCK_FILE.parent.mkdir(exist_ok=True)
    with open(LOCK_FILE, "w") as f:
        f.write(str(time.time()))
    print("✅ Sentinel Activated")

def deactivate_sentinel():
    if sentinel_running():
        LOCK_FILE.unlink()
        print("🛑 Sentinel Deactivated")
    else:
        print("ℹ️ Sentinel was not active.")

if __name__ == "__main__":
    if sentinel_running():
        deactivate_sentinel()
    else:
        activate_sentinel()

