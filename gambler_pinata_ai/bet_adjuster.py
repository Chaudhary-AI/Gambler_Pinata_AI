from shared_brain import ask_brain
# 🎚️ Bet Adjuster Engine
# File: bet_adjuster.py

import random
import pyautogui

def adjust_bet(mode="auto"):
    if mode == "auto":
        decision = random.choice(["increase", "decrease", "hold"])
    else:
        decision = mode

    if decision == "increase":
        pyautogui.moveTo(1200, 500)
        pyautogui.click()
        print("⬆️ Bet Increased")
    elif decision == "decrease":
        pyautogui.moveTo(800, 500)
        pyautogui.click()
        print("⬇️ Bet Decreased")
    else:
        print("⚖️ Bet Held")

if __name__ == "__main__":
    adjust_bet()

