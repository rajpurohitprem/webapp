from telethon import TelegramClient, events, Button
import json

with open("config.json") as f:
    config = json.load(f)

bot = TelegramClient("bot_session", config["api_id"], config["api_hash"]).start(bot_token=config["bot_token"])

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond(
        "Click below to pick a channel:",
        buttons=[
            [Button.web_app("Pick a Channel", "https://burner-gem-yr-classification.trycloudflare.com/webapp")]
        ]
    )

bot.run_until_disconnected()
