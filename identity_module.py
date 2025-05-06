# 🧬 Identity Module
# File: identity_module.py

import uuid
import socket
import logging
import requests

# Logging setup
LOG_FILE = "identity_module.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_identity(identity):
    logging.info(f"Generated Identity: {identity}")

def get_public_ip():
    """
    Fetches the public IP address using an external API.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json().get("ip", "Unknown")
    except Exception as e:
        return f"Error: {e}"

def generate_identity():
    """
    Generates a unique identity for the bot.
    """
    try:
        session_id = str(uuid.uuid4())
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = get_public_ip()
    except Exception as e:
        hostname = "Unknown"
        local_ip = f"Error: {e}"
        public_ip = "Unknown"

    return {
        "session_id": session_id,
        "hostname": hostname,
        "local_ip": local_ip,
        "public_ip": public_ip
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Identity Module")
    parser.add_argument("--log", action="store_true", help="Log the generated identity")
    args = parser.parse_args()

    identity = generate_identity()
    print("🆔 Current Bot Identity:", identity)

    if args.log:
        log_identity(identity)
