import re
from typing import Union
from client import config
import disnake
from motor.motor_asyncio import AsyncIOMotorClient

mongodb_uri = config.BOT_INFO['MONGODB_URI'].replace("<username>", config.BOT_INFO['MONGODB_USER']).replace(
    '<password>', config.BOT_INFO['MONGODB_PASSWORD'])
cluster = AsyncIOMotorClient(mongodb_uri)
collection = cluster.moon.moderator_collection
staff_collection = cluster.moon.staff_collection


def convert_str(seconds: int) -> str:
    if seconds < 60:
        return "%sсек." % seconds
    minutes, _ = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours >= 24:
        days, hours = divmod(hours, 24)
        if days >= 7:
            weeks, days = divmod(days, 7)
            return "%sнед. %sд." % (weeks, days)
        return "%sд. %sч." % (days, hours)
    return "%sч. %sмин." % (hours, minutes)


def convert_time(time: str):
    time_list = re.split('(\d+)', time)
    time_in_s = None
    if time_list[2] == "s":
        time_in_s = int(time_list[1])
    if time_list[2] == "m":
        time_in_s = int(time_list[1]) * 60
    if time_list[2] == "h":
        time_in_s = int(time_list[1]) * 60 * 60
    if time_list[2] == "d":
        time_in_s = int(time_list[1]) * 60 * 60 * 24
    if time_in_s is None:
        raise ValueError("Неизвестная величина!")
    return time_in_s


async def check_collection(user: Union[disnake.User, disnake.Member], staff_command: bool = True
                           ):
    if await collection.find_one({"_id": user.id}) is None:
        await collection.insert_one({
            "_id": user.id,
            'ban': None,
            'warns': [],
            'dont_allowed': False,
            'event_ban': None,
            'voice_mute': None,
            'text_mute': None,
            'punishments': []
        })
        print(f'{user} | Added to collection!')
    if staff_command:
        if await staff_collection.find_one({"_id": user.id}) is None:
            await staff_collection.insert_one({
                "_id": user.id,
                "voice_mutes": 0,
                "voice_unmutes": 0,
                "text_mutes": 0,
                "text_unmutes": 0,
                "bans": 0,
                "unbans": 0,
                "warns": 0,
                "unwarns": 0,
                "reports": 0,
                "rate": 0,
                "verifies": []
            })
            print(f'{user} | Added to staff collection!')
