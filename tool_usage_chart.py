import json
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import argparse

# Command-line arguments
parser = argparse.ArgumentParser(description="Tool Usage Chart Generator")
parser.add_argument("--file", default=str(Path.home() / "1man.army" / "memory" / "experience_log.json"), help="Path to the experience log file")
parser.add_argument("--output", default="tool_usage_chart.png", help="Output chart file name")
parser.add_argument("--title", default="🧠 1man.army Tool Usage Chart", help="Chart title")
parser.add_argument("--size", type=int, nargs=2, default=[10, 5], help="Chart size (width, height)")
args = parser.parse_args()

memory_path = Path(args.file)
output_file = args.output

# Load data
try:
    with open(memory_path, "r") as file:
        data = json.load(file)
except Exception as e:
    print(f"⚠️ Memory read failed: {e}")
    data = []

if not data:
    print("⚠️ No data available to generate the chart.")
    exit()

# Count tool usage
tool_counts = Counter()
for entry in data:
    if not isinstance(entry, dict):
        continue
    label = entry.get("label", "unknown")
    tool_counts[label] += 1

# Prepare data for chart
tools = list(tool_counts.keys())
counts = list(tool_counts.values())

# Generate chart
plt.figure(figsize=tuple(args.size))
plt.bar(tools, counts, color="skyblue", edgecolor="black")
plt.xlabel("Tool")
plt.ylabel("Usage Count")
plt.title(args.title)
plt.xticks(rotation=30)
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Save chart
plt.savefig(output_file, format="png")
print(f"📊 Chart saved: {output_file}")
