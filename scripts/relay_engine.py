# 🔁 Relay Engine
# File: relay_engine.py

import time

def dispatch_relay():
    print("🔁 Dispatching relay...")
    for i in range(3):
        print(f"⏱️ Tick {i + 1}")
        time.sleep(1)
    print("✅ Relay dispatched successfully")

if __name__ == "__main__":
    dispatch_relay()
