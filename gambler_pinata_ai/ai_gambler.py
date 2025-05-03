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

# ==== [ Browser Launcher ] ====
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

TACTIC_PATH = Path("ruleset") / "tactic.json"
DEFAULT_THRESHOLD = 3
DEFAULT_URL = "https://m.56myu5u3v.com/1492288/index.html?ot=AF64C68B-E04E-45E5-A4A3-3D7C2A34463D&btt=1&ops=gt61741327361818-gt6ta65three8three&l=en&or=16ijqjys%3D56cok5k3l%3Dsec&__hv=2fMEUCIQDbgG73K4Fi7e2rKTQmeu5nc7nXeP8M3TX0eQszDEz9RwIgUkVS0II960QvGA53WK%2FUTO8jXqGfAdhgW2KyBpFp54o%3D"  # 🔁 Replace with real game URL

# === Load Config ===
try:
    with open(TACTIC_PATH, "r") as f:
        tactic = json.load(f)
        scatter_threshold = tactic.get("scatter_stop_threshold", DEFAULT_THRESHOLD)
        game_url = tactic.get("url", DEFAULT_URL)
except Exception:
    print(f"⚠️ Failed to load tactic.json, using defaults")
    scatter_threshold = DEFAULT_THRESHOLD
    game_url = DEFAULT_URL

# === Launch Browser ===
print("🌐 Launching Game in Firefox...")
options = FirefoxOptions()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get(game_url)
driver.maximize_window()
print(f"✅ Game loaded: {game_url}")

time.sleep(10)  # Wait for the game to fully load

# === Load Scatter Template ===
SCATTER_TEMPLATE_PATH = "scripts/scatter_template"
if not os.path.exists(SCATTER_TEMPLATE_PATH):
    print(f"❌ Scatter template not found at {SCATTER_TEMPLATE_PATH}")
    exit()
scatter_template = cv2.imread(SCATTER_TEMPLATE_PATH, 0)
w, h = scatter_template.shape[::-1]

# === Define Region for Game Screen ===
REGION = (500, 300, 1200, 700)  # Adjust if needed

def grab_game_screen():
    screen = ImageGrab.grab(bbox=REGION)
    return cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)

def count_scatters(frame):
    result = cv2.matchTemplate(frame, scatter_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.78)
    found = set()
    for pt in zip(*loc[::-1]):
        found.add(pt)
    return len(found)

def stop_spin():
    print("🛑 Spin stopped!")
    pyautogui.press("space")  # Update if your stop key is different

# === Game Watch Loop ===
print(f"🎰 AI Active | Scatter Trigger = {scatter_threshold}+")
try:
    while True:
        frame = grab_game_screen()
        scatters = count_scatters(frame)
        print(f"[👁️] Scatters: {scatters}", end="\r")

        if scatters >= scatter_threshold:
            stop_spin()
            time.sleep(0.8)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n👋 AI Exited")
    driver.quit()