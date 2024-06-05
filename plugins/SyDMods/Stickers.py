from pyrogram import Client, filters

@Client.on_message(filters.command("stickerid") & filters.private)
async def stickerid(bot, message):
    s_msg = await bot.ask(chat_id = message.from_user.id, text = "Oᴋᴋ...! Noᴡ Sᴇɴᴅ Mᴇ Yᴏᴜʀ Sᴛɪᴄᴋᴇʀ..")
    if s_msg.sticker:
        await s_msg.reply_text(f"**Sᴛɪᴄᴋᴇʀ <b>ɪᴅ</b> ɪꜱ**  \n `{s_msg.sticker.file_id}` \n \n ** UɴɪQᴜᴇ <b>ɪᴅ</b> ɪꜱ ** \n\n`{s_msg.sticker.file_unique_id}`")
    else: 
        await s_msg.reply_text("Oᴏᴩꜱ !! Nᴏᴛ Δ ꜱᴛɪᴄᴋᴇʀ ꜰɪʟᴇ")
