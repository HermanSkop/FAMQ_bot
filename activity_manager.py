import datetime

import disnake
import pytz
import config
import file_manager


def update_player(user_id: int, start_time: datetime.datetime):
    """
    Performs count_played_time() on every guild for given user_id
    :param start_time: time when user started playing
    :param user_id: user to be counted
    """
    for guild_id in file_manager.get_guilds():
        file_manager.write_user_activity(guild_id, count_played_time(guild_id, user_id, start_time))


def count_played_time(guild_id: int, user_id: int, start_time: datetime.datetime) -> {int: [int, int, int]}:
    """
    Sums up playing time and counts points for it
    :param guild_id: guild to count points for
    :param start_time: time when user started playing
    :param user_id: user to be counted
    :return: dictionary of updated user as follows: {id: [minutes_played, points, max_points]}
    """
    user_activity = file_manager.get_user_activity(guild_id, user_id)

    mins = subtract(datetime.datetime.utcnow(), start_time) + user_activity[0]
    points = user_activity[1] + (mins // file_manager.get_minutes_for_points())
    mins %= file_manager.get_minutes_for_points()

    if user_activity[2] < points:
        max_points = points
    else:
        max_points = user_activity[2]

    # TODO logs
    file_manager.write_to_txt_file('user: ' + str(user_id) +
                                   ' | start: ' + str(start_time) +
                                   ' | end: ' + str(datetime.datetime.utcnow()) +
                                   ' | points added: ' + str(points) +
                                   ' | minutes played: ' + str(mins), config.logs_file_path)

    return {
        user_id: [
            mins,
            points,
            max_points,
        ]
    }


def subtract(date1: datetime.datetime, date2: datetime.datetime) -> int:
    date1 = pytz.timezone('UTC').localize(date1)
    delta = date1 - date2
    return int(delta.total_seconds() / 60)


def match_roles(existing_roles: list[int]) -> bool:
    needed_roles = file_manager.get_roles()
    for role in existing_roles:
        if role in needed_roles:
            return True
    return False


def edit_points(guild_id: int, user_id: int, points: int) -> [int, int, int]:
    activity = file_manager.get_user_activity(guild_id, user_id)
    activity[1] += points
    if activity[1] < 0:
        activity[1] = 0
    if activity[2] < activity[1]:
        activity[2] = activity[1]

    # TODO logs
    file_manager.write_to_txt_file('user: ' + str(user_id) +
                                   ' | points added: ' + str(points) +
                                   ' | final minutes: ' + str(activity[0]) +
                                   ' | final points: ' + str(activity[1]) +
                                   ' | final max points: ' + str(activity[2]), config.logs_file_path)

    return activity


def update_points(guild_id: int, user_id: int, points: int):
    edited_user = {user_id: edit_points(guild_id, user_id, points)}
    file_manager.write_user_activity(guild_id, edited_user)


def get_active_players(channel: disnake.TextChannel) -> str:
    players = ''
    games = file_manager.get_games()
    for user in channel.members:
        roles = [i.id for i in user.roles]
        if user.activity is not None and user.activity.name in games and match_roles(roles):
            players += '<@' + str(user.id) + '>'
    return players


def get_best_players(server: disnake.Guild) -> list[disnake.Member]:
    player_activities = file_manager.get_activities()
    players = []
    player_activities = sorted(player_activities.items(), key=lambda e: e[1][2], reverse=True)
    for player_id, _ in player_activities:
        player = server.get_member(int(player_id))
        if player is not None:
            players.append(player)
    return players[0:config.rate_people_quantity]


def reset_user(guild_id: int, user_id: int):
    file_manager.write_user_activity(guild_id, {user_id: [0, 0, 0]})
