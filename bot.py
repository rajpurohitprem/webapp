import json
from flask import Flask, send_from_directory, jsonify, request
from telethon.sync import TelegramClient
from telethon import events, Button
import threading
import os

# Load config
CONFIG_FILE = "config.json"
config = json.load(open(CONFIG_FILE))

api_id = config["api_id"]
api_hash = config["api_hash"]
bot_token = config["bot_token"]
allowed_users = config["allowed_users"]

# Clients
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
anon = TelegramClient("anon", api_id, api_hash)

# Flask app
app = Flask(__name__, static_folder="webapp")

@app.route("/")
def index():
    return send_from_directory("webapp", "index.html")

@app.route("/script.js")
def js():
    return send_from_directory("webapp", "script.js")

@app.route("/channels")
def get_channels():
    print("✅ /channels called")
    channels = []
    with anon:
        dialogs = anon.get_dialogs()
        for dialog in dialogs:
            entity = dialog.entity
            if getattr(entity, "megagroup", False) or getattr(entity, "broadcast", False):
                if getattr(entity, "creator", False):  # Admin check
                    channels.append({
                        "id": str(entity.id).replace("-100", ""),
                        "title": entity.title
                    })
    print("📡 Channels:", channels)
    return jsonify(channels)

@app.route("/save", methods=["POST"])
def save_channel():
    data = request.get_json()
    channel_id = data.get("channel_id")
    print("💾 Saving Channel ID:", channel_id)
    config["selected_channel_id"] = channel_id
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    return jsonify({"success": True})


# Telegram Bot: /start
@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    if event.sender_id not in allowed_users:
        await event.respond("❌ You are not authorized to use this bot.")
        return

    await event.respond(
        "Click the button below to pick a channel 👇",
        buttons=[
            [Button.url("📡 Pick a Channel", "https://burner-gem-yr-classification.trycloudflare.com")]
        ]
    )


# Run Flask in background
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Main
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("✅ Flask server started on http://localhost:8080")
    print("🤖 Bot is running. Press Ctrl+C to stop.")
    bot.run_until_disconnected()
