import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("CHANNEL_ID", "").strip()
PAYPAL_LINK = "https://paypal.me/Vadiikkk."

logging.basicConfig(level=logging.INFO)

ALLOWED_DOMAINS = [
    "soundcloud.com",
    "on.soundcloud.com",
    "youtube.com",
    "youtu.be",
    "music.youtube.com",
    "open.spotify.com",
    "spotify.com",
]

def is_valid_music_link(text):
    for domain in ALLOWED_DOMAINS:
        if domain in text:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hey, {user.first_name}! 👋\n"
        f"Привет, {user.first_name}! 👋\n\n"
        "🎵 Order your track / Закажи свой трек\n\n"
        "Send a link from / Отправь ссылку с:\n"
        "• SoundCloud\n"
        "• YouTube / YouTube Music\n"
        "• Spotify\n\n"
        "I'll pass it to the driver! / Передам водителю! 🎧"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""

    if not is_valid_music_link(text):
        await update.message.reply_text(
            "❌ Not a music link / Это не ссылка на музыку\n\n"
            "Send a link from YouTube, SoundCloud or Spotify.\n"
            "Отправь ссылку с YouTube, SoundCloud или Spotify."
        )
        return

    name = f"@{user.username}" if user.username else str(user.first_name)

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"🎵 New request / Новая заявка!\nFrom / От: {name}\nLink / Ссылка: {text}"
        )
        await update.message.reply_text(
            "✅ Done! / Готово!\n"
            "Your track has been sent to the driver.\n"
            "Трек отправлен водителю. 🎶"
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Something went wrong. Try again. / Что-то пошло не так. Попробуй ещё раз.")
        return

    keyboard = [
        [
            InlineKeyboardButton("⭐️ 1", callback_data="rate_1"),
            InlineKeyboardButton("⭐️ 2", callback_data="rate_2"),
            InlineKeyboardButton("⭐️ 3", callback_data="rate_3"),
            InlineKeyboardButton("⭐️ 4", callback_data="rate_4"),
            InlineKeyboardButton("⭐️ 5", callback_data="rate_5"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "How was your ride? / Как вам поездка?\nRate from 1 to 5 / Оцените от 1 до 5:",
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
            text=f"Rating / Оценка!\nFrom / От: {name}\n{stars} ({rating}/5)"
        )
    except Exception as e:
        logging.error(f"Error sending rating: {e}")

    keyboard = [
        [InlineKeyboardButton("💸 Leave a tip / Оставить чаевые", url=PAYPAL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"Thanks for rating! / Спасибо за оценку! {stars}\n\n"
        "Want to tip the driver?\n"
        "Хотите оставить чаевые водителю?",
        reply_markup=reply_markup
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_rating, pattern="^rate_"))
    app.run_polling()

if __name__ == "__main__":
    main()
