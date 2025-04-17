from shared_brain import ask_brain
# 🔀 MERGED: AI-Gambler + Cortex Brain (LLM-Augmented)
# File: ai_gambler.py

import time
import pyautogui
import easyocr
import cv2
import numpy as np
from PIL import ImageGrab
import random
import pandas as pd
import keyboard
import mouse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import json
from pathlib import Path
import os

# === OCR Setup ===
reader = easyocr.Reader(['en'])
DETECTION_BOX = (500, 300, 1200, 700)

# === Load Templates (CV Mode) ===
def load_template(file_name):
    if not os.path.exists(file_name):
        print(f"❌ Template not found: {file_name}")
        return None
    return cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

scatter_template = load_template("scatter_template.png")
multiplier_template = load_template("multiplier_template.png")

if scatter_template is None or multiplier_template is None:
    print("❌ ERROR: Template images missing. Place them in the same directory.")
    exit()

# === Memory Setup ===
MEMORY_FILE = Path("memory") / "experience_log.json"
if not MEMORY_FILE.exists():
    os.makedirs(MEMORY_FILE.parent, exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

from dotenv import load_dotenv
load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_brain(question):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
    docs = memory[-3:]
    context = "\n\n".join([d.get("output_snippet", "") for d in docs])
    prompt = f"""You are an intelligent gambling agent.
Use memory logs:
{context}
Question: {question}
Answer with one clear action.
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# === Selenium Start ===
GAME_URL = "https://m.56myu5u3v.com/1492288/index.html?..."
firefox_options = Options()
firefox_options.add_argument("--start-maximized")
driver = webdriver.Firefox(options=firefox_options)
driver.get(GAME_URL)
time.sleep(5)

try:
    start_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'GET STARTED')]"))
    )
    start_button.click()
except:
    print("⚠️ No Start Button Found")

# === Core Functions ===
def detect_elements():
    screenshot = ImageGrab.grab(bbox=DETECTION_BOX)
    img_np = np.array(screenshot)
    results = reader.readtext(img_np)
    detected_text = ' '.join([res[1] for res in results]).lower()

    scatter_count = detected_text.count("scatter")
    if scatter_count >= 3:
        print(f"🎟️ {scatter_count} Scatters! STOP!")
        pyautogui.press("space")
        return True

    for n in range(2, 101):
        if f"x{n}" in detected_text:
            print(f"💰 Multiplier x{n} Detected!")
            pyautogui.press("space")
            return True
    return False

def decide_next_action():
    try:
        response = ask_brain("Should I increase, decrease, or hold the bet?")
        if "increase" in response:
            pyautogui.moveTo(1200, 500)
            pyautogui.click()
            print("⬆️ AI: Increase Bet")
        elif "decrease" in response:
            pyautogui.moveTo(800, 500)
            pyautogui.click()
            print("⬇️ AI: Decrease Bet")
        else:
            print("⚖️ AI: Hold Bet")
    except Exception as e:
        print("🧠 Brain Error:", e)

def play_game():
    print("🚀 Cortex-Gambler STARTED!")
    while True:
        pyautogui.moveTo(1000, 600)
        pyautogui.click()
        print("🎰 SPIN!")
        time.sleep(3)

        if detect_elements():
            print("🛑 Element detected, stopping.")
            time.sleep(2)

        if random.randint(1, 4) == 2:
            decide_next_action()

        if keyboard.is_pressed("space") or mouse.is_pressed("left"):
            print("🔴 Manual Stop")
            pyautogui.press("space")
            break
        time.sleep(2)

if __name__ == "__main__":
    play_game()

