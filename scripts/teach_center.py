# 🎓 Teach Center - AI Training Stub
# File: teach_center.py

def teach_ai(topic):
    lessons = {
        "scatter": "When 3+ scatters appear, stop spin.",
        "multiplier": "Catch x20 and above. Prioritize x100.",
        "bet": "Don't overbet unless strategy confirms trend."
    }
    print("📚 Lesson:", lessons.get(topic, "Topic not found."))

if __name__ == "__main__":
    teach_ai("scatter")
