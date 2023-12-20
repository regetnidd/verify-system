import datetime

from client import config
import disnake
from disnake.ext import commands
from disnake.ext.commands import InteractionBot, BucketType
from client.ui.verify_ui import Verify

from client.tools.tools import convert_str, convert_time, check_collection


class Commands(commands.Cog):
    def __init__(self, client):
        self.client: InteractionBot = client
        self.db = self.client.cluster.moon
        self.verify_online = self.db.verify_online
        self.collection = self.db.moderator_collection
        self.staff_collection = self.db.staff_collection

    @staticmethod
    def convert_time(seconds: int) -> str:
        minutes, _ = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours >= 24:
            days, hours = divmod(hours, 24)
            if days >= 7:
                weeks, days = divmod(days, 7)
                return "%sнед. %sд." % (weeks, days)
            return "%sд. %sч." % (days, hours)
        return "%sч. %sмин." % (hours, minutes)

    @commands.guild_only()
    @commands.has_any_role(*(config.BOT_INFO['VERIFY_ACCESS_ROLES_IDS']))
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    @commands.slash_command(name="verify", description="Верифицировать пользователя.")
    async def verify(self, interaction: disnake.ApplicationCommandInteraction,
                     member: disnake.Member = commands.Param(name='пользователь', description="Укажите пользователя.")):
        await check_collection(interaction.author)
        await check_collection(member)
        emb = disnake.Embed(color=0x2f3136)
        emb.title = "Верификация"
        emb.description = f"{interaction.user.mention}, Выберите **взаимодействие** для {member.mention}!"
        emb.add_field(name="> Аккаунт создан:",
                      value=f"```{member.created_at.strftime('%d.%m.%Y')}```")
        emb.add_field(name="> Зашел на сервер:",
                      value=f"```{member.joined_at.strftime('%d.%m.%Y')}```")
        emb.set_thumbnail(url=member.display_avatar.url)
        emb.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=emb,
                                                view=Verify(interaction, member, interaction.user,
                                                            config.BOT_INFO['ROLES'].items(
                                                            ), self.collection,
                                                            self.staff_collection, interaction.author, interaction.guild, self.client))

    @commands.guild_only()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.slash_command(name='staff-profile', description='Статистика Стаффа.')
    async def stats(self, interaction: disnake.ApplicationCommandInteraction,
                    member: disnake.Member = commands.Param(None, name='стафф', description='Укажите стафф.')):
        user = member
        if member is None:
            user = interaction.user
        await check_collection(interaction.author)

        stats = await self.staff_collection.find_one({"_id": user.id})
        if stats is None:
            await interaction.send("**К сожалению статистика стаффа у данного пользователя не была обнаружена!**",
                                   ephemeral=True)
            return

        value1 = stats["rate"]
        value2 = len(stats["verifies"])

        rate = value1 / value2

        voice = await self.verify_online.find_one({"_id": user.id})
        if voice is not None:
            emb = disnake.Embed(
                description=f'                  \n'
                            f'> **Верифицировал:**  — `{len(stats["verifies"])}`\n'
                            f'> **Рейтинг:**  — `{rate:.1f}`\n',
                            title=f'Статистика {user}',
                color=0x2f3136)
        else:
            emb = disnake.Embed(
                description=f'                  \n'
                            f'> **Верифицировал:**  — `{len(stats["verifies"])}`\n'
                            f'> **Рейтинг:**  — `{rate:.1f}`\n',

                            title=f'Статистика {user}',
                color=0x2f3136)
        emb.set_thumbnail(url=user.display_avatar.url)
        emb.set_footer(text=f"ID: {user.id}")
        await interaction.send(embed=emb)



def setup(client: InteractionBot):
    client.add_cog(Commands(client))
    print("\"Other commands\" louad!")
