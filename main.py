import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Click Counter Bot",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)


@Bot.on_message(filters.command(["start"])
async def start():
    await update.reply_text(
        f"Hello {update.from_user.id}, I am a telegram bot module for how to count total clicks on button.\n\nMade By @FayasNoushad"
    )


Bot.run()
