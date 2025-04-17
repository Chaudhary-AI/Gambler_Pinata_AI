# 🚨 Alert Engine for Game Events
# File: alert_engine.py

import os
import platform
import ctypes
import winsound

def play_beep():
    if platform.system() == "Windows":
        winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms
    else:
        os.system('printf "\a"')  # Terminal beep for Unix

def show_popup(message):
    if platform.system() == "Windows":
        ctypes.windll.user32.MessageBoxW(0, message, "Gambler Alert", 1)
    else:
        print("🔔", message)

def alert_user(msg="⚠️ Special Event Triggered"):
    print("🔔 ALERT:", msg)
    play_beep()
    show_popup(msg)

if __name__ == "__main__":
    alert_user("Test Alert from alert_engine.py")
