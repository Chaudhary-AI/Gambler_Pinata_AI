# Gambler_Pinata_AI

**A simulation and testing platform for probabilistic decision-making bots, inspired by gambling scenarios.**

---

## 🧠 Overview

This project simulates and tests AI agents in gambling-like environments (like slot machines or piñata bashing) to evaluate decision-making under uncertainty. It’s built for developers, researchers, and curious minds interested in AI behavior in high-risk, probabilistic systems.

---

## 📂 Project Structure

```

Gambler\_Pinata\_AI/
│
├── assets/                 # Images, videos, and media files
│
├── data/                   # Game simulation logs and result data
│
├── environments/           # Definitions of gambling environments (slots, piñatas, etc.)
│   └── **init**.py
│   └── slot\_machine.py     # Slot machine logic
│   └── pinata\_game.py      # Piñata-style game logic
│
├── bots/                   # AI agents with various strategies
│   └── **init**.py
│   └── random\_bot.py       # Bot that acts randomly
│   └── greedy\_bot.py       # Bot that exploits best-known option
│   └── bayesian\_bot.py     # Bot using Bayesian updates
│
├── core/                   # Core simulation engine
│   └── **init**.py
│   └── simulator.py        # Runs simulations
│   └── tracker.py          # Tracks game state & rewards
│
├── tests/                  # Unit tests for bots and environments
│
├── main.py                 # CLI to run simulations
├── README.md               # Project documentation (you are here)
└── requirements.txt        # Python dependencies

````

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Chaudhary-AI/Gambler_Pinata_AI.git
   cd Gambler_Pinata_AI
````

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run a default simulation:

```bash
python main.py
```

Example with arguments (optional):

```bash
python main.py --bot bayesian_bot --env slot_machine --episodes 1000
```

---

## 📊 Bots

* **RandomBot**: Selects actions uniformly at random.
* **GreedyBot**: Chooses action with highest known payoff.
* **BayesianBot**: Updates beliefs based on outcomes and acts probabilistically.

---

## 🎮 Environments

* **Slot Machine**: N-armed bandit simulation.
* **Piñata Game**: Discrete-action reward environment with penalties.

---

## 🧪 Testing

Run all unit tests:

```bash
pytest tests/
```

---

## 📬 Contact

Made with ❤️ by [Chaudhary AI](https://github.com/Chaudhary-AI)
