import asyncio

import disnake
import access_manager
import activity_manager
import config
import file_manager
import messages
from config import bot


@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:\n')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print('\n')


@bot.event
async def on_presence_update(before: disnake.Member, after: disnake.Member):
    roles = [i.id for i in after.roles]
    if before.activity != after.activity \
            and before.activity is not None \
            and before.activity.name in file_manager.get_games() \
            and activity_manager.match_roles(roles):
        activity_manager.update_player(before.id, before.activity.start)


@bot.slash_command(name='reset', description='Сбросить статистику пользователя',
                   default_member_permissions=disnake.Permissions(8))
async def reset_user(ctx: disnake.ApplicationCommandInteraction, tag: str):
    if access_manager.is_admin(ctx.author, ctx.channel):
        if not tag.strip("<@!>").isdigit():
            await ctx.send(content=tag,
                           embed=messages.create_wrong_input_message(err_name=config.tag_err_name,
                                                                     err_description=config.tag_err_desc))
        else:
            user = ctx.guild.get_member(int(tag.strip("<@!>")))
            activity_manager.reset_user(ctx.guild.id, user.id)
            await ctx.send(content=tag, embed=messages.create_stats_message(user, ctx.guild.id))
    else:
        await ctx.send(embed=messages.create_no_rights_message())


@bot.slash_command(name='rate', description='Вывести таблицу лучших')
async def show_rate(ctx: disnake.ApplicationCommandInteraction):
    await ctx.send(embed=messages.create_rates_message(ctx.guild))


@bot.slash_command(name='tag', description='Тегнуть всех кто играет в GTAV',
                   default_member_permissions=disnake.Permissions(8))
async def tag_active(ctx: disnake.ApplicationCommandInteraction, message: str):
    await ctx.send(content=messages.create_tag_active_message(activity_manager.get_active_players(ctx.channel),
                                                              message))


@bot.slash_command(name='roles', description='Вывести список ролей с их ID и серверами',
                   default_member_permissions=disnake.Permissions(8))
async def roles(ctx: disnake.ApplicationCommandInteraction):
    await ctx.send(embed=messages.create_roles_message(bot.guilds))


@bot.slash_command(name='add_role', description='Добавить новую роль, для которой будет считаться время в игре',
                   default_member_permissions=disnake.Permissions(8))
async def add_role(ctx: disnake.ApplicationCommandInteraction, role_id: str):
    if role_id.isdigit():
        file_manager.write_role(int(role_id))
        await ctx.send(embed=messages.create_add_role_message(bot.guilds))
    else:
        await ctx.send(embed=messages.create_wrong_input_message(
            err_name='Неправильный ввод',
            err_description='Попробуйте ввести ID роли, например: 1078746439750004917'))


@bot.slash_command(name='remove_role',
                   description='Удалить роль из списка используемых ролей для подсчёта времени в игре',
                   default_member_permissions=disnake.Permissions(8))
async def remove_role(ctx: disnake.ApplicationCommandInteraction, role_id: str):
    if role_id.isdigit() and int(role_id) in file_manager.get_roles():
        file_manager.remove_role(int(role_id))
        await ctx.send(embed=messages.create_removed_role_message(bot.guilds))
    else:
        await ctx.send(embed=messages.create_wrong_input_message(
            err_name='Неправильный ввод',
            err_description='Вероятно такой роли не существует в списке ролей'))


@bot.slash_command(name='emend', description='Изменить количество баллов пользователя на n: username#0000, (-)n',
                   default_member_permissions=disnake.Permissions(8))
async def emend_points(ctx: disnake.ApplicationCommandInteraction, tag: str, points: int):
    if not tag.strip("<@!>").isdigit():
        await ctx.send(content=tag, embed=messages.create_wrong_input_message(err_name=config.tag_err_name,
                                                                              err_description=config.tag_err_desc))
    else:
        user = ctx.guild.get_member(int(tag.strip("<@!>")))
        if user is None or points is None:
            await ctx.send(embed=messages.create_help_message())
        else:
            file_manager.write_user_activity(
                ctx.guild.id, {user.id: activity_manager.edit_points(ctx.guild.id, user.id, points)}
            )
            await ctx.send(content=tag,
                           embed=messages.create_stats_message(ctx.guild.get_member(int(tag.strip("<@!>"))),
                                                               ctx.guild.id))


@bot.slash_command(name='profile', description='Узнай свою статистику')
async def print_stats(ctx: disnake.ApplicationCommandInteraction, tag: str):
    if not tag.strip("<@!>").isdigit():
        await ctx.send(content=tag,
                       embed=messages.create_wrong_input_message(err_name=config.tag_err_name,
                                                                 err_description=config.tag_err_desc))
    else:
        await ctx.send(embed=messages.create_stats_message(ctx.guild.get_member(int(tag.strip("<@!>"))),
                                                           ctx.guild.id))


@bot.slash_command(name='help', description='Команды и условия использования')
async def print_help(ctx: disnake.ApplicationCommandInteraction):
    await ctx.send(embed=messages.create_help_message())


@bot.slash_command(name='add_item', description='Добавить позицию в магазин',
                   default_member_permissions=disnake.Permissions(8))
async def add_item(ctx: disnake.ApplicationCommandInteraction, name: str, price: int):
    if file_manager.add_item([name, price], ctx.guild.id):
        await ctx.response.send_message(embed=messages.create_item_added_message([name, price]))
    else:
        await ctx.response.send_message(embed=messages.create_item_exists_message([name, price]))


@bot.slash_command(name='remove_item', description='Удалить товар из магазина',
                   default_member_permissions=disnake.Permissions(8))
async def remove_item(ctx: disnake.ApplicationCommandInteraction, name: str):
    file_manager.remove_item(name, ctx.guild.id)
    await ctx.response.send_message(embed=messages.create_item_removed_message())


async def buy(interaction: disnake.Interaction, item_id: int):
    item = file_manager.get_item(item_id, interaction.guild.id)
    if item is None:
        await interaction.response.edit_message(embed=messages.create_no_item_message(), content=None, components=[])
    else:
        if item[1] > file_manager.get_points(interaction.author.id, interaction.guild.id):
            await interaction.response.edit_message(embed=messages.create_no_money_message(),
                                                    content=None,
                                                    components=[])
        else:
            activity_manager.file_manager.write_user_activity(
                interaction.guild.id,
                {interaction.author.id:
                     activity_manager.edit_points(interaction.guild.id, interaction.author.id, -item[1])}
            )
            await interaction.response.edit_message(content=None,
                                                    components=[],
                                                    embed=messages.create_purchase_list(author=interaction.author,
                                                                                        item=item))
            await interaction.author.send(embed=messages.create_purchase_list(interaction.author, item))
            await interaction.guild.owner.send(embed=messages.create_purchase_list(interaction.author, item))


async def chose_item(interaction: disnake.Interaction):
    if isinstance(interaction, disnake.MessageInteraction):
        item_id = int(interaction.data.values[0])
        item = file_manager.get_item(item_id, interaction.guild.id)
        message_id = interaction.message.id

        if item is None:
            await interaction.response.edit_message(embed=messages.create_no_item_message(), content=None,
                                                    components=[])
        else:
            submit_button = disnake.ui.Button(label=str(item[1]) + ' pts',
                                              style=disnake.ButtonStyle.green,
                                              custom_id=config.custom_buy_button_id + '_' + str(interaction.message.id))
            action_row = disnake.ui.ActionRow(submit_button)
            await interaction.response.edit_message(
                content='Вы действительно хотите купить следующие товары?',
                embed=messages.create_shop_bill(item),
                components=[action_row]
            )
            button_interaction = await bot.wait_for("button_click",
                                                    check=lambda i: access_manager.is_buy_button(interaction=i,
                                                                                                 message_id=message_id))
            await buy(interaction=button_interaction, item_id=item_id)


@bot.slash_command(name='shop', description='Открыть магазин')
async def show_shop(ctx: disnake.ApplicationCommandInteraction):
    select_menu = messages.create_shop_Select_Menu(ctx.guild.id)
    message_id = ctx.channel.last_message_id
    if select_menu is None:
        await ctx.send(embed=messages.create_empty_shop_message())
    else:
        select_menu.custom_id = config.custom_shop_id + '_' + str(message_id)
        await ctx.send(content='МАГАЗИН:', components=[disnake.ui.ActionRow(select_menu)])
        try:
            interaction = await ctx.bot.wait_for(
                "interaction",
                check=lambda i: access_manager.is_shop(interaction=i,
                                                       message_id=message_id),
                timeout=config.shop_time_delay
            )
            await chose_item(interaction)
        except asyncio.TimeoutError:
            await ctx.delete_original_message()


bot.run(token="MTA3NzI3NTE1MDA5NDk2Njg3NQ.GmYZIB.KKSo2LfCG9dgr1qXIUugFp9N8GpBJ7z_xRRe3g")

# test MTA3OTcxNjMxNTgwOTQ1MjA4Mw.GMGVQe.Z9x_mjcNxkZlr3bz1bUU9bEsXUamGbgo1En2yM
