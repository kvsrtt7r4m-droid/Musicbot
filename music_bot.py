import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

ALLOWED_DOMAINS = ["soundcloud.com","youtube.com","youtu.be","music.youtube.com","open.spotify.com","spotify.com","music.yandex.ru"]

def is_valid_music_link(text):
    for domain in ALLOWED_DOMAINS:
        if domain in text:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Привет, {user.first_name}! Отправь ссылку на трек и я передам её диджею!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""
    if not is_valid_music_link(text):
        await update.message.reply_text("Это не ссылка на музыку. Отправь ссылку с YouTube, SoundCloud или Spotify.")
        return
    username = f"@{user.username}" if user.username else f"{user.first_name}"
    await context.bot.send_message(chat_id=CHANNEL_ID, text=f"Новая заявка!\nОт: {username}\nСсылка: {text}")
    await update.message.reply_text("Готово! Трек отправлен диджею.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
