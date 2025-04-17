# 🔐 Memory Encryptor
# File: memory_encryptor.py

from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path("memory/key.key")
DATA_FILE = Path("memory/experience_log.json")

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("🔑 Encryption key generated.")

def encrypt_data():
    if not KEY_FILE.exists():
        print("⚠️ No key found. Generating new one...")
        generate_key()

    key = open(KEY_FILE, "rb").read()
    f = Fernet(key)

    if not DATA_FILE.exists():
        print("⚠️ No memory file to encrypt.")
        return

    data = open(DATA_FILE, "rb").read()
    encrypted = f.encrypt(data)
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted)
    print("🔐 Memory encrypted.")

if __name__ == "__main__":
    encrypt_data()
