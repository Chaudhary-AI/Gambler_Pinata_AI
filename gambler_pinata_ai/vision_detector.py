import cv2
import numpy as np
from PIL import ImageGrab
import time

# ✅ Template Files Mapping (Expect full path or ensure these images are in working dir)
TEMPLATE_PATHS = {
    "scatter": "scatter_template",
    "x2": "multiplier_x2_template",
    "x100": "multiplier_x100_template"
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

    return found

# ✅ Main Vision Loop (Trigger logic external)
def scan_screen_for_symbols():
    templates = load_templates()
    if not templates:
        print("❌ No templates loaded. Aborting scan.")
        return []

    screenshot = ImageGrab.grab(bbox=DETECTION_BOX)
    screen_np = np.array(screenshot)
    return detect_templates(screen_np, templates)
