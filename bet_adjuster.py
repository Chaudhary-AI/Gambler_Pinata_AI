from shared_brain import ask_brain
# 🎚️ Bet Adjuster Engine
# File: bet_adjuster.py

import random
import pyautogui
import json
import logging
from pathlib import Path

# Load button coordinates from configuration
CONFIG_FILE = Path("assets_config.json")

def load_coordinates():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    return config["buttons"]["increase"], config["buttons"]["decrease"]

INCREASE_COORDS, DECREASE_COORDS = load_coordinates()

# Logging setup
logging.basicConfig(filename="bet_adjuster.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_action(action):
    logging.info(action)

def adjust_bet(mode="auto"):
    if mode == "auto":
        decision = random.choice(["increase", "decrease", "hold"])
    else:
        decision = mode

    try:
        if decision == "increase":
            pyautogui.moveTo(*INCREASE_COORDS)
            pyautogui.click()
            log_action("⬆️ Bet Increased")
            print("⬆️ Bet Increased")
        elif decision == "decrease":
            pyautogui.moveTo(*DECREASE_COORDS)
            pyautogui.click()
            log_action("⬇️ Bet Decreased")
            print("⬇️ Bet Decreased")
        else:
            log_action("⚖️ Bet Held")
            print("⚖️ Bet Held")
    except Exception as e:
        logging.error(f"Error adjusting bet: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎚️ Bet Adjuster Engine Started")
    print("Commands: 'increase', 'decrease', 'hold', 'auto', 'exit'")
    
    while True:
        mode = input("Enter command: ").strip().lower()
        if mode == "exit":
            print("👋 Exiting Bet Adjuster Engine.")
            break
        elif mode in ["increase", "decrease", "hold", "auto"]:
            adjust_bet(mode=mode)
        else:
            print("❌ Invalid command. Please enter 'increase', 'decrease', 'hold', 'auto', or 'exit'.")

