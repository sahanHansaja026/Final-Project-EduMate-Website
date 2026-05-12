import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(message: str):
    url = "https://openrouter.ai/api/v1/chat/completions"

    if not OPENROUTER_API_KEY:
        return "API Error: Missing OPENROUTER_API_KEY in .env"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "MyAIApp"
    }

    data = {
        "model": "meta-llama/llama-3.1-8b-instruct",  # safe free model
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()

        # 🔍 DEBUG (optional - remove later)
        print("OPENROUTER RESPONSE:", result)

        # ✅ handle API errors safely
        if "choices" not in result:
            return f"API Error: {result.get('error', result)}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Request Error: {str(e)}"