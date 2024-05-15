import asyncio 
from database import Database, db
from script import Script
from info import SYD_CHANNEL
from MrSyD import is_reqa_subscribed
from pyrogram import Client, filters, enums
from .test import get_configs, update_configs, CLIENT, parse_buttons, start_clone_bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired

CLIENT = CLIENT()

@Client.on_message(filters.command('settings'))
async def settings(client, message):
   await message.reply_text(
     "<b>📝 Eᴅɪᴛ Δɴᴅ ᴄʜᴀɴɢᴇ ꜱΞᴛᴛɪɴɢꜱ ᴀꜱ ʏᴏᴜʀ ᴡɪꜱʜ.......\n<blockquote>ᴩʀᴏ ✨</blockquote></b>",
     reply_markup=main_buttons()
     )

@Client.on_callback_query(filters.regex(r'^settings'))
async def settings_query(bot, query):
  user_id = query.from_user.id
  i, type = query.data.split("#")
  buttons = [[InlineKeyboardButton('«« ʙΔᴄᴋ', callback_data="settings#main")]]
  if type=="main":
     await query.message.edit_text(
       "<b>📝 Eᴅɪᴛ Δɴᴅ ᴄʜᴀɴɢᴇ ꜱΞᴛᴛɪɴɢꜱ ᴀꜱ ʏᴏᴜʀ ᴡɪꜱʜ.......\n<blockquote>ᴩʀᴏ ✨</blockquote></b>",
       reply_markup=main_buttons())

  elif type=="bots":
     buttons = [] 
     _bot = await db.get_bot(user_id)
     if _bot is not None:
        buttons.append([InlineKeyboardButton(_bot['name'],
                         callback_data=f"settings")])
     else:
        buttons.append([InlineKeyboardButton('✚ Aᴅᴅ ʙᴏᴛ ✚', 
                         callback_data="settings#addbot")])
        buttons.append([InlineKeyboardButton('✚ Aᴅᴅ Uꜱᴇʀ ʙᴏᴛ ✚', 
                         callback_data="settings#adduserbot")])
     buttons.append([InlineKeyboardButton('«« ʙΔᴄᴋ', 
                      callback_data="settingsn")])
     await query.message.edit_text(
       "<b><u>Mʏ 8ᴏᴛꜱ</b></u>\n\n<b>Yoᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ʙᴏᴛ'ꜱ ʜᴇʀᴇ😜</b>",
       reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="addbot":
     await query.message.delete()
     bot = await CLIENT.add_bot(bot, query)
     if bot != True: return
     await query.message.reply_text(
        "<b>Bᴏᴛ ꜱUᴄᴄᴇꜱꜱ ꜰUʟʟʏ Δᴅᴅᴇᴅ ᴛᴏ Sʏᴅ-ʙᴀꜱᴇ</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="editbot": 
     bot = await db.get_bot(user_id)
     TEXT = Script.BOT_DETAILS if bot['is_bot'] else Script.USER_DETAILS
     buttons = [[InlineKeyboardButton('❌ Remove ❌', callback_data=f"settings#removebot")
               ],
               [InlineKeyboardButton('«« ʙΔᴄᴋ', callback_data="settings#bots")]]
     await query.message.edit_text(
        TEXT.format(bot['name'], bot['id'], bot['username']),
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="removebot":
     await db.remove_bot(user_id)
     await query.message.edit_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup(buttons))
def main_buttons():
  buttons = [[
       InlineKeyboardButton('🤖 Бᴏᴛꜱ 🤖',
                    callback_data=f'settings#bots'),
       InlineKeyboardButton('👣 CʜᴀИИᴇʟꜱ 👣',
                    callback_data=f'settings#channels')
  ]
  return InlineKeyboardMarkup(buttons)
