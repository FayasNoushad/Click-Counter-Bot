import os
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified
from dotenv import load_dotenv

load_dotenv()


Bot = Client(
    "Click Counter Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),  # type: ignore
    api_hash=os.environ.get("API_HASH"),
    parse_mode="html",
    sleep_threshold=3600,
)


@Bot.on_message(filters.command(["start"]))
async def start(_, update: Message):
    await update.reply_text(
        f"Hello {update.from_user.mention}, I am a telegram bot module for counting total number of clicks on a button.\n\nMade By @FayasNoushad"
    )


@Bot.on_message(filters.command(["count"]))
async def count(_, update: Message):
    await update.reply_text(
        text="Total 0 clicks",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click Here", callback_data="count")]]
        ),
    )


@Bot.on_message(filters.command("reset"))
async def reset_count(_, update: Message):
    if (reply := update.reply_to_message) and (reply.reply_markup):
        try:
            await reply.edit(text="Total 0 clicks", reply_markup=reply.reply_markup)
            await reply.reply_text("Counter has been reset successfully", True)
        except MessageNotModified:
            await reply.reply_text("Counter is already at 0", True)
    else:
        await update.reply_text("Please reply to an active counter message")


@Bot.on_callback_query(filters.regex(r"^count$"))
async def callback(_, update: CallbackQuery):
    count = int(update.message.text.split(" ")[1]) + 1
    text = f"Total {count} clicks"
    await update.message.edit_text(text=text, reply_markup=update.message.reply_markup)
    await update.answer(text=f"Added your click,\n\n{text}", show_alert=True)


Bot.run()
