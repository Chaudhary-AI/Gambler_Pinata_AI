# 🧠 Cortex Brain (LLM Interface)
# File: cortex_brain_llm.py

from shared_brain import ask_brain
import logging

# Logging setup
LOG_FILE = "cortex_brain_llm.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_interaction(prompt, response):
    logging.info(f"Prompt: {prompt} | Response: {response}")

def ask_brain_safe(prompt):
    """
    Safely calls the ask_brain function with error handling.
    """
    try:
        return ask_brain(prompt)
    except Exception as e:
        return f"⚠️ Unable to process your request: {e}"

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cortex Brain LLM Interface")
    parser.add_argument("--prompt", help="Prompt to send to the brain")
    args = parser.parse_args()

    if args.prompt:
        response = ask_brain_safe(args.prompt)
        print("🧠:", response)
        log_interaction(args.prompt, response)
    else:
        q = input("🤖 Ask Cortex: ")
        response = ask_brain_safe(q)
        print("🧠:", response)
        log_interaction(q, response)
