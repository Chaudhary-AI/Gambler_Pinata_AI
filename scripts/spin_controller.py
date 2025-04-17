# scripts/spin_controller.py

import pyautogui
import time
import os
import cv2
import numpy as np
from PIL import ImageGrab

# Path setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPIN_BUTTON = os.path.join(BASE_DIR, "spin_button.png")
SCATTER_TEMPLATE = os.path.join(BASE_DIR, "scatter_template.png")

# Screen capture
def capture_screen():
    screen = ImageGrab.grab()
    return cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

# Template matcher
def detect_template(image_path, threshold=0.8):
    if not os.path.exists(image_path):
        print(f"❌ Template not found: {image_path}")
        return None

    screen = capture_screen()
    template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if template is None or screen is None:
        print("❌ Image read failed.")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"✅ Detected {os.path.basename(image_path)} (conf: {max_val:.2f}) at {max_loc}")
        return max_loc
    return None

# Spin clicker
def press_spin(location, offset=30):
    x = location[0] + offset
    y = location[1] + offset
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()
    print(f"🎯 Spin clicked at {x}, {y}")

# Scatter stopper
def wait_for_scatter_and_stop():
    for i in range(20):  # Max wait
        loc = detect_template(SCATTER_TEMPLATE, threshold=0.75)
        if loc:
            print("💥 Scatter detected! Sending stop command...")
            pyautogui.press("space")
            break
        time.sleep(0.3)

# Auto Spinner
def spin_loop(spins=10):
    print(f"🔄 Starting spin loop for {spins} rounds...")

    for i in range(spins):
        print(f"🎰 Spin #{i+1}")
        spin_btn = detect_template(SPIN_BUTTON, 0.8)
        if spin_btn:
            press_spin(spin_btn)
            wait_for_scatter_and_stop()
        else:
            print("⚠️ Spin button not found.")
        time.sleep(2.5)

if __name__ == "__main__":
    spin_loop(spins=5)
