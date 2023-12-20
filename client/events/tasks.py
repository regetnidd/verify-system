import datetime
import traceback

import disnake
from disnake.ext import tasks, commands
from disnake.ext.commands import InteractionBot

from client import config


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client: InteractionBot = client
        self.db = self.client.cluster.moon
        self.collection = self.db.moderator_collection
        self.verify_online = self.db.verify_online
        self.verify_onlineDD.start()

    @tasks.loop(seconds=10)
    async def verify_onlineDD(self):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(config.BOT_INFO['GUILD_ID'])
        for channel_id in config.BOT_INFO['VERIFY_CHANNELS_IDS']:
            channel: disnake.TextChannel = await guild.fetch_channel(int(channel_id))
            if not channel:
                print(f"Not found verify channel with id: {channel_id}")
                continue
            for u in channel.members:
                if not u.bot:
                    if u.voice:
                        staff_role = disnake.utils.get(
                            guild.roles, id=int(config.BOT_INFO['STAFF_ROLE_ID']))
                        if staff_role in u.roles:
                            if not u.voice.deaf or not u.voice.self_deaf:
                                if await self.verify_online.find_one({"_id": u.id}) is None:
                                    await self.verify_online.insert_one({"_id": u.id, "online": 0})
                                else:
                                    await self.verify_online.update_one({"_id": u.id}, {"$inc": {"online": 1}})


def setup(client: InteractionBot):
    client.add_cog(Tasks(client))
    print('Tasks подгружены!')
