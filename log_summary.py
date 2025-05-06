import json

LOG_FILE = "experience_log.json"

def generate_summary(log_file):
    try:
        with open(log_file, "r") as f:
            logs = json.load(f)

        summary = {"scatter": 0, "win": 0, "loss": 0, "multiplier": 0}
        for log in logs:
            event_type = log.get("type")
            if event_type in summary:
                summary[event_type] += 1

        print("Event Summary:", summary)
        return summary

    except FileNotFoundError:
        print(f"⚠️ Log file not found: {log_file}")
    except json.JSONDecodeError:
        print(f"⚠️ Log file is not a valid JSON: {log_file}")

# Example usage
if __name__ == "__main__":
    generate_summary(LOG_FILE)