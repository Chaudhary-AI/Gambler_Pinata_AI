# scripts/chroma_brain.py

# 🧠 Chroma Brain – Source Code Intelligence Module
# Auto-loads code file content, applies labels, and feeds to LLM/memory
# Includes graceful fallback if called standalone

import os
import sys
import logging
from pathlib import Path

# Logging setup
LOG_FILE = "chroma_brain.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Add the current directory to sys.path dynamically
sys.path.append(str(Path(__file__).resolve().parent))

def log_action(message):
    logging.info(message)

def feed_code_file(file_path, label=None):
    """
    Loads a .py or .txt file and returns a structured memory block.
    """
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        log_action(f"File not found: {file_path}")
        return None

    if not file_path.endswith(('.py', '.txt')):
        print(f"❌ Unsupported file type: {file_path}")
        log_action(f"Unsupported file type: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        memory_block = {
            "filename": os.path.basename(file_path),
            "label": label or "unlabeled_code",
            "content": code.strip()
        }
        log_action(f"Processed file: {file_path} with label: {label}")
        return memory_block

    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
        log_action(f"Error reading {file_path}: {e}")
        return None

def save_to_memory_block(memory_block):
    """
    Placeholder for saving memory block to a database or external system.
    """
    print(f"📦 Saving memory block: {memory_block}")
    log_action(f"Saved memory block: {memory_block}")

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
    import argparse

    parser = argparse.ArgumentParser(description="Chroma Brain Source Code Processor")
    parser.add_argument("--file", help="Path to the file to process")
    parser.add_argument("--label", help="Label for the file")
    args = parser.parse_args()

    if args.file:
        result = feed_code_file(args.file, label=args.label)
        print("📦 Memory Block:", result)
        if result:
            save_to_memory_block(result)
    else:
        display_chroma_brain()
        print("✨ Chroma Brain Core Loaded (standalone mode)")
