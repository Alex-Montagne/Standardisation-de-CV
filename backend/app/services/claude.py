import os
import requests
from app.core.config import settings

def ask_claude(text: str) -> dict:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": settings.CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    data = {
        "model": settings.CLAUDE_MODEL,
        "max_tokens": 800,
        "messages": [
            {"role": "user", "content": f"Standardise ce CV en JSON:\n{text}"}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    json_result = response.json()

    import json
    return json.loads(json_result['content'][0]['text'])