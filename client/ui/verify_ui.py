import datetime
from typing import Optional

from client import config
import disnake
from datetime import datetime
from disnake.ext.commands import InteractionBot, BucketType
import traceback
import tracemalloc


class RateModal(disnake.ui.Modal):
    def __init__(self, rate, admin, client, guild) -> None:
        self.admin = admin
        self.rate = rate
        self.client: InteractionBot = client
        self.guild = guild
        self.db = self.client.cluster.moon
        self.staff_collection = self.db.verify_collection
        components = [
            disnake.ui.TextInput(
                label="Укажите свой комментарий",
                placeholder="Ассистент очень приятно общался со мной!",
                custom_id="comment",
                style=disnake.TextInputStyle.short,
                min_length=5,
                max_length=200,
            ),
        ]
        super().__init__(title="Оценка работы", custom_id="rate", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        comment = inter.text_values['comment']
        channel = self.client.get_channel(
            config.BOT_INFO['VERIFY_LOG_CHANNEL_ID'])

        embed = disnake.Embed()
        embed.set_author(name="Логи верификации")
        embed.add_field(name="Отправитель", value=inter.author, inline=True)
        embed.add_field(name="Комментарий",
                        value=f"```\n{comment}\n```", inline=False)
        embed.add_field(
            name="Оценка", value=f"`{self.rate} / 5`", inline=False)
        embed.set_footer(text=f"\u200b Верифицировал {self.admin}")
        embed.timestamp = datetime.now()

        embed2 = disnake.Embed()
        embed2.title = "Обратная связь"
        embed2.description = "> Спасибо за ваш отзыв"
        embed2.timestamp = datetime.now()
        embed2.set_footer(text=f"\u200b")

        await inter.response.send_message(embed=embed2, ephemeral=True)
        await channel.send(embed=embed)


class Buttons(disnake.ui.View):
    def __init__(self, admin, client, guild):
        self.admin = admin
        self.client: InteractionBot = client
        self.guild = guild
        self.db = self.client.cluster.moderator_db
        self.staff_collection = self.db.staff_collection
        super().__init__(timeout=None)

    @disnake.ui.button(label="1", style=disnake.ButtonStyle.grey, custom_id="one")
    async def one(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.staff_collection.find_one({"_id": self.admin.id}):
            await self.staff_collection.update_one({"_id": self.admin.id}, {"$inc": {"rate": 1}})
            print(self.admin.id)
            print("rate 1")
            await inter.response.send_modal(RateModal(rate=1, admin=self.admin, client=self.client, guild=self.guild))

            self.one.disabled = True
            self.two.disabled = True
            self.three.disabled = True
            self.four.disabled = True
            self.five.disabled = True
            await inter.edit_original_response(view=self)

    @disnake.ui.button(label="2", style=disnake.ButtonStyle.grey, custom_id="two")
    async def two(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.staff_collection.find_one({"_id": self.admin.id}):
            await self.staff_collection.update_one({"_id": self.admin.id}, {"$inc": {"rate": 2}})
            print(self.admin.id)
            print("rate 2")
            await inter.response.send_modal(RateModal(rate=2, admin=self.admin, client=self.client, guild=self.guild))

            self.one.disabled = True
            self.two.disabled = True
            self.three.disabled = True
            self.four.disabled = True
            self.five.disabled = True
            await inter.edit_original_response(view=self)

    @disnake.ui.button(label="3", style=disnake.ButtonStyle.grey, custom_id="three")
    async def three(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.staff_collection.find_one({"_id": self.admin.id}):
            await self.staff_collection.update_one({"_id": self.admin.id}, {"$inc": {"rate": 3}})
            print(self.admin.id)
            print("rate 3")
            await inter.response.send_modal(RateModal(rate=3, admin=self.admin, client=self.client, guild=self.guild))

            self.one.disabled = True
            self.two.disabled = True
            self.three.disabled = True
            self.four.disabled = True
            self.five.disabled = True
            await inter.edit_original_response(view=self)

    @disnake.ui.button(label="4", style=disnake.ButtonStyle.grey, custom_id="four")
    async def four(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.staff_collection.find_one({"_id": self.admin.id}):
            await self.staff_collection.update_one({"_id": self.admin.id}, {"$inc": {"rate": 4}})
            print(self.admin.id)
            print("rate 4")
            await inter.response.send_modal(RateModal(rate=4, admin=self.admin, client=self.client, guild=self.guild))

            self.one.disabled = True
            self.two.disabled = True
            self.three.disabled = True
            self.four.disabled = True
            self.five.disabled = True
            message = inter.original_message()
            await inter.edit_original_response(view=self)

    @disnake.ui.button(label="5", style=disnake.ButtonStyle.grey, custom_id="five")
    async def five(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.staff_collection.find_one({"_id": self.admin.id}):
            await self.staff_collection.update_one({"_id": self.admin.id}, {"$inc": {"rate": 5}})
            print(self.admin.id)
            print("rate 5")
            await inter.response.send_modal(RateModal(rate=5, admin=self.admin, client=self.client, guild=self.guild))

            self.one.disabled = True
            self.two.disabled = True
            self.three.disabled = True
            self.four.disabled = True
            self.five.disabled = True
            await inter.edit_original_response(view=self)


class Btn_Verify(disnake.ui.Button):
    def __init__(self, *, roles_ids: list, member: disnake.Member,
                 style: disnake.ButtonStyle = disnake.ButtonStyle.gray, emoji: Optional[str] = None,
                 label: Optional[str] = None, staff_collection, collection, admin, guild, client):
        super().__init__(style=style, label=label, emoji=emoji)
        self.staff_collection = staff_collection
        self.collection = collection
        self.client: InteractionBot = client
        self.admin = admin
        self.guild = guild
        if not isinstance(roles_ids, (int, list)):
            raise ValueError("Неправильный тип role_name")
        if not isinstance(member, disnake.Member):
            raise ValueError("Неправильный тип member")
        self.roles_ids = roles_ids
        self.member = member

    async def callback(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)
        if self.roles_ids[0] == 'DELETE_ALL_ROLES':
            for role_id in config.BOT_INFO['ROLES'].values():
                if role_id is None:
                    continue
                role = disnake.utils.get(
                    interaction.guild.roles, id=int(role_id))
                if role in (await interaction.guild.fetch_member(self.member.id)).roles:
                    await self.member.remove_roles(role)
            await self.collection.update_one({"_id": self.member.id}, {"$set": {"dont_allowed": False}})
            await interaction.followup.send("Успешно удалены все роли!", ephemeral=True)
            embed_member = disnake.Embed(color=0x2f3136)
            embed_member.set_author(
                name="Вам удалили роли верификации!", icon_url=self.member.display_avatar.url)
            embed_member.description = f">>> Все роли **верифицации** были удалены!"
            embed_member.set_footer(text=f"Выполнил(а) {interaction.user}")
            try:
                await self.member.send(embed=embed_member)
            except disnake.Forbidden:
                pass
            return

        for role_id in config.BOT_INFO['ROLES'].values():
            if role_id is None:
                continue
            role = disnake.utils.get(interaction.guild.roles, id=int(role_id))
            if role in (await interaction.guild.fetch_member(self.member.id)).roles:
                await self.member.remove_roles(role)
        for role_id in self.roles_ids:
            if role_id is None:
                continue
            if role_id == config.BOT_INFO['ROLES']['NOT_ALLOWED_ROLE_ID']:
                embed_member = disnake.Embed(color=0x2f3136)
                embed_member.set_author(
                    name="Вам был выдан недопуск!", icon_url=self.member.display_avatar.url)
                embed_member.description = f">>> Вы получили **недопуск** к верификации!"
                embed_member.set_footer(text=f"Выполнил(а) {interaction.user}")
                try:
                    await self.member.send(embed=embed_member)
                except disnake.Forbidden:
                    pass
                role = disnake.utils.get(
                    interaction.guild.roles, id=int(role_id))
                await self.collection.update_one({"_id": self.member.id}, {"$set": {"dont_allowed": True}})
                await self.staff_collection.update_one({"_id": interaction.author.id}, {"$push": {
                    "verifies": {'type': "dont_allowed", "user_id": self.member.id, "date_issue": datetime.now()}}})
                try:
                    await self.member.edit(roles=[role])
                except disnake.HTTPException:
                    pass

                emb = disnake.Embed(
                    color=0x2f3136, title='Управление пользователем')
                emb.description = f'{interaction.user.mention}, выдал **недопуск** пользователю {self.member.mention}'
                emb.timestamp = datetime.now()
                await interaction.edit_original_response(embed=emb, view=None)
                if config.BOT_INFO['VERIFY_LOG_CHANNEL_ID']:
                    embed_log = disnake.Embed(
                        color=0x2f3136, title='Логи верификации')
                    embed_log.add_field(
                        name='>>> Выдан недопуск к:', value=self.member.mention, inline=False)
                    embed_log.add_field(
                        name='>>> Выдал недопуск:', value=interaction.user.mention, inline=False)
                    embed_log.timestamp = datetime.now()
                    embed_log.set_thumbnail(url=self.member.display_avatar.url)
                    log_channel = interaction.bot.get_channel(
                        int(config.BOT_INFO['VERIFY_LOG_CHANNEL_ID']))
                    await log_channel.send(embed=embed_log)
                await interaction.followup.send('Роль успешно добавилась!', ephemeral=True)
                return
            role = disnake.utils.get(interaction.guild.roles, id=int(role_id))
            await self.member.add_roles(role)
        embed_member = disnake.Embed(color=0x2f3136)
        embed_member.set_author(
            name="Вам выдали верификацию!", icon_url=self.member.display_avatar.url)
        embed_member.description = f">>> Вы **успешно** получили **верифицацию** на сервер!"
        embed_member.set_footer(text=f"Выполнил(а) {interaction.user}")

        embed2_member = disnake.Embed(color=0x2f3136)
        embed2_member.set_author(
            name="Отзыв о работе", icon_url=self.member.display_avatar.url)
        embed2_member.description = f"> Для улучшения качества работы, вы можете оценить работу Welcomer'a."
        embed2_member.set_footer(text=f"Выполнил(а) {interaction.user}")
        try:
            await self.member.send(embed=embed_member)
            await self.member.send(embed=embed2_member, view=Buttons(admin=self.admin, client=self.client, guild=self.guild))
        except disnake.Forbidden:
            pass
        await interaction.followup.send('Роль успешно добавилась!', ephemeral=True)
        emb = disnake.Embed(color=0x2f3136, title='Управление пользователем')
        _ = '**парня**' if config.BOT_INFO['ROLES']['MALE_ROLE_ID'] in self.roles_ids else "**девушку**"
        emb.description = f'{interaction.user.mention}, **верифицировал** пользователя {self.member.mention} как {_}'
        emb.timestamp = datetime.now()
        emb.set_thumbnail(url=self.member.display_avatar.url)
        type_ = 'male' if config.BOT_INFO['ROLES']['MALE_ROLE_ID'] in self.roles_ids else "female"
        await self.staff_collection.update_one({"_id": interaction.author.id}, {"$push": {"verifies": {'type': type_, "user": self.member.id, "date_issue": datetime.now()}}})
        if config.BOT_INFO['VERIFY_LOG_CHANNEL_ID']:
            _ = '**парень**' if config.BOT_INFO['ROLES']['MALE_ROLE_ID'] in self.roles_ids else "**девушка**"
            embed_log = disnake.Embed(color=0x2f3136, title='Логи верификации')
            embed_log.add_field(
                name=f'>>> Верифицирован(а) как: {_}', value=self.member.mention, inline=False)
            embed_log.add_field(name='>>> Верифицировал:',
                                value=interaction.user.mention, inline=False)
            embed_log.timestamp = datetime.now()
            embed_log.set_thumbnail(url=self.member.display_avatar.url)
            log_channel = interaction.bot.get_channel(
                int(config.BOT_INFO['VERIFY_LOG_CHANNEL_ID']))
            await log_channel.send(embed=embed_log)
        await interaction.edit_original_response(embed=emb, view=None)


class Verify(disnake.ui.View):
    def __init__(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, author,
                 roles: tuple, collection, staff_collection, admin, guild, client):
        super().__init__(timeout=30)
        self.interaction = interaction
        self.user = author
        self.member = member
        self.admin = admin
        self.guild = guild
        self.client = client
        for role_name, role_id in roles:
            if role_id is None:
                continue
            if role_name == 'MALE_ROLE_ID':
                self.add_item(Btn_Verify(roles_ids=[config.BOT_INFO['ROLES']['MALE_ROLE_ID'],
                                                    config.BOT_INFO['ROLES']['VERIFY_ROLE_ID']],
                                         member=self.member, emoji='♂', staff_collection=staff_collection,
                                         collection=collection, admin=self.admin, guild=self.guild, client=self.client))
            if role_name == 'FEMALE_ROLE_ID':
                self.add_item(Btn_Verify(roles_ids=[config.BOT_INFO['ROLES']['FEMALE_ROLE_ID'],
                                                    config.BOT_INFO['ROLES']['VERIFY_ROLE_ID']],
                                         member=self.member, emoji='♀', staff_collection=staff_collection,
                                         collection=collection, admin=self.admin, guild=self.guild, client=self.client))
            if role_name == 'NOT_ALLOWED_ROLE_ID':
                self.add_item(Btn_Verify(roles_ids=[config.BOT_INFO['ROLES']['NOT_ALLOWED_ROLE_ID']],
                                         member=self.member, label='Недопуск', staff_collection=staff_collection,
                                         collection=collection, admin=self.admin, guild=self.guild, client=self.client))
        if len(self.children) == 0 and config.BOT_INFO['ROLES']['VERIFY_ROLE_ID'] is not None:
            self.add_item(Btn_Verify(roles_ids=[config.BOT_INFO['ROLES']['VERIFY_ROLE_ID']],
                                     member=self.member, label='Верифицировать', staff_collection=staff_collection,
                                     collection=collection, admin=self.admin, guild=self.guild, client=self.client))
        if not (len(self.children) == 0):
            self.add_item(Btn_Verify(roles_ids=["DELETE_ALL_ROLES"],
                                     member=self.member, label='Удалить все роли',
                                     style=disnake.ButtonStyle.red, staff_collection=staff_collection,
                                     collection=collection, admin=self.admin, guild=self.guild, client=self.client))

    async def interaction_check(self, interaction: disnake.ApplicationCommandInteraction) -> bool:
        if self.user:
            if interaction.user != self.user:
                try:
                    await interaction.response.send_message("Это команда работает для кого-то другого!", ephemeral=True)
                except disnake.InteractionResponded:
                    await interaction.followup.send("Это команда работает для кого-то другого!", ephemeral=True)
                return False
        return True

    async def on_timeout(self) -> None:
        await self.interaction.edit_original_response(view=None)
