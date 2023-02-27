import datetime

import disnake
import pytz
import config
import file_manager


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
    mins = subtract(datetime.datetime.utcnow(), start_time) + user_activity[0]
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


def edit_number_of_points(user_id: int, points: int) -> {int: [int, int, int]}:
    activity = file_manager.get_user_activity(user_id)
    activity[1] += points
    if activity[1] < 0:
        activity[1] = 0
    if activity[2] < activity[1]:
        activity[2] = activity[1]
    return {user_id: activity}


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
