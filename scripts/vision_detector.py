# scripts/vision_detector.py

import cv2
import numpy as np
from PIL import ImageGrab
import os

def capture_screen(region=None):
    """Take a screenshot of the whole screen or a region."""
    screen = ImageGrab.grab(bbox=region)
    return cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

def detect_element(template_path, threshold=0.82):
    """
    Detect a single UI element or symbol using template matching.
    Returns position (x, y) if found, else None.
    """
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return None

    screen = capture_screen()
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    if template is None or screen is None:
        print("⚠️ Failed to read template or capture screen.")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"✅ Found {os.path.basename(template_path)} at {max_loc} (Conf: {max_val:.2f})")
        return max_loc
    else:
        print(f"❌ {os.path.basename(template_path)} not found (Conf: {max_val:.2f})")
        return None

def click_element(template_path, threshold=0.82, offset_x=30, offset_y=30):
    """
    Locate and click on a template element if found.
    """
    position = detect_element(template_path, threshold)
    if position:
        try:
            import pyautogui
            x, y = position[0] + offset_x, position[1] + offset_y
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.click()
            print(f"🖱️ Clicked at ({x}, {y})")
            return True
        except Exception as e:
            print(f"⚠️ PyAutoGUI failed: {e}")
    return False
