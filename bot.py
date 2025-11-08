import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
from telegram.request import HTTPXRequest

# =============== CONFIGURATION ===============

TELEGRAM_TOKEN = "8344196577:AAFWHqALD_0k2wG75TCYFpu9TqjjaakCOtM"  # your bot token
OPENAI_API_KEY = "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"  # replace with your real OpenAI key

# Optional proxy (if Telegram is blocked in your country)
# Comment this line if not needed:
request = HTTPXRequest(proxy="socks5://68.71.247.130:4145")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Build Telegram app
app = (
    ApplicationBuilder()
    .token(TELEGRAM_TOKEN)
    .request(request)
    .build()
)

# =============== BOT COMMANDS ===============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I’m your AI bot.\n"
        "Send me any message and I’ll reply intelligently using GPT!"
    )

# =============== MESSAGE HANDLER ===============

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
        )

        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("⚠️ Error: " + str(e))

# =============== HANDLERS ===============

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# =============== RUN BOT ===============

print("🤖 Bot is running... Press Ctrl+C to stop.")
app.run_polling()
