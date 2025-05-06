# 💠 Symbol Value AI Estimator
# File: symbol_value_ai.py

def estimate_symbol_value(symbol: str) -> int:
    values = {
        "scatter": 100,
        "wild": 75,
        "bonus": 50,
        "x100": 100,
        "x50": 50,
        "x20": 20,
    }
    return values.get(symbol.lower(), 0)

if __name__ == "__main__":
    print("💰 Symbol value for 'scatter':", estimate_symbol_value("scatter"))
