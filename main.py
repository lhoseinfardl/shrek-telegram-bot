# 🌟 Shrek Bot - Telegram Bot by @Hoseinfard7
# 🔥 Running with Pyrogram
import os
import random
from pyrogram import Client ,filters
BOT_TOKEN = os.environ.get("BOT_TOKEN", "Token") #your token
API_ID = int(os.environ.get("API_ID", Api_id)) #your api id
API_HASH = os.environ.get("API_HASH", "Api_hash") #your api hash

# ⚙️ Configuring the Bot
plugins = dict(root="plugins")

# 🤖 Creating the Shrek Bot Client
app = Client(
    name="SHeREK",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins
)


# 🚀 Running the bot
if __name__ == "__main__":
    print("🤖 Starting Shrek Bot...")
    app.run()
    print("✨ Rبات روشن شد! Shrek is ready!")