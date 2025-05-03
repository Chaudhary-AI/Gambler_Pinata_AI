# 🧬 Identity Module
# File: identity_module.py

import uuid
import socket

def generate_identity():
    return {
        "session_id": str(uuid.uuid4()),
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname())
    }

if __name__ == "__main__":
    identity = generate_identity()
    print("🆔 Current Bot Identity:", identity)
