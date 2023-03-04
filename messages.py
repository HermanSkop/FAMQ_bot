import disnake
import activity_manager
import file_manager
from config import custom_shop_id


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


def create_shop_Select_Menu(guild_id: int):
    content = file_manager.get_shop_content(guild_id)
    if len(content) == 0:
        return None

    options = [disnake.SelectOption(label=item[0] + ': ' + str(item[1]) + ' pts',
                                    value=content.index(item)) for item in content]

    return disnake.ui.StringSelect(
        options=options,
        placeholder="Выберете товар",
        min_values=1,
        max_values=1
    )


def create_no_item_message():
    embed = disnake.Embed(
        title='Покупка прервана',
        color=disnake.Color.brand_red()
    )
    embed.add_field(name='Товара больше нет в магазине', value='Обратитесь за помощью к администрации')
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_empty_shop_message() -> disnake.Embed:
    embed = disnake.Embed(
        title='Магазин пуст!',
        color=disnake.Color.brand_red()
    )
    embed.add_field(name='Кажется администрация вашего сервера ещё не заполнила магазин.', value='')
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_shop_bill(items: [str, int]) -> disnake.Embed:
    embed = disnake.Embed(color=disnake.Color.orange())
    embed.description = "```" + items[0] + ' | ' + str(items[1]) + " pts```"
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_purchase_list(author: disnake.Member, item: [str, int]):
    embed = disnake.Embed(color=disnake.Color.greyple())
    embed.title = 'Куплены следующие товары:'
    embed.description = f"{item[0]} | {str(item[1])} pts"
    embed.set_author(name=author,
                     icon_url=author.avatar.url)
    return embed


def create_no_money_message():
    embed = disnake.Embed(color=disnake.Color.brand_red())
    embed.title = 'Покупка прервана!'
    embed.add_field(name='Недостаточно средств на счету', value='')
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_item_added_message(item: [str, int]):
    embed = disnake.Embed(color=disnake.Color.brand_green())
    embed.title = 'Товар успешно добавлен в магазин'
    embed.add_field(name=item[0], value=str(item[1])+' pts')
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_item_exists_message(item: [str, int]):
    embed = disnake.Embed(color=disnake.Color.brand_red())
    embed.title = 'Товар невозможно добавить в магазин'
    embed.add_field(name='Данный товар уже есть в магазине', value=item[0] + ' | ' + str(item[1])+' pts')
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed


def create_item_removed_message():
    embed = disnake.Embed(color=disnake.Color.brand_green())
    embed.title = 'Товара в магазине больше нет'
    embed.set_footer(text='Больше можно узнать командой: /help')
    return embed
