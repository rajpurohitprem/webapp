from telegram import (
    KeyboardButton,
    KeyboardButtonRequestChat,
    ReplyKeyboardMarkup,
    Update,
    ChatAdministratorRights,
)
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Replace with your data
BOT_TOKEN = "YOUR_BOT_TOKEN"
ALLOWED = {123456789}
ADMIN_RIGHTS = ChatAdministratorRights(can_manage_chat=True)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED:
        return await update.message.reply_text("🚫 Access denied.")

    # Create a chat-request button
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
                    request_username=True,
                    request_title=True,
                    request_photo=True
                )
            )
        ]
    ]
    markup = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Select a channel you admin:", reply_markup=markup)

async def chat_shared(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_shared = update.effective_message.chat_shared
    if not chat_shared:
        return

    cid = chat_shared.chat_id
    await update.message.reply_text(f"✅ You selected channel ID: `{cid}`", parse_mode="markdown")

    # Save to config.json
    import json
    cfg = {"selected_channel_id": cid}
    with open("config.json", "w") as f:
        json.dump(cfg, f, indent=2)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.Text("/start"), start))
app.add_handler(MessageHandler(filters.StatusUpdate.CHAT_SHARED, chat_shared))
app.run_polling()
