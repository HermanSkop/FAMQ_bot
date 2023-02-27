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


def write_to_txt_file(o, path):
    with open(path, "a") as openfile:
        openfile.write(o + '\n')


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


def get_user_activity(user_id: int) -> [int, int, int]:
    act = parse_value_from_json(config.activity_file_path, user_id)
    if act is None:
        return [0, 0, 0]
    else:
        return act


def get_activities() -> {str: [int, int, int]}:
    player = read_json_file(config.activity_file_path)
    if player is None:
        return {}
    else:
        return player


def write_user_activity(dto: {int: [int, int, int]}):
    update_json_file(dto, config.activity_file_path)


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

