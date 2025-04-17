# 🛠️ Update Requirements from Runtime
# File: update_requirements.py

import subprocess

def freeze_requirements(output="requirements.txt"):
    try:
        with open(output, "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f)
        print(f"✅ Updated {output} with current pip environment.")
    except Exception as e:
        print("❌ Failed to update requirements:", e)

if __name__ == "__main__":
    freeze_requirements()
