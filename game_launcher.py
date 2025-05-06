import pyautogui
import time
import os
from PIL import ImageGrab
import cv2
import numpy as np
import logging

# Logging setup
LOG_FILE = "game_launcher.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Constants
TEMPLATE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
LOGIN_BUTTON_PATH = os.path.join(TEMPLATE_FOLDER, "login_button.png")
GAME_ICON_PATH = os.path.join(TEMPLATE_FOLDER, "game_icon.png")
POSTER_PATH = os.path.join(TEMPLATE_FOLDER, "game_poster_start.png")
START_BUTTON_PATH = os.path.join(TEMPLATE_FOLDER, "game_start_button.png")
SCATTER_PATH = os.path.join(TEMPLATE_FOLDER, "scatter_template.png")

def log_action(message):
    logging.info(message)

# Utility: Capture screen
def capture_screen():
    screen = ImageGrab.grab()
    return cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

# Utility: Detect template on screen
def detect_element(template_path, threshold=0.8):
    if not os.path.exists(template_path):
        print(f"⚠️ Warning: Template not found at {template_path}")
        log_action(f"Template not found: {template_path}")
        return None
    
    screen = capture_screen()
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    if template is None or screen is None:
        print("❌ Failed to load screen or template")
        log_action("Failed to load screen or template")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"✅ Detected {template_path} at {max_loc} (confidence: {max_val:.2f})")
        log_action(f"Detected {template_path} at {max_loc} (confidence: {max_val:.2f})")
        return max_loc
    else:
        print(f"❌ {template_path} not detected (confidence: {max_val:.2f})")
        log_action(f"{template_path} not detected (confidence: {max_val:.2f})")
        return None

# Utility: Click by offset location
def click_at(position, offset_x=30, offset_y=30):
    x = position[0] + offset_x
    y = position[1] + offset_y
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()
    print(f"🖱️ Clicked at {x}, {y}")
    log_action(f"Clicked at {x}, {y}")

# Utility: Wait for element
def wait_for_element(template_path, threshold=0.8, timeout=30):
    print(f"🔍 Waiting for {template_path}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        pos = detect_element(template_path, threshold)
        if pos:
            return pos
        time.sleep(1)
    return None

# Step 1: Login to the game
def login_to_game(username, password):
    print("🔐 Logging in...")
    pos = detect_element(LOGIN_BUTTON_PATH, 0.8)
    if not pos:
        print("❌ Login button not found.")
        log_action("Login button not found.")
        return False
    click_at(pos)

    pyautogui.write(username, interval=0.1)
    pyautogui.press("tab")
    pyautogui.write(password, interval=0.1)
    pyautogui.press("enter")
    print("✅ Login credentials entered.")
    log_action("Login credentials entered.")
    time.sleep(5)
    return True

# Step 2: Select the game
def select_game():
    print("🎮 Selecting game...")
    pos = detect_element(GAME_ICON_PATH, 0.8)
    if not pos:
        print("❌ Game icon not found.")
        log_action("Game icon not found.")
        return False
    click_at(pos)
    print("✅ Game selected.")
    log_action("Game selected.")
    time.sleep(5)
    return True

# Step 3: Launch the game
def launch_game():
    print("🎮 Starting Game Launcher...")
    pos = wait_for_element(POSTER_PATH, 0.75, timeout=30)
    if not pos:
        print("❌ Game poster not found. Exiting...")
        log_action("Game poster not found. Exiting...")
        return

    pos = wait_for_element(START_BUTTON_PATH, 0.75, timeout=30)
    if not pos:
        print("❌ Start button not found. Exiting...")
        log_action("Start button not found. Exiting...")
        return
    click_at(pos)
    print("🚀 Game start button clicked.")
    log_action("Game start button clicked.")

    print("⏳ Verifying game loaded via scatter...")
    for _ in range(10):
        if detect_element(SCATTER_PATH, 0.7):
            print("🎯 Scatter found — Game Loaded!")
            log_action("Scatter found — Game Loaded!")
            break
        time.sleep(1)

if __name__ == "__main__":
    USERNAME = "your_username"
    PASSWORD = "your_password"

    if login_to_game(USERNAME, PASSWORD):
        if select_game():
            launch_game()
