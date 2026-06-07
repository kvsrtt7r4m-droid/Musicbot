import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Токен и ID берутся из переменных окружения Railway
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
            "❌ Это не похоже на ссылку на музыку.\n\n"
            "Пожалуйста, отправь ссылку с SoundCloud, YouTube, Spotify или Яндекс Музыки."
        )
        return

    username = f"@{user.username}" if user.username else f"{user.first_name} (ID: {user.id})"

    message = (
        f"🎵 *Новая заявка на трек!*\n\n"
        f"👤 От: {username}\n"
        f"🔗 Ссылка: {text}"
    )

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            "✅ Готово! Твой трек отправлен диджею.\n"
            "Скоро услышишь его в эфире! 🎶"
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке в канал: {e}")
        await update.message.reply_text(
            "⚠️ Что-то пошло не так. Попробуй ещё раз позже."
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан в переменных окружения!")
    if not CHANNEL_ID:
        raise ValueError("CHANNEL_ID не задан в переменных окружения!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
