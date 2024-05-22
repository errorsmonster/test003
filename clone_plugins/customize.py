import asyncio 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from info import DATABASE_URI as MONGO_URL
from pymongo import MongoClient
from database.users_chats_db import db

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]


@Client.on_message(filters.command(["share_text", "share", "sharetext",]))
async def share_text(client, message):
    reply = message.reply_to_message
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"**Notice:**\n\n1. Reply Any Messages.\n2. No Media Support\n\n**Any Question Join Support Chat**",                
            reply_to_message_id=reply_id,               
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support Chat", url=f"https://t.me/MKSSION_GROUP")]])
            )                                                   
        return
    user_id = reply_id
    chat_id = input_text
    await db.add_channel(user_id, chat_id)
    await message.reply_text(
        text=f"**Here is Your Sharing Text 👇**\n\nhttps://t.me/share/url?url="+(input_text),
        reply_to_message_id=reply_id,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("♂️ Share", url=f"https://t.me/share/url?url=(input_text)")]])       
    )
   
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

  elif type=="addchannel":  
     chat_ids = await Client.ask(chat_id=query.message.chat.id, text="<b>❪ SET TARGET CHAT ❫\n\nForward a message from Your target chat\n/cancel - cancel this process</b>")
     if chat_ids.text=="/cancel":
        return await chat_ids.reply_text(
                  "<b>Pʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟᴇᴅ 😮‍💨 !</b>",
                  reply_markup=InlineKeyboardMarkup(buttons))
     elif not chat_ids.forward_date:
        return await chat_ids.reply("**This is not a forward message**")
     else:
        chat_id = chat_ids.forward_from_chat.id
        title = chat_ids.forward_from_chat.title
        username = chat_ids.forward_from_chat.username
        username = "@" + username if username else "private"
     chat = await db.add_channel(user_id, chat_id, title, username)
     await query.message.reply_text(
        "<b>Successfully updated</b>" if chat else "<b>This channel already added</b>",
        reply_markup=InlineKeyboardMarkup(buttons))



def main_buttons():
  buttons = [[
       InlineKeyboardButton('🤖 Бᴏᴛꜱ 🤖',
                    callback_data='customize'),
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
