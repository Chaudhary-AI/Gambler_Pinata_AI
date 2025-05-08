# 🔥 AI Gambler - Full Browser Launcher + Scatter Detection
# File: ai_gambler.py

import time
import json
import cv2
import numpy as np
import pyautogui
from pathlib import Path
from PIL import ImageGrab
import os
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
from collections import Counter

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Config paths and defaults
TACTIC_PATH = Path("ruleset") / "tactic.json"
SCATTER_TEMPLATE_PATH = "assets/scatter_template"  # Correct path to scatter templates
DEFAULT_THRESHOLD = 3
REGION = (500, 300, 1200, 700)  # Default game screen region
STOP_KEY = "space"  # Key to stop spin
LOG_FILE = "experience_log.json"

# Load tactic.json
try:
    with open("tactic.json", "r", encoding="utf-8-sig") as f:  # Use utf-8-sig to handle BOM
        tactic = json.load(f)
        print(f"Loaded tactic.json: {tactic}")
        scatter_threshold = tactic.get("scatter_stop_threshold", DEFAULT_THRESHOLD)
        game_url = tactic.get("url", "https://m.x1skf.com/1492288/index.html?ot=AF64C68B-E04E-45E5-A4A3-3D7C2A34463D&btt=1&ops=gt61741327361818-gt6ta65three8three&l=th&or=12efmfuo%3Dj1ewr%3Doay&__hv=2fMEQCIEV9J4xK49iMCBPiT0a7pa6Ei5uIKurdFmghBycqBeD3AiAfMvKvFil8l8bmD0uYVF7wXLUDnNnurOSs7lXxeYXqxA%3D%3D")  # Default fallback URL
except Exception as e:
    print(f"⚠️ Error loading tactic.json: {e}")
    scatter_threshold = DEFAULT_THRESHOLD
    game_url = "https://m.x1skf.com/1492288/index.html?ot=AF64C68B-E04E-45E5-A4A3-3D7C2A34463D&btt=1&ops=gt61741327361818-gt6ta65three8three&l=th&or=12efmfuo%3Dj1ewr%3Doay&__hv=2fMEQCIEV9J4xK49iMCBPiT0a7pa6Ei5uIKurdFmghBycqBeD3AiAfMvKvFil8l8bmD0uYVF7wXLUDnNnurOSs7lXxeYXqxA%3D%3D"  # Default fallback URL

# User input for scatter threshold
user_threshold = input(f"Enter scatter threshold (default: {scatter_threshold}): ")
if user_threshold.isdigit():
    scatter_threshold = int(user_threshold)
    print(f"✅ Scatter threshold set to: {scatter_threshold}")
else:
    print(f"⚠️ Using default scatter threshold: {scatter_threshold}")

# Launch browser
print("🌐 Launching Game in Firefox...")
options = FirefoxOptions()
options.headless = False
try:
    driver = webdriver.Firefox(options=options)
    driver.get(game_url)
    driver.maximize_window()
    print(f"✅ Game loaded: {game_url}")
except Exception as e:
    print(f"❌ Failed to launch browser: {e}")
    exit()

# Wait for game to load
time.sleep(10)

# Load scatter template
while not os.path.exists(SCATTER_TEMPLATE_PATH):
    print(f"❌ Scatter template not found at {SCATTER_TEMPLATE_PATH}")
    SCATTER_TEMPLATE_PATH = input("Enter correct scatter template path: ")
scatter_template = cv2.imread(SCATTER_TEMPLATE_PATH, 0)
w, h = scatter_template.shape[::-1]

# User input for game screen region
region_input = input("Enter game screen region (x1,y1,x2,y2) or press Enter to use default: ")
if region_input:
    try:
        REGION = tuple(map(int, region_input.split(',')))
        print(f"✅ Region set to: {REGION}")
    except ValueError:
        print("⚠️ Invalid input, using default region.")

# Functions
def grab_game_screen():
    screen = ImageGrab.grab(bbox=REGION)
    return cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)

def count_scatters(frame):
    result = cv2.matchTemplate(frame, scatter_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.78)
    return len(set(zip(*loc[::-1])))

def stop_spin():
    print("🛑 Spin stopped!")
    pyautogui.press(STOP_KEY)

def log_event(event_type, message):
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": event_type,
        "output_snippet": message
    }
    try:
        # Load existing log
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    # Append new event
    logs.append(event)

    # Save updated log
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"Logged event: {event}")

def generate_summary(log_file):
    with open(log_file, "r") as f:
        logs = json.load(f)

    event_types = [log["type"] for log in logs]
    summary = Counter(event_types)
    print("Event Summary:", summary)

def sort_by_timestamp(log_file):
    with open(log_file, "r") as f:
        logs = json.load(f)

    sorted_logs = sorted(logs, key=lambda x: x["timestamp"])
    with open(log_file, "w") as f:
        json.dump(sorted_logs, f, indent=2)

def filter_by_event_type(log_file, event_type):
    with open(log_file, "r") as f:
        logs = json.load(f)

    filtered_logs = [log for log in logs if log["type"] == event_type]
    print(f"Filtered Logs ({event_type}):", filtered_logs)

# Example usage
generate_summary("experience_log.json")
sort_by_timestamp("experience_log.json")
filter_by_event_type("experience_log.json", "loss")

# Game loop
logging.info("🎰 AI Active | Scatter Trigger = %d+", scatter_threshold)
try:
    while True:
        frame = grab_game_screen()
        scatters = count_scatters(frame)
        print(f"[👁️] Scatters: {scatters}", end="\r")

        if scatters >= scatter_threshold:
            logging.info("Detected %d scatters", scatters)
            log_event("scatter", f"Detected {scatters} scatters.")
            stop_spin()
            time.sleep(0.8)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n👋 AI Exited")
finally:
    driver.quit()
    print("🛑 Browser closed.")