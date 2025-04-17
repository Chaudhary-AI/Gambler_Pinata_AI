from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is 3 + 7?"}]
)

print(response.choices[0].message.content)
