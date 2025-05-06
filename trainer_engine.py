from shared_brain import ask_brain
import json
from pathlib import Path
from collections import Counter

MEMORY_FILE = Path("c:/Users/Yenkh/1-ManArmy/OneDrive/professorai/Gambler_Pinata_AI/experience_log.json")
OUTPUT_FILE = Path("memory") / "training_insights.json"

if not MEMORY_FILE.exists():
    print("⚠️ No experience log found.")
    exit()

with open(MEMORY_FILE, "r") as f:
    memory = json.load(f)

# --- Training Analysis ---
summary = {
    "total_entries": len(memory),
    "scatter_triggers": 0,
    "multiplier_hits": Counter(),
    "loss_streaks": 0
}

streak = 0
for entry in memory:
    output = entry.get("output_snippet", "").lower()
    if "scatter" in output:
        summary["scatter_triggers"] += 1
    if "x" in output:
        for tag in ["x20", "x50", "x100"]:
            if tag in output:
                summary["multiplier_hits"][tag] += 1
    if "loss" in output:
        streak += 1
    else:
        if streak >= 3:
            summary["loss_streaks"] += 1
        streak = 0

summary["multiplier_hits"] = dict(summary["multiplier_hits"])

with open(OUTPUT_FILE, "w") as f:
    json.dump(summary, f, indent=2)

print("✅ Training summary saved:", OUTPUT_FILE)

