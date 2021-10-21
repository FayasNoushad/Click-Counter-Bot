import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Click Counter Bot",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    parse_mode="html",
    sleep_threshold=3600
)


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        f"Hello {update.from_user.id}, I am a telegram bot module for how to count total clicks on button.\n\nMade By @FayasNoushad"
    )


@Bot.on_message(filters.command(["count"]))
async def count(bot, update, count=0, cb=False):
    text = f"Total {str(count)} clicks"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Click Here", callback_data="count="+str(count))]]
    )
    if cb:
        await update.answer(text="Added your click.\n\n"+text, show_alert=True)
        await update.message.edit_text(text=text, reply_markup=reply_markup)
    else:
        await update.reply_text(text=text, reply_markup=reply_markup)


@Bot.on_callback_query()
async def callback(bot, update):
    await count(bot, update, count=str(int(update.data.split("=")[1])+1), cb=True)


Bot.run()
