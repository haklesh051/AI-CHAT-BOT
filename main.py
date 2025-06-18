import os
import requests
from pyrogram import Client, filters

# Get environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Start Pyrogram bot client
bot = Client("groq_ai_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Hello! I'm your AI bot powered by **Groq LLaMA 3.3 70B**.\n"
        "Just send me a message and I'll reply intelligently!"
    )

# Respond to all text messages
@bot.on_message(filters.text & ~filters.command("start"))
async def reply_with_ai(client, message):
    user_input = message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # ✅ latest Groq model
        "messages": [
            {"role": "system", "content": "You are a friendly and intelligent assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.8,  # ✅ More natural/random responses
        "max_tokens": 200
    }

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        print("Status Code:", res.status_code)
        print("Response:", res.text)

        data = res.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        elif "error" in data:
            reply = f"❌ Groq Error: {data['error'].get('message', 'Unknown error')}"
        else:
            reply = "❌ Unexpected response from Groq API."

    except Exception as e:
        reply = f"❌ Exception: {e}"

    await message.reply(reply)

# Run the bot
bot.run()
