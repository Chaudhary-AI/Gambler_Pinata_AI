import cv2
import numpy as np
from PIL import ImageGrab
import os
import time
import logging

# Logging setup
LOG_FILE = "vision_detector.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_action(message):
    logging.info(message)

# ✅ Template Files Mapping (Configurable via environment variables)
TEMPLATE_PATHS = {
    "scatter": os.getenv("SCATTER_TEMPLATE", "scatter_template.png"),
    "x2": os.getenv("MULTIPLIER_X2_TEMPLATE", "multiplier_x2_template.png"),
    "x100": os.getenv("MULTIPLIER_X100_TEMPLATE", "multiplier_x100_template.png")
}

# ✅ Detection Settings
DETECTION_BOX = (500, 300, 1200, 700)  # Adjust based on slot area
MATCH_THRESHOLD = 0.75  # Confidence level for match

# ✅ Load Templates (grayscale + edge)
def load_templates():
    templates = {}
    for name, path in TEMPLATE_PATHS.items():
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"❌ Error loading template: {path}")
            log_action(f"Error loading template: {path}")
            continue
        templates[name] = cv2.Canny(img, 50, 150)
    return templates

# ✅ Detect matching template in screen
def detect_templates(screen_img, templates):
    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(screen_gray, 50, 150)
    found = []

    for name, tmpl in templates.items():
        result = cv2.matchTemplate(edges, tmpl, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= MATCH_THRESHOLD)
        if len(loc[0]) > 0:
            found.append(name)
            print(f"✅ Detected: {name.upper()}")
            log_action(f"Detected: {name.upper()}")

    return found

# ✅ Main Vision Loop (Trigger logic external)
def scan_screen_for_symbols():
    templates = load_templates()
    if not templates:
        print("❌ No templates loaded. Aborting scan.")
        log_action("No templates loaded. Scan aborted.")
        return []

    try:
        screenshot = ImageGrab.grab(bbox=DETECTION_BOX)
    except Exception as e:
        print(f"❌ Screen capture failed: {e}")
        log_action(f"Screen capture failed: {e}")
        return []

    screen_np = np.array(screenshot)
    return detect_templates(screen_np, templates)

# ✅ Continuous Scanning with Timeout
def scan_screen_with_timeout(timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        detected = scan_screen_for_symbols()
        if detected:
            print(f"✅ Detected: {detected}")
            break
        time.sleep(1)
    else:
        print("⏳ Timeout: No symbols detected.")
        log_action("Timeout: No symbols detected.")
