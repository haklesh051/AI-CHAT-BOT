import os
import requests
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = Client("groq_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🤖 Send me any message and I'll reply using Groq AI!")

@bot.on_message(filters.text & ~filters.command("start"))
async def ai_chat(client, message):
    user_msg = message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": user_msg}],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        print("Status Code:", res.status_code)
        print("Raw Response:", res.text)

        # Try parsing the response
        data = res.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"❌ Error: {e}"

    await message.reply(reply)

bot.run()
