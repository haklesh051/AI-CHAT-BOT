import os
import requests
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = Client("groq_ai_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Hello! I'm your Groq AI Bot using the latest Llama 3 model.\n"
        "Send me any message and I'll reply intelligently."
    )

@bot.on_message(filters.text & ~filters.command("start"))
async def reply_with_ai(client, message):
    user_input = message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # <-- Updated model here
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        print("Status Code:", res.status_code)
        print("Response Text:", res.text)

        data = res.json()
        if "choices" not in data:
            reply = f"❌ Error: 'choices' not found in response.\nFull response:\n{data}"
        else:
            reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"❌ Exception: {e}"

    await message.reply(reply)

bot.run()
