# 🔥 AI Gambler - Full Browser Launcher + Scatter Detection
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
from selenium.webdriver.firefox.service import Service
from datetime import datetime
from collections import Counter

# ===================== SETUP =====================

# Paths & Constants
BASE_PATH = Path(__file__).parent
TACTIC_PATH = BASE_PATH / "ruleset" / "tactic.json"
SCATTER_TEMPLATE_PATH = BASE_PATH / "assets" / "scatter_template.png"
LOG_FILE = BASE_PATH / "experience_log.json"
GECKO_PATH = r"C:\Users\Yenkh\1-ManArmy\OneDrive\professorai\Gambler_Pinata_AI\geckodriver.exe"

DEFAULT_THRESHOLD = 3
DEFAULT_GAME_URL = "https://example.com"
STOP_KEY = "space"
REGION = (500, 300, 1200, 700)  # Default capture region

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# ===================== LOAD TACTIC.JSON =====================

try:
    with open(TACTIC_PATH, "r", encoding="utf-8-sig") as f:
        tactic = json.load(f)
        print(f"✅ Loaded tactic.json: {tactic}")
        scatter_threshold = tactic.get("scatter_stop_threshold", DEFAULT_THRESHOLD)
        game_url = tactic.get("url", DEFAULT_GAME_URL)
except Exception as e:
    print(f"⚠️ Failed to load tactic.json: {e}")
    scatter_threshold = DEFAULT_THRESHOLD
    game_url = DEFAULT_GAME_URL

print(f"🎯 Scatter Threshold: {scatter_threshold}")
print(f"🌍 Game URL: {game_url}")

# ===================== USER INPUT =====================

user_threshold = input(f"Enter scatter threshold (default: {scatter_threshold}): ")
if user_threshold.isdigit():
    scatter_threshold = int(user_threshold)
    print(f"✅ Using scatter threshold: {scatter_threshold}")
else:
    print(f"⚠️ Using default scatter threshold: {scatter_threshold}")

region_input = input("Enter game screen region (x1,y1,x2,y2) or press Enter to use default: ")
if region_input:
    try:
        REGION = tuple(map(int, region_input.split(',')))
        print(f"✅ Region set to: {REGION}")
    except ValueError:
        print("⚠️ Invalid region input, using default.")

# ===================== BROWSER LAUNCH =====================

print("🌐 Launching Firefox with Selenium...")
options = FirefoxOptions()
options.headless = False

try:
    service = Service(executable_path=GECKO_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(game_url)
    driver.maximize_window()
    print(f"✅ Game loaded: {game_url}")
except Exception as e:
    print(f"❌ Failed to launch Firefox: {e}")
    exit()

time.sleep(10)  # Let game load

# ===================== LOAD SCATTER TEMPLATE =====================

while not SCATTER_TEMPLATE_PATH.exists():
    print(f"❌ Scatter template not found at {SCATTER_TEMPLATE_PATH}")
    new_path = input("Enter correct path to scatter_template.png: ")
    SCATTER_TEMPLATE_PATH = Path(new_path)

scatter_template = cv2.imread(str(SCATTER_TEMPLATE_PATH), 0)
w, h = scatter_template.shape[::-1]

# ===================== FUNCTIONS =====================

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
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(event)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"📝 Logged event: {event}")

def generate_summary():
    if not LOG_FILE.exists():
        print("📭 No log file found.")
        return
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    summary = Counter(log["type"] for log in logs)
    print("📊 Event Summary:", summary)

def sort_by_timestamp():
    if not LOG_FILE.exists():
        return
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    sorted_logs = sorted(logs, key=lambda x: x["timestamp"])
    with open(LOG_FILE, "w") as f:
        json.dump(sorted_logs, f, indent=2)

def filter_by_event_type(event_type):
    if not LOG_FILE.exists():
        return
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    filtered = [log for log in logs if log["type"] == event_type]
    print(f"📂 Filtered ({event_type}):", filtered)

# ===================== LOG ANALYTICS (Optional) =====================

generate_summary()
sort_by_timestamp()
filter_by_event_type("scatter")

# ===================== MAIN GAME LOOP =====================

print(f"🎰 AI ACTIVE | Watching for {scatter_threshold}+ scatters...")

try:
    while True:
        frame = grab_game_screen()
        scatters = count_scatters(frame)
        print(f"[👁️] Scatters: {scatters}", end="\r")

        if scatters >= scatter_threshold:
            logging.info(f"Detected {scatters} scatters")
            log_event("scatter", f"Detected {scatters} scatters.")
            stop_spin()
            time.sleep(0.8)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n👋 Exiting AI...")
finally:
    driver.quit()
    print("🛑 Browser closed.")
