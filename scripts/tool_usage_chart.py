import json
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

memory_path = Path.home() / "1man.army" / "memory" / "experience_log.json"

try:
    with open(memory_path, "r") as file:
        data = json.load(file)
except Exception as e:
    print(f"Memory read failed: {e}")
    data = []

tool_counts = Counter()
for entry in data:
    label = entry.get("label", "unknown")
    tool_counts[label] += 1

tools = list(tool_counts.keys())
counts = list(tool_counts.values())

plt.figure(figsize=(10, 5))
plt.bar(tools, counts)
plt.xlabel("Tool")
plt.ylabel("Usage Count")
plt.title("🧠 1man.army Tool Usage Chart")
plt.xticks(rotation=30)
plt.tight_layout()
plt.grid(True)

plt.savefig("tool_usage_chart.png")
print("📊 Chart saved: tool_usage_chart.png")
