import os
from typing import Union
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
    api_id=int(os.environ.get("API_ID")),
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
async def count(_, update: Union[Message, CallbackQuery], count=0):
    text = f"Total {str(count)} clicks"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Click Here", callback_data="count=" + str(count))]]
    )
    if isinstance(update, CallbackQuery):
        await update.answer(text="Added your click.\n\n" + text, show_alert=True)
        await update.message.edit_text(text=text, reply_markup=reply_markup)
    else:
        await update.reply_text(text=text, reply_markup=reply_markup)


@Bot.on_message(filters.command("reset"))
async def reset_count(_, update: Message):
    if (reply := update.reply_to_message) and (mkp := reply.reply_markup):
        mkp.inline_keyboard[0][0].callback_data = "count=0"  # modifying the callback data
        try:
            await reply.edit(text="Total 0 clicks", reply_markup=reply.reply_markup)
            await reply.reply_text("Counter has been reset successfully", True)
        except MessageNotModified:
            await reply.reply_text("Counter is already at 0", True)
    else:
        await update.reply_text("Please reply to an active counter message")


@Bot.on_callback_query()
async def callback(_, update: CallbackQuery):
    await count(None, update, count=str(int(update.data.split("=")[1]) + 1))


Bot.run()
