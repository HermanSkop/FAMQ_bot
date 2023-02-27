import disnake

import activity_manager
import file_manager


def create_stats_message(author: disnake.Member) -> disnake.Embed:
    embed = disnake.Embed(
        title='Статистика:',
        color=disnake.Color.dark_magenta()
    )
    user_activity = file_manager.get_user_activity(author.id)
    embed.add_field(name='До следующего балла(мин):',
                    value=str(file_manager.get_minutes_for_points() - user_activity[0]),
                    inline=False)
    embed.add_field(name='Количество баллов:', value=str(user_activity[1]), inline=True)
    embed.add_field(name='Максимальное количество баллов:', value=str(user_activity[2]), inline=False)
    embed.set_author(name=author, icon_url=author.avatar)
    return embed


def create_help_message() -> disnake.Embed:
    embed = disnake.Embed(
        title='Need help?',
        # description='Description of the Embed Message',
        color=disnake.Color.blue()
    )
    embed.add_field(name='some help..?', value='asd')
    return embed


def create_no_rights_message() -> disnake.Embed:
    embed = disnake.Embed(
        title='Команда недоступна!',
        color=disnake.Color.brand_red()
    )
    embed.add_field(name='Кажется вы пытаетесь воспользоваться командой, \nна которую у вас нет прав.',
                    value='')
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_add_role_message(guilds: list[disnake.Guild]) -> disnake.Embed:
    embed = disnake.Embed(
        title='Роль добавлена',
        color=disnake.Color.green()
    )

    embed.add_field(name='Доступные роли:', value='', inline=False)
    add_embed_roles_list(guilds, embed)
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_removed_role_message(guilds: list[disnake.Guild]) -> disnake.Embed:
    embed = disnake.Embed(
        title='Роль удалена',
        color=disnake.Color.yellow()
    )

    embed.add_field(name='Доступные роли:', value='', inline=False)
    add_embed_roles_list(guilds, embed)
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_roles_message(guilds: list[disnake.Guild]) -> disnake.Embed:
    embed = disnake.Embed(
        title='Доступные роли:',
        color=disnake.Color.teal()
    )
    add_embed_roles_list(guilds, embed)
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_wrong_input_message(err_name: str, err_description: str) -> disnake.Embed:
    embed = disnake.Embed(
        title='Ошибка!',
        color=disnake.Color.brand_red()
    )
    embed.add_field(name=err_name, value=err_description)
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def add_embed_roles_list(guilds: list[disnake.Guild], embed_message: disnake.Embed):
    roles = file_manager.get_roles()
    for role_id in roles:
        for guild in guilds:
            role = guild.get_role(role_id)
            if role is not None:
                embed_message.add_field(name=role.name, value='Сервер: ' + role.guild.name + '\n ID: ' + str(role.id),
                                        inline=False)


def create_tag_active_message(tags: str, message: str):
    return tags + '\n\n' + message


def create_rates_message(server: disnake.Guild):
    embed = disnake.Embed(
        title='Рейтинг лучших',
        color=disnake.Color.dark_gold()
    )
    pos = 1
    for player in activity_manager.get_best_players(server):
        embed.add_field(name='#' + str(pos) + ' ' + str(player),
                        value=file_manager.get_user_activity(player.id)[2],
                        inline=False)
        pos += 1
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed
