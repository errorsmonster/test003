import re
import logging
import asyncio
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from info import API_ID, API_HASH, ADMINS, DATABASE_NAME
from info import DATABASE_URL as MONGO_URL


CLONE_TXT = """HI"""

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]
mongo_collection = mongo_db[DATABASE_NAME]

@Client.on_message(filters.command("clone") & filters.private)
async def clone(client, message):
    await message.reply_text(CLONE_TXT)

@Client.on_message((filters.regex(r'\d{8,10}:[0-9A-Za-z_-]{35}')) & filters.private)
async def on_clone(client, message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot_token = re.findall(r'\d{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d{8,10}', message.text)
        bots = list(mongo_db.bots.find())
        bot_tokens = [bot['token'] for bot in bots]

        forward_from_id = message.forward_from.id if message.forward_from else None
        if bot_token in bot_tokens and forward_from_id == 93372553:
            await client.send_message(message.chat.id, "**©️ This bot is already cloned.**")
            return

        if not forward_from_id or forward_from_id != 93372553:
            msg = await client.send_message(message.chat.id, "**Please wait while I'm creating your bot.**")
            try:
                ai = Client(
                    f"{bot_token}", API_ID, API_HASH,
                    bot_token=bot_token,
                    plugins={"root": "clone_plugins"},
                )
                await ai.start()
                bot = await ai.get_me()
                details = {
                    'bot_id': bot.id,
                    'is_bot': True,
                    'user_id': user_id,
                    'name': bot.first_name,
                    'token': bot_token,
                    'username': bot.username
                }
                mongo_db.bots.insert_one(details)
                await msg.edit_text(f"<b>Successfully cloned your bot: @{bot.username}.</b>")
            except Exception as e:
                logging.exception("Error while cloning bot.")
                await msg.edit_text(f"⚠️ <b>Bot Error:</b>\n\n<code>{e}</code>\n\n**Kindly forward this message to @KingVJ01 to get assistance.**")
    except Exception as e:
        logging.exception("Error while handling message.")

@Client.on_message(filters.command("deletecloned") & filters.private)
async def delete_cloned_bot(client, message):
    try:
        bot_token = re.findall(r'\d{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d{8,10}', message.text)

        mongo_collection = mongo_db.bots
        cloned_bot = mongo_collection.find_one({"token": bot_token})
        if cloned_bot:
            mongo_collection.delete_one({"token": bot_token})
            await client.send_message(message.chat.id, "**The cloned bot has been removed from the list and its details have been removed from the database.**")
        else:
            await client.send_message(message.chat.id, "**The bot token provided is not in the cloned list.**")
    except Exception as e:
        logging.exception("Error while deleting cloned bot.")
        await client.send_message(message.chat.id, "An error occurred while deleting the cloned bot.")

async def restart_bots():
    logging.info("Restarting all bots........")
    bots = list(mongo_db.bots.find())
    for bot in bots:
        bot_token = bot['token']
        try:
            ai = Client(
                f"{bot_token}", API_ID, API_HASH,
                bot_token=bot_token,
                plugins={"root": "clone_plugins"},
            )
            await ai.start()
        except Exception as e:
            logging.exception(f"Error while restarting bot with token {bot_token}: {e}")

# Call the restart function
asyncio.ensure_future(restart_bots())
