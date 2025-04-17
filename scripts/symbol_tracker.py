# scripts/symbol_tracker.py

import time
import cv2
import numpy as np
from PIL import ImageGrab

SCATTER_TEMPLATE = "assets/scatter_template.png"
SCATTER_THRESHOLD = 0.85

def capture_screen(region=None):
    screen = ImageGrab.grab(bbox=region)
    screen_np = np.array(screen)
    return cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

def load_template(path):
    template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if template is None:
        raise FileNotFoundError(f"❌ Template not found: {path}")
    return template

def detect_scatter_symbols():
    screen = capture_screen()
    template = load_template(SCATTER_TEMPLATE)

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= SCATTER_THRESHOLD)
    count = len(zip(*locations[::-1]))  # List of match points

    return count

def check_for_scatters():
    try:
        count = detect_scatter_symbols()
        print(f"✨ Scatter Symbols Found: {count}")
        return count >= 4
    except FileNotFoundError as e:
        print(e)
        return False
