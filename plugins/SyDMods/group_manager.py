from pyrogram.types import *
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, enums
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid

from utils import extract_time, extract_user, admin_check, admin_filter                        
from info import ADMINS
from Script import script
from time import time
import asyncio



@Client.on_message(filters.command("ban"))
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin: return 
    user_id, user_first_name = extract_user(message)
    try: await message.chat.ban_member(user_id=user_id)
    except Exception as error: await message.reply_text(str(error))                    
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Sᴏᴍᴇᴏɴᴇ ᴇʟꜱᴇ ɪꜱ ᴅᴜꜱᴛɪɴɢ ᴏꜰꜰ..💤! \n{user_first_name} \nIꜱ Ғᴏʀʙɪᴅᴅᴇɴ.")                              
        else:
            await message.reply_text(f"Sᴏᴍᴇᴏɴᴇ ᴇʟꜱᴇ ɪꜱ ᴅᴜꜱᴛɪɴɢ ᴏꜰꜰ..💤! \n<a href='tg://user?id={user_id}'>{user_first_name}</a> Is Ғoʀʙɪᴅᴅᴇɴ")                      
            

@Client.on_message(filters.command("tban"))
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin: return
    if not len(message.command) > 1: return
    user_id, user_first_name = extract_user(message)
    until_date_val = extract_time(message.command[1])
    if until_date_val is None: return await message.reply_text(text=f"Iɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ꜱᴩᴇᴄɪꜰɪᴇᴅ. ᴄᴏʀʀᴇᴄᴛ ɪᴛ ᴩʟᴇᴀꜱᴇ, \nExᴩᴇᴄᴛᴇᴅ m, h, or d, ɢᴏᴛ ɪᴛ: {message.command[1][-1]}")   
    try: await message.chat.ban_member(user_id=user_id, until_date=until_date_val)            
    except Exception as error: await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Sᴏᴍᴇᴏɴᴇ ᴇʟꜱᴇ ɪꜱ ᴅᴜꜱᴛɪɴɢ ᴏꜰꜰ..💤! \n{user_first_name}\nBᴀɴɴᴇᴅ ꜰᴏʀ {message.command[1]}!")
        else:
            await message.reply_text(f"Sᴏᴍᴇᴏɴᴇ ᴇʟꜱᴇ ɪꜱ ᴅᴜꜱᴛɪɴɢ ᴏꜰꜰ..💤! \n<a href='tg://user?id={user_id}'>ᴜꜱᴇʀ</a>\n  ꜰᴏʀ {message.command[1]}!")
                

@Client.on_message(filters.command(["unban", "unmute"]))
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin: return
    user_id, user_first_name = extract_user(message)
    try: await message.chat.unban_member(user_id=user_id)
    except Exception as error: await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Sᴏᴍᴇᴏɴᴇ ᴇʟꜱᴇ ɪꜱ ᴅᴜꜱᴛɪɴɢ ᴏꜰꜰ..💤!  {user_first_name} To Yᴏᴜ ᴄᴀɴ ᴊᴏɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ 💫!")
        else:
            await message.reply_text(f"Sᴏᴍᴇᴏɴᴇ ᴇʟꜱᴇ ɪꜱ ᴅᴜꜱᴛɪɴɢ ᴏꜰꜰ..💤!  <a href='tg://user?id={user_id}'>{user_first_name}</a> To Yᴏᴜ ᴄᴀɴ ᴊᴏɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ 💫!")           
            

@Client.on_message(filters.command("mute"))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin: return
    user_id, user_first_name = extract_user(message)
    try: await message.chat.restrict_member(user_id=user_id, permissions=ChatPermissions())                         
    except Exception as error: await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"👍🏻 {user_first_name} Mᴜᴛᴇᴅ 🔇🤐🔇")
        else:
            await message.reply_text(f"👍🏻 <a href='tg://user?id={user_id}'>Of lavender</a> The mouth is closed! 🤐")


@Client.on_message(filters.command("tmute"))
async def temp_mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin: return
    if not len(message.command) > 1: return
    user_id, user_first_name = extract_user(message)
    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        return await message.reply_text(f"Invalid time type specified. Expected m, h, or d, Got it: {message.command[1][-1]}")        
    try:
        await message.chat.restrict_member(user_id=user_id, permissions=ChatPermissions(), until_date=until_date_val)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Be quiet for a while! 😠 {user_first_name} muted for {message.command[1]}!")
        else:
            await message.reply_text(f"Be quiet for a while! 😠 <a href='tg://user?id={user_id}'>Of lavender</a>  Mouth  muted for {message.command[1]}!")                


