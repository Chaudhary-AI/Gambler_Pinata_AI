# 🧠 Cortex Brain (LLM Interface)
# File: cortex_brain_llm.py

from openai import OpenAI
import os
from dotenv import load_dotenv

# === Load .env API Key ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ API KEY not found in environment.")

openai = OpenAI(api_key=api_key)

def query_brain(prompt):
    print("🔍 Asking Brain:", prompt)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    q = input("🤖 Ask Cortex: ")
    print("🧠:", query_brain(q))
