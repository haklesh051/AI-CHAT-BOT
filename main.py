import os
import requests
from pyrogram import Client, filters

# Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Pyrogram Client
bot = Client("groq_ai_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Hello! I'm your AI bot powered by **Groq - LLaMA 3.3 70B**.\n\n"
        "Just send me any message and I'll respond with AI!"
    )

# AI Reply to Text Messages
@bot.on_message(filters.text & ~filters.command("start"))
async def reply_with_ai(client, message):
    user_input = message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # ✅ Updated to new supported model
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
        print("Payload sent:", payload)
        print("Status Code:", res.status_code)
        print("Response Text:", res.text)

        data = res.json()

        # Check if choices exist in response
        if "choices" not in data:
            reply = f"❌ Error: 'choices' not found.\n\nResponse:\n{data}"
        else:
            reply = data["choices"][0]["message"]["content"]

    except Exception as e:
        reply = f"❌ Exception: {e}"

    await message.reply(reply)

# Run the bot
bot.run()
