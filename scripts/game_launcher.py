# scripts/game_launcher.py

import pyautogui
import time
import os
from PIL import ImageGrab
import cv2
import numpy as np

# Constants
TEMPLATE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTER_PATH = os.path.join(TEMPLATE_FOLDER, "game_poster_start.png")
START_BUTTON_PATH = os.path.join(TEMPLATE_FOLDER, "game_start_button.png")
SCATTER_PATH = os.path.join(TEMPLATE_FOLDER, "scatter_template.png")

# Utility: Capture screen
def capture_screen():
    screen = ImageGrab.grab()
    return cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

# Utility: Detect template on screen
def detect_element(template_filename, threshold=0.8):
    template_path = os.path.join(TEMPLATE_FOLDER, template_filename)
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return None
    
    screen = capture_screen()
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    if template is None or screen is None:
        print("❌ Failed to load screen or template")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"✅ Detected {template_filename} at {max_loc} (confidence: {max_val:.2f})")
        return max_loc
    else:
        print(f"❌ {template_filename} not detected (confidence: {max_val:.2f})")
        return None

# Utility: Click by offset location
def click_at(position, offset_x=30, offset_y=30):
    x = position[0] + offset_x
    y = position[1] + offset_y
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()
    print(f"🖱️ Clicked at {x}, {y}")

# 🎯 Game Launcher Main
def launch_game():
    print("🎮 Starting Game Launcher...")

    # Wait for game poster
    print("🔍 Waiting for game poster...")
    while True:
        pos = detect_element("game_poster_start.png", 0.75)
        if pos:
            print("📌 Game poster found. Waiting for start button...")
            break
        time.sleep(1)

    # Wait for Start button
    while True:
        pos = detect_element("game_start_button.png", 0.75)
        if pos:
            click_at(pos)
            print("🚀 Game start button clicked.")
            break
        time.sleep(1)

    # Optional: Wait for scatter to appear as confirmation
    print("⏳ Verifying game loaded via scatter...")
    for _ in range(10):
        if detect_element("scatter_template.png", 0.7):
            print("🎯 Scatter found — Game Loaded!")
            break
        time.sleep(1)

if __name__ == "__main__":
    launch_game()
