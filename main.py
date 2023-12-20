import os

import disnake
from disnake.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

from client import config


class Bot(commands.InteractionBot):
    def __init__(self):
        super().__init__(intents=disnake.Intents.all(),
                         application_id=config.BOT_INFO['BOT_ID'],
                         test_guilds=[config.BOT_INFO['GUILD_ID']])
        mongodb_uri = config.BOT_INFO['MONGODB_URI'].replace("<username>", config.BOT_INFO['MONGODB_USER']).replace(
            '<password>', config.BOT_INFO['MONGODB_PASSWORD'])
        self.cluster = AsyncIOMotorClient(mongodb_uri)
        self.db = self.cluster.moderator_db
        self.collection = self.db.moderator_collection

    async def on_ready(self):

        for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/client/events"):
            if filename.endswith(".py"):
                self.load_extension(f"client.events.{filename[:-3]}")
        print(f"{self.user} готов!")

        for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/client/commands/moderation"):
            if filename.endswith(".py"):
                self.load_extension(
                    f"client.commands.moderation.{filename[:-3]}")
        print(f"{self.user} готов!")


bot = Bot()

bot.run(config.BOT_INFO['TOKEN'])
