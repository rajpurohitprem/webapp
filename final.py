from telegram import (
    KeyboardButton,
    KeyboardButtonRequestChat,
    ReplyKeyboardMarkup,
    Update,
    ChatAdministratorRights,
)
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import json

# Replace with your actual token and user ID
BOT_TOKEN = "YOUR_BOT_TOKEN"
ALLOWED = {123456789}  # Replace with your allowed user IDs
CONFIG_FILE = "config.json"

# Administrator rights required by the user and bot
ADMIN_RIGHTS = ChatAdministratorRights(can_manage_chat=True)

# /start handler
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED:
        return await update.message.reply_text("🚫 Access denied.")

    # Chat picker button
    kb = [
        [
            KeyboardButton(
                text="📢 Pick a Channel",
                request_chat=KeyboardButtonRequestChat(
                    request_id=1,
                    chat_is_channel=True,
                    user_administrator_rights=ADMIN_RIGHTS,
                    bot_administrator_rights=ADMIN_RIGHTS,
                    bot_is_member=True,
                )
            )
        ]
    ]
    markup = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Select a channel you admin:", reply_markup=markup)

# Handle shared chat from keyboard button
async def chat_shared(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_shared = update.effective_message.chat_shared
    if not chat_shared:
        return

    cid = str(chat_shared.chat_id).replace("-100", "")
    await update.message.reply_text(f"✅ You selected channel ID: `{cid}`", parse_mode="markdown")

    # Save to config.json
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    config["selected_channel_id"] = cid
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

# Setup app
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.CHAT_SHARED, chat_shared))

# Run the bot
if __name__ == "__main__":
    print("✅ Bot is running...")
    app.run_polling()
