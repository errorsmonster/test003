from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from info import DATABASE_URI as MONGO_URL
from pymongo import MongoClient

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]



@Client.on_message(filters.command("customize") & filters.private)
async def sydoo(bot, message):
    id = bot.me.id
    owner = mongo_db.bots.find_one({'bot_id': id})
    ownerid = int(owner['user_id'])
    if ownerid != message.from_user.id:
        await message.reply_text("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅ❗")
        return
    text = await message.reply_text(text="<code>Gᴇᴛᴛɪɴɢ ɪɴꜰᴏ.....</code>", disable_web_page_preview=True) 
    await asyncio.sleep(0.6)
    await text.edit_text(
        text="<b>Link :-</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("Oᴩᴇɴ Lɪɴᴋ", callback_data="forc"),
            InlineKeyboardButton("βᴏᴛ𝘴 🏞️", callback_data="start"),
            InlineKeyboardButton("Sʜᴀʀᴇ Lɪɴᴋ", callback_data="help")
            ],[
            InlineKeyboardButton("✗ Cꪶꪮ𝘴ꫀ ✗", callback_data="close")
            ]])
    )
    
