import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

ALLOWED_DOMAINS = [
    "soundcloud.com",
    "youtube.com",
    "youtu.be",
    "music.youtube.com",
    "open.spotify.com",
    "spotify.com",
    "music.yandex.ru",
    "yandex.ru/music",
]

def is_valid_music_link(text: str) -> bool:
    for domain in ALLOWED_DOMAINS:
        if domain in text:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "🎵 Хочешь заказать трек?\n\n"
        "Просто отправь ссылку на песню с:\n"
        "• SoundCloud\n"
        "• YouTube / YouTube Music\n"
        "• Spotify\n"
        "• Яндекс Музыка\n\n"
        "И я передам её диджею! 🎧"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""

    if not is_valid_music_link(text):
        await update.message.reply_text(
            "❌ Это не похоже на ссылку
