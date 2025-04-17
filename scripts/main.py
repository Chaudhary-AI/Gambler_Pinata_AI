# scripts/main.py

from game_launcher import launch_game
import sys
sys.path.append("path_to_chroma_brain_directory")
from spin_controller import start_spin
from symbol_tracker import check_for_scatters
from chroma_brain import feed_code_file
import time
import logging

logging.basicConfig(
    filename="gambler_ai.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MAX_SPINS = 50

def run_gambler_ai():
    print("\n🎰 INITIATING PINATA GAMBLER AI ENGINE...\n")

    # Step 1: Launch game
    launch_game()

    # Step 2: Begin loop
    for spin_num in range(1, MAX_SPINS + 1):
        print(f"\n🔁 Spin Cycle: {spin_num}")

        if check_for_scatters():
            print("🎯 4+ Scatters Detected — Game will stop now.")
            break

        if not start_spin():
            print("⚠️ Spin button not detected — Breaking loop.")
            break

        time.sleep(2.5)

    print("\n🧠 SESSION ENDING. Feeding memory to brain...")
    feed_code_file(__file__, label="main_control")

    print("✅ Gambler AI Session Complete.")


if __name__ == "__main__":
    run_gambler_ai()
