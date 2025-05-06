# 🧠 Bet Optimizer Logic
# File: bet_optimizer.py

import random
import logging

# Logging setup
logging.basicConfig(filename="bet_optimizer.log", level="INFO", format="%(asctime)s - %(message)s")

def log_decision(history, decision):
    logging.info(f"History: {history} | Decision: {decision}")

def optimize_bet(history):
    if not history:
        return "hold", "low"
    
    wins = sum(1 for r in history if r == "win")
    losses = sum(1 for r in history if r == "lose")
    
    if wins > losses:
        confidence = "high" if wins - losses > 2 else "medium"
        decision = "increase"
    elif losses > wins:
        confidence = "high" if losses - wins > 2 else "medium"
        decision = "decrease"
    else:
        confidence = "low"
        decision = random.choice(["increase", "decrease", "hold"])  # Tie-breaker logic

    log_decision(history, decision)
    return decision, confidence

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Bet Optimizer")
    parser.add_argument("--history", nargs="+", help="Betting history (e.g., win lose win)")
    args = parser.parse_args()

    if args.history:
        decision, confidence = optimize_bet(args.history)
        print(f"Optimized decision: {decision} (Confidence: {confidence})")
    else:
        # Generate fake history for testing
        fake_history = [random.choice(["win", "lose"]) for _ in range(10)]
        decision, confidence = optimize_bet(fake_history)
        print(f"Fake history: {fake_history}")
        print(f"Optimized decision: {decision} (Confidence: {confidence})")
