# ✅ AI Gambler Custom Config Loader
# File: ai_gambler_customized.py

import json
import os
from pathlib import Path

CONFIG_FILE = Path("ruleset") / "gambler_ruleset.json"
_cached_config = None

def load_custom_config():
    global _cached_config
    if _cached_config is not None:
        return _cached_config

    if not CONFIG_FILE.exists():
        print("⚠️ No ruleset found at:", CONFIG_FILE)
        _cached_config = {}
        return _cached_config

    try:
        with open(CONFIG_FILE, "r") as f:
            _cached_config = json.load(f)
        print("✅ Loaded gambler config:", _cached_config)
        return _cached_config
    except Exception as e:
        print("❌ Failed to load config:", e)
        _cached_config = {}
        return _cached_config

def get_param(key, default=None):
    config = load_custom_config()
    return config.get(key, default)

if __name__ == "__main__":
    rules = load_custom_config()
    print("Current Ruleset Loaded:", rules)
