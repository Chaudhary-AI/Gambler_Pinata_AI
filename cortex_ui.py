# 🎛️ Cortex UI Terminal Interface
# File: cortex_ui.py

import logging
import os

# Logging setup
LOG_FILE = "cortex_ui.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Global state for Hot Mode
hot_mode = False

def log_action(action):
    logging.info(action)

def start_ai_gambler():
    print("🚀 Starting AI Gambler...")
    log_action("AI Gambler started.")
    # Call the AI Gambler script here (e.g., os.system("python ai_gambler.py"))

def toggle_hot_mode():
    global hot_mode
    hot_mode = not hot_mode
    state = "enabled" if hot_mode else "disabled"
    print(f"🔥 Hot Mode {state}")
    log_action(f"Hot Mode {state}.")

def trigger_report():
    print("📊 Generating Report...")
    log_action("Report triggered.")
    # Call the report generation script here (e.g., os.system("python generate_report.py"))

def launch_ui():
    while True:
        print("\n🧠 Cortex Interface")
        print("====================")
        print("1. Start AI Gambler")
        print("2. Toggle Hot Mode")
        print("3. Trigger Report")
        print("4. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            start_ai_gambler()
        elif choice == "2":
            toggle_hot_mode()
        elif choice == "3":
            trigger_report()
        elif choice == "4":
            print("👋 Exiting...")
            log_action("User exited the interface.")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    launch_ui()
