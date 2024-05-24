from info import DATABASE_URI as MONGO_URL
from pymongo import MongoClient
import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URL, AUTH_CHANNEL, IS_SHORTLINK


class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        mongo_client = MongoClient(MONGO_URL)
        self.bd = mongo_client["cloned_vjbotz"]
        self.col = self.db.users
        self.grp = self.db.groups
        self.bot = self.bd.bots

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )

    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)


    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    
    async def get_all_users(self):
        return self.col.find({})



    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def get_settings(self, id):
        default = {
            'forc_id': AUTH_CHANNEL,
            'is_forc': IS_SHORTLINK,
        }
        bot = await self.bot.find_one({'id':int(id)})
        if bot:
            return bot.get('settings', default)
        return default
        
    async def update_settings(self, id, settings):
        await self.bot.update_one({'id': int(id)}, {'$set': {'settings': settings}})

    async def update_one(self, filter_query, update_data):
        try:
            # Assuming self.client and self.users are set up properly
            result = await self.users.update_one(filter_query, update_data)
            return result.matched_count == 1
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

    async def in_channel(self, user_id: int, bot_id: int) -> bool:
       channel = await self.chl.find_one({"user_id": int(user_id), "bot_id": int(bot_id)})
       return bool(channel)
    
    async def add_channel(self, user_id: int, bot_id: int, chat_id: int, title, username):
       channel = await self.in_channel(user_id, bot_id)
       if channel:
         return False
       return await self.chl.insert_one({"user_id": user_id, "bot_id": bot_id, "chat_id": chat_id, "title": title, "username": username})
    
    async def remove_channel(self, user_id: int, bot_id: int, chat_id: int):
       channel = await self.in_channel(user_id, bot_id )
       if not channel:
         return False
       return await self.chl.delete_many({"user_id": int(user_id), "bot_id": int(bot_id)})
    
    async def get_channel_details(self, user_id: int, chat_id: int):
       return await self.chl.find_one({"user_id": int(user_id), "chat_id": int(chat_id)})
       
    async def get_user_channels(self, user_id: int):
       channels = self.chl.find({"user_id": int(user_id)})
       return [channel async for channel in channels]

db = Database(DATABASE_URL, DATABASE_NAME)
