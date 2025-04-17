# 🔥 Hot Mode Toggle
# File: hot_mode.py

HOT_MODE_FILE = "memory/hot_mode.flag"

def enable_hot_mode():
    with open(HOT_MODE_FILE, "w") as f:
        f.write("enabled")
    print("🔥 Hot mode enabled!")

def disable_hot_mode():
    import os
    if os.path.exists(HOT_MODE_FILE):
        os.remove(HOT_MODE_FILE)
        print("❄️ Hot mode disabled.")
    else:
        print("ℹ️ Hot mode was not active.")

if __name__ == "__main__":
    enable_hot_mode()
