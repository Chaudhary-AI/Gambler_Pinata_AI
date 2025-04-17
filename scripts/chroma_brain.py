# scripts/chroma_brain.py

# 🧠 Chroma Brain – Source Code Intelligence Module
# Auto-loads code file content, applies labels, and feeds to LLM/memory
# Includes graceful fallback if called standalone

import os
import sys
sys.path.append("path_to_chroma_brain_directory")

def feed_code_file(file_path, label=None):
    """
    Loads a .py or .txt file and returns a structured memory block.
    """
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        return {
            "filename": os.path.basename(file_path),
            "label": label or "unlabeled_code",
            "content": code.strip()
        }

    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
        return None


# 🧪 Standalone mode for testing/debugging
def display_chroma_brain():
    print("🧠 Cortex Mode Activated:")
    print(r"""
   ____ _                            _                 
  / ___| |__   __ _ _ __   __ _  ___| |__   ___  _ __  
 | |   | '_ \ / _` | '_ \ / _` |/ __| '_ \ / _ \| '_ \ 
 | |___| | | | (_| | | | | (_| | (__| | | | (_) | | | |
  \____|_| |_|\__,_|_| |_|\__,_|\___|_| |_|\___/|_| |_|

    """)


if __name__ == "__main__":
    display_chroma_brain()
    print("✨ Chroma Brain Core Loaded (standalone mode)")
    test_file = "symbol_tracker.py"
    result = feed_code_file(test_file, label="test_run")
    print("📦 Memory Block:", result)
