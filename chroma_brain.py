# 🧠 Chroma Brain – Game Automation Module

import os
import logging
import json
import webbrowser
from pathlib import Path
import pyautogui
import time

# Logging setup
LOG_FILE = "chroma_brain.log"
try:
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")
except Exception as e:
    print(f"⚠️ Logging setup failed: {e}")

def log_action(message):
    """Logs actions and errors."""
    logging.info(message)

def load_game_url():
    """
    Loads the game URL from tactic.json.
    """
    try:
        with open("tactic.json", "r") as f:
            config = json.load(f)
            return config.get("url")
    except Exception as e:
        log_action(f"⚠️ Failed to load URL from tactic.json: {e}")
        print(f"⚠️ Failed to load URL from tactic.json: {e}")
        return None

def launch_game(url):
    """
    Launches the game in the default web browser.
    """
    if not url:
        print("❌ No URL provided. Cannot launch the game.")
        return

    try:
        webbrowser.open(url)
        log_action(f"Game launched at URL: {url}")
        print(f"✅ Game launched at: {url}")
    except Exception as e:
        log_action(f"⚠️ Failed to launch game: {e}")
        print(f"⚠️ Failed to launch game: {e}")

def perform_game_actions():
    """
    Automates game actions like clicking buttons and detecting symbols.
    """
    try:
        time.sleep(10)  # Wait for the game to load
        print("🎮 Starting game automation...")

        # Example: Click the spin button
        spin_button_location = pyautogui.locateOnScreen("assets/symbol_spin_button.png", confidence=0.8)
        if spin_button_location:
            pyautogui.click(spin_button_location)
            log_action("Clicked spin button")
            print("✅ Spin button clicked")
        else:
            log_action("Spin button not found")
            print("❌ Spin button not found")

        # Add more actions here (e.g., adjust bet, detect symbols)
    except Exception as e:
        log_action(f"⚠️ Error during game actions: {e}")
        print(f"⚠️ Error during game actions: {e}")

if __name__ == "__main__":
    # Load the game URL from tactic.json
    GAME_URL = load_game_url()

    # Launch the game
    launch_game(GAME_URL)

    # Perform game actions
    perform_game_actions()