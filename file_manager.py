import datetime
import json
from json import JSONDecodeError
from typing import Any

import config


def read_json_file(path) -> dict:
    """
    Loads the whole json file
    :param path: path to the file
    :return: json object depending on content, f.e. dict
    """
    try:
        with open(path, 'r', encoding="utf8") as openfile:
            json_object = json.load(openfile)
        return json_object
    except JSONDecodeError:
        return {}


def parse_value_from_json(path, key):
    """
    :param key: key to find the value
    :param path: path to the json file
    :return: value by key
    """
    try:
        return read_json_file(path)[str(key)]
    except KeyError:
        return None


def parse_key_from_json(path, value: str):
    try:
        dic = read_json_file(path)
        return [key for key in dic if dic[key] == value]
    except KeyError:
        return None


def write_to_json_file(json_object, path):
    with open(path, "w", encoding="utf8") as outfile:
        outfile.write(json.dumps(json_object, ensure_ascii=False, indent=4))


def read_txt_file(path) -> list:
    with open(path, "r", encoding="utf8") as openfile:
        content = openfile.read().split("\n")
    return content


def write_to_txt_file(obj, path):
    with open(path, "w") as openfile:
        openfile.write(str(obj) + '\n')


def write_all_to_txt_file(obj: list, path):
    if len(obj) == 0:
        write_to_txt_file('', path)
    for i in obj:
        write_to_txt_file(i, path)


def update_json_file(new_object, path):
    file_content = read_json_file(path)
    for key, value in new_object.items():
        key = str(key)
        if key in file_content.keys():
            file_content[key] = value
        else:
            file_content.update({key: value})
    write_to_json_file(file_content, path)


def get_minutes_for_points() -> int:
    return parse_value_from_json(config.config_file_path, "minutes_for_point")


def get_roles() -> list[int]:
    return parse_value_from_json(config.config_file_path, "roles")


def get_games() -> list[str]:
    return parse_value_from_json(config.config_file_path, "games")


def get_admin_roles() -> list[int]:
    return parse_value_from_json(config.config_file_path, "admin_roles")


def get_user_activity(guild_id: int, user_id: int) -> [int, int, int]:
    user_id = str(user_id)
    guild = get_guild(guild_id)
    if user_id not in guild:
        return [0, 0, 0]
    else:
        return guild[user_id]


def get_guild(guild_id: int) -> {}:
    guild = parse_value_from_json(config.activity_file_path, guild_id)
    if guild is None:
        return {}
    return guild


def get_activities() -> {str: [int, int, int]}:
    player = read_json_file(config.activity_file_path)
    if player is None:
        return {}
    else:
        return player


def get_points(user_id: int, guild_id: int) -> int:
    return get_user_activity(guild_id, user_id)[1]


def write_user_activity(guild_id: int, user: {int: [int, int, int]}):
    updated_guild = update_guild(guild_id, user)
    update_json_file({guild_id: updated_guild}, config.activity_file_path)


def update_guild(guild_id: int, updated_user: {int: [int, int, int]}) -> {str: [int, int, int]}:
    guild = get_guild(guild_id)
    if guild is None:
        guild = {}
    updated_user = {str(key): value for key, value in updated_user.items()}

    guild.update(updated_user)
    return guild


def update_guilds(updated_guild: {int: {int: [int, int, int]}}):
    if updated_guild is None:
        return
    update_json_file(updated_guild, config.activity_file_path)


def get_guilds() -> {str: {str: [int, int, int]}}:
    guilds = read_json_file(config.activity_file_path)
    if guilds is None:
        return {}
    return guilds


def write_role(role_id: int):
    roles = parse_value_from_json(config.config_file_path, "roles")
    if roles is None:
        roles = []
    if role_id not in roles:
        roles.append(role_id)
    update_json_file({"roles": roles}, config.config_file_path)


def remove_role(role_id: int):
    roles = parse_value_from_json(config.config_file_path, "roles")
    if roles is None or role_id not in roles:
        return
    roles.remove(role_id)
    update_json_file({"roles": roles}, config.config_file_path)


def write_shop(dto: {int: [[str, int]]}):
    write_to_json_file(dto, config.shops_file_path)


def get_shop_content(guild_id: int) -> [[str, int]]:
    shop = parse_value_from_json(config.shops_file_path, guild_id)
    if shop is None:
        shop = []
    return shop


def get_item(item_id: int, guild_id: int) -> [str, int]:
    content = get_shop_content(guild_id)
    if len(content) > int(item_id) and len(content[item_id]) == 2:
        return content[int(item_id)]
    else:
        return None


def add_item(item: [str, int], guild_id: int) -> bool:
    shop = get_shop_content(guild_id)
    if item in shop:
        return False
    shop.append(item)
    write_shop({guild_id: shop})
    return True


def remove_item(name: str, guild_id: int):
    shop = [item for item in get_shop_content(guild_id) if name not in item]
    write_shop({guild_id: shop})


def get_last_join(user_id: id) -> str:
    return parse_value_from_json(config.last_join_path, str(user_id))


def write_last_join(user_id: id, last_time: str):
    update_json_file({user_id: last_time}, config.last_join_path)


def toggle_paused_guild(guild_id: int) -> bool:
    """
    Adds id to paused if there is no such id yet. Otherwise, removes id from the list
    :param guild_id: id of guild to be toggled
    :return: true if added and false if removed
    """
    guild_id = str(guild_id)
    added = False
    guild_ids = read_txt_file(config.paused_guilds_path)
    if guild_id not in guild_ids:
        guild_ids.append(guild_id)
        added = True
    else:
        guild_ids.remove(guild_id)
    write_all_to_txt_file(guild_ids, config.paused_guilds_path)
    return added


def paused_guilds() -> list:
    return read_txt_file(config.paused_guilds_path)