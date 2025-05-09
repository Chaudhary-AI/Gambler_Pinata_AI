# 🧠 Chroma Brain – Game Automation Module

import os
import json
import logging
import time
import webbrowser
from pathlib import Path
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui

# Paths and setup
BASE_PATH = Path(__file__).parent
ASSETS_PATH = BASE_PATH / "assets"
TACTIC_PATH = BASE_PATH / "ruleset" / "tactic.json"
SPIN_BUTTON_PATH = ASSETS_PATH / "symbol_spin_button.png"
LOG_FILE = BASE_PATH / "chroma_brain.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_action(message):
    logging.info(message)
    print(message)

def load_game_url():
    try:
        with open(TACTIC_PATH, "r", encoding="utf-8-sig") as f:
            config = json.load(f)
            return config.get("url")
    except Exception as e:
        log_action(f"⚠️ Failed to load tactic.json: {e}")
        return None

def capture_screen():
    screen = ImageGrab.grab()
    return cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

def detect_element(template_path, threshold=0.8):
    if not template_path.exists():
        log_action(f"❌ Template not found: {template_path}")
        return None

    screen = capture_screen()
    template = cv2.imread(str(template_path), cv2.IMREAD_UNCHANGED)

    if template is None:
        log_action(f"❌ Failed to load template image: {template_path}")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        log_action(f"✅ Detected {template_path.name} at {max_loc} (confidence: {max_val:.2f})")
        return max_loc
    else:
        log_action(f"❌ {template_path.name} not detected (confidence: {max_val:.2f})")
        return None

def click_at(position, offset_x=30, offset_y=30):
    x = position[0] + offset_x
    y = position[1] + offset_y
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()
    log_action(f"🖱️ Clicked at {x}, {y}")

def perform_game_actions():
    try:
        time.sleep(10)  # Wait for game to load
        log_action("🎮 Starting game actions...")

        spin_pos = detect_element(SPIN_BUTTON_PATH, threshold=0.8)
        if spin_pos:
            click_at(spin_pos)
        else:
            log_action("⚠️ Spin button not found after initial load.")
    except Exception as e:
        log_action(f"❌ Error during automation: {e}")

if __name__ == "__main__":
    game_url = load_game_url()

    if not game_url:
        log_action("❌ No URL found. Exiting...")
        exit()

    log_action(f"🌐 Launching game at: {game_url}")
    webbrowser.open(game_url)

    perform_game_actions()
