# 🎛️ Cortex UI Terminal Interface
# File: cortex_ui.py

def launch_ui():
    print("🧠 Cortex Interface")
    print("====================")
    print("1. Start AI Gambler")
    print("2. Toggle Hot Mode")
    print("3. Trigger Report")
    print("4. Exit")

    choice = input("Enter choice: ")
    if choice == "1":
        print("🚀 Launching...")
    elif choice == "2":
        print("🔥 Hot Mode Enabled")
    elif choice == "3":
        print("📊 Generating Report")
    else:
        print("👋 Exiting")

if __name__ == "__main__":
    launch_ui()