@Client.on_message(filters.command("pin") & filters.create(admin_filter))
async def pin(_, message: Message):
    if not message.reply_to_message: return
    await message.reply_to_message.pin()


@Client.on_message(filters.command("unpin") & filters.create(admin_filter))             
async def unpin(_, message: Message):
    if not message.reply_to_message: return
    await message.reply_to_message.unpin()



@Client.on_message(filters.command("purge") & (filters.group | filters.channel))                   
async def purge(client, message):
    if message.chat.type not in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)): return
    is_admin = await admin_check(message)
    if not is_admin: return
    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0
    if message.reply_to_message:
        for a_s_message_id in range(message.reply_to_message.id, message.id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == "100":
                await client.delete_messages(chat_id=message.chat.id, message_ids=message_ids, revoke=True)              
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(chat_id=message.chat.id, message_ids=message_ids, revoke=True)
            count_del_etion_s += len(message_ids)
    await status_message.edit_text(f"deleted {count_del_etion_s} messages")
    await status_message.delete()
    

@Client.on_message(filters.group & filters.command('inkick'))
async def inkick(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):      
        note = await message.reply_text(script.CREATOR_REQUIRED)
        await asyncio.sleep(3)
        await note.delete()
        return await message.delete()
    if len(message.command) > 1:
        input_str = message.command
        sent_message = await message.reply_text(script.START_KICK)
        await asyncio.sleep(2)
        await message.delete()
        count = 0
        for member in client.get_chat_members(message.chat.id):
            if member.user.status in input_str and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                try:
                    client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
                    count += 1
                except (ChatAdminRequired, UserAdminInvalid):
                    await sent_message.edit(script.ADMIN_REQUIRED)
                    await client.leave_chat(message.chat.id)
                    break
                except FloodWait as e:
                    await asyncio.sleep(e.value)
        try:
            await sent_message.edit(script.KICKED.format(count))
        except ChatWriteForbidden: pass
    else:
        await message.reply_text(script.INPUT_REQUIRED)
  

@Client.on_message(filters.group & filters.command('dkick'))
async def dkick(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):      
        note = await message.reply_text(script.CREATOR_REQUIRED)
        await asyncio.sleep(3)
        await note.delete()
        return await message.delete()
    sent_message = await message.reply_text(script.START_KICK)
    await message.delete()
    count = 0
    for member in client.get_chat_members(message.chat.id):
        if member.user.is_deleted and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            try:
                await client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
                count += 1
            except (ChatAdminRequired, UserAdminInvalid):
                await sent_message.edit(script.ADMIN_REQUIRED)
                await client.leave_chat(message.chat.id)
                break
            except FloodWait as e:
                await asyncio.sleep(e.value)
    try:
        await sent_message.edit(script.DKICK.format(count))
    except ChatWriteForbidden: pass
  
  
@Client.on_message((filters.channel | filters.group) & filters.command('instatus'))
async def instatus(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER, ADMINS):
        note = await message.reply("you are not administrator in this chat")
        await asyncio.sleep(3)
        await message.delete()
        return await note.delete()
    sent_message = await message.reply_text("🔁 Processing.....")
    recently = 0
    within_week = 0
    within_month = 0
    long_time_ago = 0
    deleted_acc = 0
    uncached = 0
    bot = 0
    for member in client.get_chat_members(message.chat.id):
        if member.user.is_deleted: deleted_acc += 1
        elif member.user.is_bot: bot += 1
        elif member.user.status == enums.UserStatus.RECENTLY: recently += 1
        elif member.user.status == enums.UserStatus.LAST_WEEK: within_week += 1
        elif member.user.status == enums.UserStatus.LAST_MONTH: within_month += 1
        elif member.user.status == enums.UserStatus.LONG_AGO: long_time_ago += 1
        else: uncached += 1
    if message.chat.type == enums.ChatType.CHANNEL:
        await sent_message.edit(f"{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}")            
    elif message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await sent_message.edit(f"{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}")
        
            
  


