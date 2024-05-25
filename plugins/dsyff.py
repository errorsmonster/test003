import asyncio 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from info import DATABASE_URI as MONGO_URL
from pymongo import MongoClient
from clone_plugins.users_api import get_settings, save_bot_settings
from database.users_chats_db import db
from .test import CLIENT

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]

CLIENT = CLIENT()


@Client.on_message(filters.command("fsub"))
async def forsyd(bot, message):
    id = bot.me.id
    bot_id = mongo_db.bots.find_one({'bot_id': id})
    try:
        command, forc_id = data.split(" ")
    except:
        return 
        await message.reply_text("<b>ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !\nɢɪᴠᴇ ᴍᴇ ᴄᴏᴍᴍᴀɴᴅ ᴀʟᴏɴɢ ᴡɪᴛʜ ꜱʜᴏʀᴛɴᴇʀ ᴡᴇʙꜱɪᴛᴇ ᴀɴᴅ ᴀᴘɪ.\n\nꜰᴏʀᴍᴀᴛ : <code>/shortlink krishnalink.com c8dacdff6e91a8e4b4f093fdb4d8ae31bc273c1a</code>")
    reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
    await reply.edit_text(f"<b>✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ꜱʜᴏʀᴛʟɪɴᴋ ꜰᴏʀ <code>{title}</code>.\n\nꜱʜᴏʀᴛʟɪɴᴋ ᴡᴇʙꜱɪᴛᴇ : <code>{shortlink_url}</code>\nꜱʜᴏʀᴛʟɪɴᴋ ᴀᴘɪ : <code>{api}</code></b>")


@Client.on_message(filters.command('customize'))
async def settings(client, message):
   await message.reply_text(
     "<b>📝 Eᴅɪᴛ Δɴᴅ ᴄʜᴀɴɢᴇ ꜱΞᴛᴛɪɴɢꜱ ᴀꜱ ʏᴏᴜʀ ᴡɪꜱʜ.......\n<blockquote>ᴩʀᴏ ✨</blockquote></b>",
     reply_markup=main_buttons()
     )

@Client.on_callback_query(filters.regex(r'^customize'))
async def settings_query(bot, query):
  user_id = query.from_user.id
  i, type = query.data.split("#")
  buttons = [[InlineKeyboardButton('«« ʙΔᴄᴋ', callback_data="customize#main")]]
  if type=="main":
     await query.message.edit_text(
       "<b>📝 Eᴅɪᴛ Δɴᴅ ᴄʜᴀɴɢᴇ ꜱΞᴛᴛɪɴɢꜱ ᴀꜱ ʏᴏᴜʀ ᴡɪꜱʜ.......\n<blockquote>ᴩʀᴏ ✨</blockquote></b>",
       reply_markup=main_buttons())
  elif type=="bots":
     buttons = [] 
     _bot = await db.get_bot(user_id)
     if _bot is not None:
        buttons.append([InlineKeyboardButton(_bot['name'],
                         callback_data=f"settings#editbot")])
     else:
        buttons.append([InlineKeyboardButton('✚ Add Bot ✚', 
                         callback_data="settings#addbot")])
        buttons.append([InlineKeyboardButton('✚ Add User Bot ✚', 
                         callback_data="settings#adduserbot")])
     buttons.append([InlineKeyboardButton('🔙 Back', 
                      callback_data="settings#main")])
     await query.message.edit_text(
       "<b><u>My Bots</u></b>\n\nYou Can Manage Your Bots In Here",
       reply_markup=InlineKeyboardMarkup(buttons))
  
  elif type=="addbot":
     await query.message.delete()
     bot = await CLIENT.add_bot(bot, query)
     if bot != True: return
     await query.message.reply_text(
        "<b>Bot Token Successfully Added To Database</b>",
        reply_markup=InlineKeyboardMarkup(buttons))
  elif type=="forc":  
     await query.message.delete()
     try:
         text = await bot.send_message(user_id, "<b><u>Set Target Chat</u></b>\n\nForward A Message From Your Target Chat\n/cancel - To Cancel This Process")
         chat_ids = await bot.listen(chat_id=user_id, timeout=300)
         if chat_ids.text=="/cancel":
            await chat_ids.delete()
            return await text.edit_text(
                  "Process Canceled",
                  reply_markup=InlineKeyboardMarkup(buttons))
         elif not chat_ids.forward_date:
            await chat_ids.delete()
            return await text.edit_text("This Is Not A Forward Message")
         else:
            chat_id = chat_ids.forward_from_chat.id
            title = chat_ids.forward_from_chat.title
            username = chat_ids.forward_from_chat.username
            username = "@" + username if username else "private"
            bot_id = bot.me.id
         forc = await db.add_channel(user_id, chat_id, title, username, bot_id)
         await chat_ids.delete()
         await text.edit_text(
            "Successfully Updated" if forc else "This Channel Already Added",
            reply_markup=InlineKeyboardMarkup(buttons))
     except asyncio.exceptions.TimeoutError:
         await text.edit_text('Process Has Been Automatically Cancelled', reply_markup=InlineKeyboardMarkup(buttons))
  

def main_buttons():
  buttons = [[
       InlineKeyboardButton('🤖 Бᴏᴛꜱ 🤖',
                    callback_data='customize#bots'),
       InlineKeyboardButton('👣 CʜᴀИИᴇʟꜱ 👣',
                    callback_data=f'customize#forc')
       ],[
       InlineKeyboardButton('✎ Cᴀᴘᴛɪᴏɴ ✎',
                    callback_data='forc'),
       InlineKeyboardButton('𠂤 Dᴀᴛᴀ-Бᴀꜱᴇ 𠂤',
                    callback_data='customize')
       ],[
       InlineKeyboardButton('🖤 Fɪʟᴛᴇʀꜱ 🖤',
                    callback_data='customize'),
       InlineKeyboardButton('🖱 ʙꪊᴛᴛᴏɴ 🖱',
                    callback_data='customize')
       ],[
       InlineKeyboardButton('⌂ H0ᴍᴇ ⌂', callback_data='start')
       ]]
  return InlineKeyboardMarkup(buttons)
