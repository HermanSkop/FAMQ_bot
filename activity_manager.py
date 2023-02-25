import datetime

import disnake
import pytz
import config
import file_manager


def update_activity(user: disnake.member):
    updated_user = count_played_time(user.id, user.activity.start)
    file_manager.update_json_file(updated_user, config.activity_file_path)


def count_played_time(user_id: int, start_time: datetime.datetime) -> {int: [int, int, int]}:
    """
    Sums up playing time and counts points for it
    :param start_time: time when user started playing
    :param user_id: user to be counted
    :return: dictionary of updated user as follows: {id: [minutes_played, points, max_points]}
    """
    user_activity = file_manager.parse_value_from_json(config.activity_file_path, user_id)

    if user_activity is None:
        user_activity = [0, 0, 0]
    mins = get_minutes(datetime.datetime.utcnow(), start_time) + user_activity[0]
    points = user_activity[1] + (mins // file_manager.get_minutes_for_points())
    mins %= file_manager.get_minutes_for_points()

    if user_activity[2] < points:
        max_points = points
    else:
        max_points = user_activity[2]

    return {
        user_id: [
            mins,
            points,
            max_points,
        ]
    }


def get_minutes(date1: datetime.datetime, date2: datetime.datetime) -> int:
    date1 = pytz.timezone('UTC').localize(date1)
    delta = date1 - date2
    return int(delta.total_seconds() / 60)


def create_stats_message(author: disnake.Member) -> disnake.Embed:
    embed = disnake.Embed(
        title='Статистика:',
        # description='Description of the Embed Message',
        color=disnake.Color.dark_magenta()
    )

    user_activity = file_manager.get_user_activity(author.id)
    # Add fields to the embed message
    embed.add_field(name='До следующего балла(мин):',
                    value=str(file_manager.get_minutes_for_points() - user_activity[0]),
                    inline=False)
    embed.add_field(name='Количество баллов:', value=str(user_activity[1]), inline=True)
    embed.add_field(name='Максимальное количество баллов:', value=str(user_activity[2]), inline=False)

    # Set the author of the embed message
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


def match_roles(existing_roles: list[str]) -> bool:
    needed_roles = file_manager.get_roles()
    for role in existing_roles:
        if role in needed_roles:
            return True
    return False