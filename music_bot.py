import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

logging.basicConfig(level=logging.INFO)

DOMAINS = ["soundcloud.com","youtube.com","youtu.be","open.spotify.com","spotify.com"]

def is_link(text):
    for d in DOMAINS:
        if d in text:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a music link!")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    user = update.effective_user
    if not is_link(text):
        await update.message.reply_text("Not a music link!")
        return
    name = f"@{user.username}" if user.username else str(user.first_name)
    await context.bot.send_message(chat_id=CHANNEL_ID, text=f"New request from {name}: {text}")
    await update.message.reply_text("Done!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
