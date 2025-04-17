# ✅ AI Gambler Custom Config Loader
# File: ai_gambler_customized.py

import json
import os
from pathlib import Path

CONFIG_FILE = Path("ruleset") / "gambler_ruleset.json"

def load_custom_config():
    if not CONFIG_FILE.exists():
        print("⚠️ No ruleset found at:", CONFIG_FILE)
        return {}

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        print("✅ Loaded gambler config:", config)
        return config
    except Exception as e:
        print("❌ Failed to load config:", e)
        return {}

def get_param(key, default=None):
    config = load_custom_config()
    return config.get(key, default)

if __name__ == "__main__":
    rules = load_custom_config()
    print("Current Ruleset Loaded:", rules)
