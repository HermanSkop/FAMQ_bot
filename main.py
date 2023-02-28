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
async def on_presence_update(before, after):
    roles = [i.id for i in after.roles]
    if before.activity != after.activity \
            and before.activity is not None \
            and before.activity.name in file_manager.get_games() \
            and activity_manager.match_roles(roles):
        file_manager.write_user_activity(activity_manager.count_played_time(before.id, before.activity.start))


@bot.slash_command(name='reset', description='Сбросить статистику пользователя')
async def reset_user(ctx: disnake.ApplicationCommandInteraction, tag: str):
    if access_manager.is_admin(ctx.author, ctx.channel):
        if not tag.strip("<@!>").isdigit():
            await ctx.send(content=tag,
                           embed=messages.create_wrong_input_message(err_name=config.tag_err_name,
                                                                     err_description=config.tag_err_desc))
        else:
            user = ctx.guild.get_member(int(tag.strip("<@!>")))
            activity_manager.reset_user(user.id)
            await ctx.send(embed=messages.create_stats_message(user))
    else:
        await ctx.send(embed=messages.create_no_rights_message())


@bot.slash_command(name='rate', description='Вывести таблицу лучших')
async def show_rate(ctx: disnake.ApplicationCommandInteraction):
    await ctx.send(embed=messages.create_rates_message(ctx.guild))


@bot.slash_command(name='tag', description='Тегнуть всех кто играет в GTAV')
async def tag_active(ctx: disnake.ApplicationCommandInteraction, message: str):
    if access_manager.is_admin(ctx.author, ctx.channel):
        await ctx.send(content=messages.create_tag_active_message(activity_manager.get_active_players(ctx.channel),
                                                                  message))
    else:
        await ctx.send(embed=messages.create_no_rights_message())


@bot.slash_command(name='roles', description='Вывести список ролей с их ID и серверами')
async def roles(ctx: disnake.ApplicationCommandInteraction):
    if access_manager.is_admin(ctx.author, ctx.channel):
        await ctx.send(embed=messages.create_roles_message(bot.guilds))
    else:
        await ctx.send(embed=messages.create_no_rights_message())


@bot.slash_command(name='add_role', description='Добавить новую роль, для которой будет считаться время в игре')
async def add_role(ctx: disnake.ApplicationCommandInteraction, role_id: str):
    if access_manager.is_admin(ctx.author, ctx.channel):
        if role_id.isdigit():
            file_manager.write_role(int(role_id))
            await ctx.send(embed=messages.create_add_role_message(bot.guilds))
        else:
            await ctx.send(embed=messages.create_wrong_input_message(
                err_name='Неправильный ввод',
                err_description='Попробуйте ввести ID роли, например: 1078746439750004917'))
    else:
        await ctx.send(embed=messages.create_no_rights_message())


@bot.slash_command(name='remove_role',
                   description='Удалить роль из списка используемых ролей для подсчёта времени в игре')
async def remove_role(ctx: disnake.ApplicationCommandInteraction, role_id: str):
    if access_manager.is_admin(ctx.author, ctx.channel):
        if role_id.isdigit() and int(role_id) in file_manager.get_roles():
            file_manager.remove_role(int(role_id))
            await ctx.send(embed=messages.create_removed_role_message(bot.guilds))
        else:
            await ctx.send(embed=messages.create_wrong_input_message(
                err_name='Неправильный ввод',
                err_description='Вероятно такой роли не существует в списке ролей'))
    else:
        await ctx.send(embed=messages.create_no_rights_message())


@bot.slash_command(name='emend', description='Изменить количество баллов пользователя на n: username#0000, (-)n')
async def emend_points(ctx: disnake.ApplicationCommandInteraction, tag: str, points: int):
    if access_manager.is_admin(ctx.author, ctx.channel):
        if not tag.strip("<@!>").isdigit():
            await ctx.send(content=tag, embed=messages.create_wrong_input_message(err_name=config.tag_err_name,
                                                                                err_description=config.tag_err_desc))
        else:
            user = ctx.guild.get_member(int(tag.strip("<@!>")))
            if user is None or points is None:
                await ctx.send(embed=messages.create_help_message())
            else:
                file_manager.write_user_activity(
                    activity_manager.edit_number_of_points(user.id, points)
                )
                await ctx.send(content=tag, embed=messages.create_stats_message(ctx.guild.get_member(int(tag.strip("<@!>")))))
    else:
        await ctx.send(embed=messages.create_no_rights_message())


@bot.slash_command(name='stats', description='Узнай свою статистику')
async def print_stats(ctx: disnake.ApplicationCommandInteraction, tag: str):
    if not tag.strip("<@!>").isdigit():
        await ctx.send(content=tag,
                       embed=messages.create_wrong_input_message(err_name=config.tag_err_name,
                                                                 err_description=config.tag_err_desc))
    else:
        await ctx.send(embed=messages.create_stats_message(ctx.guild.get_member(int(tag.strip("<@!>")))))


@bot.slash_command(name='help', description='Команды и условия использования')
async def print_help(ctx: disnake.ApplicationCommandInteraction):
    await ctx.send(embed=messages.create_help_message())


bot.run(token='MTA3OTcxNjMxNTgwOTQ1MjA4Mw.GFGsbL.KxXcQQ9XsCJlA6PErAXYs1i146KGTI_TztvsRQ')
