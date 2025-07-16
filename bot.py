from flask import Flask, render_template, request, jsonify
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os, json

# Load bot token and user restrictions
config = json.load(open("bot_config.json"))
BOT_TOKEN = config["bot_token"]
ALLOWED_USERS = config["allowed_users"]

api_id = 123456  # your api_id
api_hash = "your_api_hash"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_channels', methods=["POST"])
def get_channels():
    user_id = int(request.form.get("user_id"))
    session_str = request.form.get("session")

    if user_id not in ALLOWED_USERS:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        client = TelegramClient(StringSession(session_str), api_id, api_hash)
        client.connect()
        dialogs = client.get_dialogs()
        channels = [{"id": d.entity.id, "title": d.name} for d in dialogs if d.is_channel and not d.is_user]
        client.disconnect()
        return jsonify({"channels": channels})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=7860)
