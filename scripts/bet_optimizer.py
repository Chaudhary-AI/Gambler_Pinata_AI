# 🧠 Bet Optimizer Logic
# File: bet_optimizer.py

import random
import time

def optimize_bet(history):
    if not history:
        return "hold"
    
    wins = sum(1 for r in history if r == "win")
    losses = sum(1 for r in history if r == "lose")
    
    if wins > losses:
        return "increase"
    elif losses > wins:
        return "decrease"
    return "hold"

if __name__ == "__main__":
    fake_history = [random.choice(["win", "lose"]) for _ in range(10)]
    decision = optimize_bet(fake_history)
    print("Optimized decision:", decision)
