import os, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegraph import upload_file
from utils import get_file_id


@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    replied = update.reply_to_message
    if not replied:
        return await update.reply_text("Rᴇᴘʟʏ Tᴏ A Pʜᴏᴛᴏ Oʀ Vɪᴅᴇᴏ Uɴᴅᴇʀ 5ᴍʙ")
    file_info = get_file_id(replied)
    if not file_info:
        return await update.reply_text("Nᴏᴛ Sᴜᴩᴩᴏʀᴛᴇᴅ!")
    text = await update.reply_text(text="<code>Dᴏᴡɴʟᴏᴀᴅɪɴɢ To Mʏ Sᴇʀᴠᴇʀ ...</code>", disable_web_page_preview=True)   
    media = await update.reply_to_message.download()   
    await text.edit_text(text="<code>Dᴏᴡᴏᴀᴅɪɴɢ Cᴏᴍᴩʟᴇᴛᴇᴅ. Now I ᴀᴍ Uᴩʟᴏᴀᴅɪɴɢ ᴛᴏ telegra.ph Lɪɴᴋ ...</code> \nᴅᴏɴ'ᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ꜱᴜᴩᴩᴏʀᴛ ᴜꜱ @Bot_Cracker", disable_web_page_preview=True)                                            
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"Eʀʀᴏʀ :- {error}", disable_web_page_preview=True)       
        return    
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return    
    await text.edit_text(
        text=f"<b>Lɪɴᴋ :-</b>\n\n<code>https://graph.org{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Oᴩᴇɴ Lɪɴᴋ", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="βᴏᴛ𝘴 🏞️", url="https://t.me/Bot_Cracker/17"),
            InlineKeyboardButton(text="Sʜᴀʀᴇ Lɪɴᴋ", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
            ],[
            InlineKeyboardButton(text="✗ Cꪶꪮ𝘴ꫀ ✗", callback_data="close")
            ]])
        )
    
