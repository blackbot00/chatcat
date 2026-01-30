import httpx
from app.config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def ai_reply(system_prompt: str, user_msg: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
