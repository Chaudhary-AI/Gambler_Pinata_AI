# 🧠 Cortex Brain (LLM Interface)
# File: cortex_brain_llm.py

from shared_brain import ask_brain

if __name__ == "__main__":
    q = input("🤖 Ask Cortex: ")
    print("🧠:", ask_brain(q))
