from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButtonRequestChat,
)
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton(
        text="Share a group",
        request_chat=KeyboardButtonRequestChat(
            request_id=1,
            chat_is_channel=False  # Set to True if you want to request a channel instead
        )
    )

    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text("Please share a group with me:", reply_markup=reply_markup)

app = Application.builder().token('7857315431:AAEDMVPL8cCWM1wPBt0Oj3yTT3AqHlKN7sQ').build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
