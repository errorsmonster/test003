import os
import re 
import sys
import asyncio 
import logging 
from database.users_chats_db import Database, db
from info import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from pyrogram.errors import FloodWait
from Script import script
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)]\[buttonurl:/{0,2}(.+?)(:same)?])")
BOT_TOKEN_TEXT = "<b>1) create a bot using @BotFather\n2) Then you will get a message with bot token\n3) Forward that message to me</b>"
SESSION_STRING_SIZE = 351

class CLIENT: 
  def __init__(self):
     self.api_id = Config.API_ID
     self.api_hash = Config.API_HASH

  def client(self, data, user=None):
     if user == None and data.get('is_bot') == False:
        return Client("USERBOT", self.api_id, self.api_hash, session_string=data.get('session'))
     elif user == True:
        return Client("USERBOT", self.api_id, self.api_hash, session_string=data)
     elif user != False:
        data = data.get('token')
     return Client("BOT", self.api_id, self.api_hash, bot_token=data, in_memory=True)

  async def add_bot(self, bot, message):
     try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)
        bots = list(mongo_db.bots.find())
        bot_tokens = None # Initialize bot_tokens variable

        for bot in bots:
            bot_tokens = bot['token']

        forward_from_id = message.forward_from.id if message.forward_from else None
        if bot_tokens == bot_token and forward_from_id == 93372553:
            await message.reply_text("**©️ ᴛʜɪs ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ʙᴀʙʏ 🐥**")
            return

        if not forward_from_id != 93372553:
            msg = await message.reply_text("**👨‍💻 ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ ɪ ᴀᴍ ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʙᴏᴛ ❣️**")
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
                await msg.edit_text(f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ʏᴏᴜʀ ʙᴏᴛ: @{bot.username}.\n\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ sᴇᴛ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ɪɴ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ sᴛᴀʀᴛ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ</b>")
            except BaseException as e:
                logging.exception("Error while cloning bot.")
                await msg.edit_text(f"⚠️ <b>Bot Error:</b>\n\n<code>{e}</code>\n\n**Kindly forward this message to @KingVJ01 to get assistance.**")
     except Exception as e:
         logging.exception("Error while handling message.")

  async def add_session(self, bot, message):
     user_id = int(message.from_user.id)
     text = "<b>⚠️ DISCLAIMER ⚠️</b>\n\n<code>you can use your session for forward message from private chat to another chat.\nPlease add your pyrogram session with your own risk. Their is a chance to ban your account. My developer is not responsible if your account may get banned.</code>"
     await bot.send_message(user_id, text=text)
     msg = await bot.ask(chat_id=user_id, text="<b>send your pyrogram session.\nget it from @mdsessiongenbot\n\n/cancel - cancel the process</b>")
     if msg.text=='/cancel':
        return await msg.reply('<b>process cancelled !</b>')
     elif len(msg.text) < SESSION_STRING_SIZE:
        return await msg.reply('<b>invalid session sring</b>')
     try:
       client = await bot.start_clone_bot(self.client(msg.text, True), True)
     except Exception as e:
       await msg.reply_text(f"<b>USER BOT ERROR:</b> `{e}`")
     user = client.me
     details = {
       'id': user.id,
       'is_bot': False,
       'user_id': user_id,
       'name': user.first_name,
       'session': msg.text,
       'username': user.username
     }
     await db.add_bot(details)
     return True

@Client.on_message(filters.private & filters.command('reset'))
async def forward_tag(bot, m):
   default = await db.get_configs("01")
   temp.CONFIGS[m.from_user.id] = default
   await db.update_configs(m.from_user.id, default)
   await m.reply("successfully settings reseted ✔️")

@Client.on_message(filters.command('resetall') & filters.user(Config.BOT_OWNER_ID))
async def resetall(bot, message):
  users = await db.get_all_users()
  sts = await message.reply("**processing**")
  TEXT = "total: {}\nsuccess: {}\nfailed: {}\nexcept: {}"
  total = success = failed = already = 0
  ERRORS = []
  async for user in users:
      user_id = user['id']
      default = await get_configs(user_id)
      default['db_uri'] = None
      total += 1
      if total %10 == 0:
         await sts.edit(TEXT.format(total, success, failed, already))
      try: 
         await db.update_configs(user_id, default)
         success += 1
      except Exception as e:
         ERRORS.append(e)
         failed += 1
  if ERRORS:
     await message.reply(ERRORS[:100])
  await sts.edit("completed\n" + TEXT.format(total, success, failed, already))

async def get_configs(user_id):
  #configs = temp.CONFIGS.get(user_id)
  #if not configs:
  configs = await db.get_configs(user_id)
  #temp.CONFIGS[user_id] = configs 
  return configs

async def update_configs(user_id, key, value):
  current = await db.get_configs(user_id)
  if key in ['caption', 'duplicate', 'db_uri', 'forward_tag', 'protect', 'file_size', 'size_limit', 'extension', 'keywords', 'button']:
     current[key] = value
  else: 
     current['filters'][key] = value
 # temp.CONFIGS[user_id] = value
  await db.update_configs(user_id, current)

def parse_buttons(text, markup=True):
    buttons = []
    for match in BTN_URL_REGEX.finditer(text):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        if n_escapes % 2 == 0:
            if bool(match.group(4)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", "")))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", ""))])
    if markup and buttons:
       buttons = InlineKeyboardMarkup(buttons)
    return buttons if buttons else None
