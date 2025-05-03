# 🖱️ Pixel Click AI
# File: pixel_click_ai.py

import pyautogui
import time

def click_coordinates(coords=(1000, 600), delay=1):
    print(f"🎯 Clicking at: {coords}")
    pyautogui.moveTo(*coords)
    pyautogui.click()
    time.sleep(delay)

if __name__ == "__main__":
    click_coordinates()
