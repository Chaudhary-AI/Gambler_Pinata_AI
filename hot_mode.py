# 🔥 Hot Mode Toggle
# File: hot_mode.py

import os
import logging

# Logging setup
LOG_FILE = "hot_mode.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Hot mode flag file
HOT_MODE_FILE = os.getenv("HOT_MODE_FILE", "memory/hot_mode.flag")

def log_action(message):
    logging.info(message)

def enable_hot_mode():
    """
    Enables hot mode by creating the flag file.
    """
    os.makedirs(os.path.dirname(HOT_MODE_FILE), exist_ok=True)
    with open(HOT_MODE_FILE, "w") as f:
        f.write("enabled")
    print("🔥 Hot mode enabled!")
    log_action("Hot mode enabled.")

def disable_hot_mode():
    """
    Disables hot mode by deleting the flag file.
    """
    if os.path.exists(HOT_MODE_FILE):
        os.remove(HOT_MODE_FILE)
        print("❄️ Hot mode disabled.")
        log_action("Hot mode disabled.")
    else:
        print("ℹ️ Hot mode was not active.")
        log_action("Hot mode was not active.")

def toggle_hot_mode():
    """
    Toggles hot mode based on the current state.
    """
    if os.path.exists(HOT_MODE_FILE):
        disable_hot_mode()
    else:
        enable_hot_mode()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hot Mode Toggle")
    parser.add_argument("--enable", action="store_true", help="Enable hot mode")
    parser.add_argument("--disable", action="store_true", help="Disable hot mode")
    parser.add_argument("--toggle", action="store_true", help="Toggle hot mode")
    args = parser.parse_args()

    if args.enable:
        enable_hot_mode()
    elif args.disable:
        disable_hot_mode()
    elif args.toggle:
        toggle_hot_mode()
    else:
        print("ℹ️ Use --enable, --disable, or --toggle")