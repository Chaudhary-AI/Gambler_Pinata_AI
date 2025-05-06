# 🚨 Alert Engine for Game Events
# File: alert_engine.py

import os
import platform
import ctypes
import winsound
import logging
import tkinter as tk
from tkinter import messagebox

# Ensure the logs folder exists
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

# Logging setup
LOG_FILE = os.path.join(LOG_FOLDER, "alerts.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def play_beep(frequency=1000, duration=500):
    try:
        if platform.system() == "Windows":
            winsound.Beep(frequency, duration)
        else:
            os.system('printf "\a"')
    except Exception as e:
        print(f"Error playing beep: {e}")

def show_popup(message):
    try:
        if platform.system() == "Windows":
            ctypes.windll.user32.MessageBoxW(0, message, "Gambler Alert", 1)
        else:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showinfo("Gambler Alert", message)
    except Exception as e:
        print(f"Error showing popup: {e}")

def alert_user(msg="⚠️ Special Event Triggered"):
    print("🔔 ALERT:", msg)
    logging.info(msg)
    play_beep()
    show_popup(msg)

if __name__ == "__main__":
    alert_user("Test Alert from alert_engine.py")
