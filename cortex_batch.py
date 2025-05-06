# 🧠 Cortex Brain (LLM Interface)
# File: cortex_batch.py

from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import time

# === Load .env API Key ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ API KEY not found in environment.")

openai = OpenAI(api_key=api_key)

# Logging setup
LOG_FILE = "cortex_batch.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_interaction(prompt, response):
    logging.info(f"Prompt: {prompt} | Response: {response}")

def query_brain(prompt):
    """
    Sends a prompt to the OpenAI GPT-4 model and returns the response.
    """
    print("🔍 Asking Brain:", prompt)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        print(f"❌ OpenAI API Error: {e}")
        return "⚠️ Unable to process your request at the moment."

def query_brain_with_retry(prompt, retries=3, delay=2):
    """
    Handles rate limits and retries the query if needed.
    """
    for attempt in range(retries):
        try:
            return query_brain(prompt)
        except openai.error.RateLimitError:
            print(f"⚠️ Rate limit exceeded. Retrying in {delay} seconds...")
            time.sleep(delay)
    return "⚠️ Unable to process your request after multiple attempts."

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cortex Brain LLM Interface")
    parser.add_argument("--prompt", help="Prompt to send to the brain")
    args = parser.parse_args()

    if args.prompt:
        response = query_brain_with_retry(args.prompt)
        print("🧠:", response)
        log_interaction(args.prompt, response)
    else:
        q = input("🤖 Ask Cortex: ")
        response = query_brain_with_retry(q)
        print("🧠:", response)
        log_interaction(q, response)
