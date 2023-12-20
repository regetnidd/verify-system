import traceback

from client import config
import disnake
from disnake.ext import commands
from disnake.ext.commands import InteractionBot


class Events(commands.Cog):
    def __init__(self, client):
        self.client: InteractionBot = client
        self.db = self.client.cluster.moon
        self.collection = self.db.moderator_collection

    @commands.Cog.listener("on_member_join")
    async def unverify(self, member: disnake.Member):
        if member.guild.id == config.BOT_INFO['GUILD_ID'] and config.BOT_INFO['ROLES']['UN_VERIFY_ROLE_ID']:
            role = disnake.utils.get(member.guild.roles, id=int(
                config.BOT_INFO['ROLES']['UN_VERIFY_ROLE_ID']))
            await member.add_roles(role)

    @commands.Cog.listener("on_member_join")
    async def check_punishments(self, member: disnake.Member):
        if member.guild.id == config.BOT_INFO['GUILD_ID']:
            finds = await self.collection.find_one({"_id": member.id})
            if not finds:
                return
            if finds['ban']:
                if finds['ban']['type'] == 'role':
                    ban_role = disnake.utils.get(
                        member.guild.roles, id=int(config.BOT_INFO['BAN_ROLE_ID']))
                    await member.add_roles(ban_role)
            if finds['voice_mute']:
                role = disnake.utils.get(member.guild.roles, id=int(
                    config.BOT_INFO['VOICE_MUTE_ROLE_ID']))
                await member.add_roles(role)
            if finds['text_mute']:
                role = disnake.utils.get(member.guild.roles, id=int(
                    config.BOT_INFO['TEXT_MUTE_ROLE_ID']))
                await member.add_roles(role)
            if finds['dont_allowed']:
                role = disnake.utils.get(member.guild.roles, id=int(
                    config.BOT_INFO['ROLES']['NOT_ALLOWED_ROLE_ID']))
                await member.add_roles(role)


def setup(client: InteractionBot):
    client.add_cog(Events(client))
    print('events подгружены!')
