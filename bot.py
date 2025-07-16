import json
from flask import Flask, request, send_from_directory
from telethon import TelegramClient, events, Button
import threading

# Load config
with open("config.json") as f:
    config = json.load(f)

app = Flask(__name__)

# Start bot and user sessions
bot = TelegramClient("bot", config["api_id"], config["api_hash"]).start(bot_token=config["bot_token"])
anon = TelegramClient("anon", config["api_id"], config["api_hash"])

# Start Flask + WebApp
@app.route("/")
def index():
    return send_from_directory("webapp", "index.html")

@app.route("/script.js")
def script():
    return send_from_directory("webapp", "script.js")

@app.route("/channels", methods=["GET"])
async def get_channels():
    await anon.connect()
    dialogs = await anon.get_dialogs()
    admin_channels = [
        {"title": d.name, "id": str(d.entity.id)}
        for d in dialogs if d.is_channel and d.entity.admin_rights
    ]
    return admin_channels

@app.route("/save", methods=["POST"])
def save_channel():
    data = request.json
    channel_id = str(data.get("channel_id")).replace("-100", "")
    config["selected_channel_id"] = channel_id
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    return {"status": "saved", "channel_id": channel_id}

# Telegram bot: Send web app button
@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    if event.sender_id not in config["allowed_users"]:
        await event.respond("❌ You are not authorized to use this bot.")
        return

    await event.respond(
        "Click below to pick a channel 👇",
        buttons=[
            [Button.web_app("📡 Pick a Channel", "https://burner-gem-yr-classification.trycloudflare.com")]
        ]
    )

# Run Flask server in a thread
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Main
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("✅ Flask server started on http://localhost:8080")
    print("🤖 Bot is running. Press Ctrl+C to stop.")
    bot.run_until_disconnected()
