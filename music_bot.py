import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("CHANNEL_ID", "").strip()

logging.basicConfig(level=logging.INFO)

ALLOWED_DOMAINS = [
    "soundcloud.com",
    "on.soundcloud.com",
    "youtube.com",
    "youtu.be",
    "music.youtube.com",
    "open.spotify.com",
    "spotify.com",
    "music.yandex.ru",
]

def is_valid_music_link(text):
    for domain in ALLOWED_DOMAINS:
        if domain in text:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n\n"
        "Отправь ссылку на трек с:\n"
        "SoundCloud, YouTube, Spotify\n\n"
        "И я передам её водителю!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""

    if not is_valid_music_link(text):
        await update.message.reply_text(
            "Это не ссылка на музыку.\n"
            "Отправь ссылку с YouTube, SoundCloud или Spotify."
        )
        return

    name = f"@{user.username}" if user.username else str(user.first_name)

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"Новая заявка!\nОт: {name}\nСсылка: {text}"
        )
        await update.message.reply_text("Готово! Трек отправлен водителю.")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Что-то пошло не так. Попробуй ещё раз.")
        return

    keyboard = [
        [
            InlineKeyboardButton("⭐️1", callback_data="rate_1"),
            InlineKeyboardButton("⭐️2", callback_data="rate_2"),
            InlineKeyboardButton("⭐️3", callback_data="rate_3"),
            InlineKeyboardButton("⭐️4", callback_data="rate_4"),
            InlineKeyboardButton("⭐️5", callback_data="rate_5"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Как вам поездка? Оцените от 1 до 5:",
        reply_markup=reply_markup
    )

async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    rating = query.data.split("_")[1]
    name = f"@{user.username}" if user.username else str(user.first_name)

    stars = "⭐️" * int(rating)

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"Оценка поездки!\nОт: {name}\n{stars} ({rating}/5)"
        )
        await query.edit_message_text(f"Спасибо за оценку {stars}\nХорошего дня!")
    except Exception as e:
        logging.error(f"Ошибка при отправке оценки: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_rating, pattern="^rate_"))
    app.run_polling()

if __name__ == "__main__":
    main()
