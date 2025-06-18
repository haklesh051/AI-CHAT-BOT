import os
import time
import requests
from pyrogram import Client, filters

# Get from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Start bot
bot = Client("groq_ai_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Hello! I'm an AI bot powered by Groq LLaMA 3.3 70B.\n"
        "Send me any message and I'll reply using AI.\n\n"
        "Note: On free plan, I may pause if too many messages are sent quickly."
    )

# AI chat handler
@bot.on_message(filters.text & ~filters.command("start"))
async def ai_reply(client, message):
    user_input = message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a friendly, intelligent assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.8,
        "max_tokens": 200
    }

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        # Rate limit error (429)
        if res.status_code == 429:
            await message.reply("⚠️ Rate limit reached. Waiting 3 seconds...")
            time.sleep(3)
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )

        data = res.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        elif "error" in data:
            reply = f"❌ Groq Error: {data['error'].get('message', 'Unknown error')}"
        else:
            reply = "❌ Unexpected response from Groq API."

    except Exception as e:
        reply = f"❌ Exception occurred: {e}"

    await message.reply(reply)

# Run bot
bot.run()
