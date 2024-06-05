# Don't Remove Credit @SyD_Xyz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


import traceback
from asyncio import get_running_loop
from io import BytesIO
from googletrans import Translator
from gtts import gTTS
from pyrogram import Client, filters
from pyrogram.types import Message


def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = lang + ".mp3"
    tts.write_to_fp(audio)
    return audio


@Client.on_message(filters.command("tts"))
async def text_to_speech(bot, message: Message):
    vj = await bot.ask(chat_id = message.from_user.id, text = "Nᴏᴡ Sᴇɴᴅ Mᴇ Yᴏᴜʀ Tᴇxᴛ....")
    if vj.text:
        m = await vj.reply_text("Pʀᴏᴄᴇꜱꜱɪɴɢ...!")
        text = vj.text
        try:
            loop = get_running_loop()
            audio = await loop.run_in_executor(None, convert, text)
            await vj.reply_audio(audio)
            await m.delete()
            audio.close()
        except Exception as e:
            await m.edit(e)
            e = traceback.format_exc()
            print(e)
    else:
        await vj.reply_text("Sᴇɴᴅ ᴍᴇ ᴏɴʟʏ ᴛᴇxᴛ Bᴜᴅᴅʏ....")


