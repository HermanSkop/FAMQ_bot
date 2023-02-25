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


def parse_value_from_json(path, key: str | int):
    """
    :param key: key to find the value
    :param path: path to the json file
    :return: value by key
    """
    try:
        return read_json_file(path)[str(key)]
    except KeyError:
        return None


def parse_key_from_json(path, value: str) -> list[Any] | None:
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


def update_json_file(new_object: {str: str} | {int: int}, path):
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


def get_channels() -> list[int]:
    return parse_value_from_json(config.config_file_path, "channels")


def get_roles() -> list[str]:
    return parse_value_from_json(config.config_file_path, "roles")


def get_games() -> list[str]:
    return parse_value_from_json(config.config_file_path, "games")


def get_user_activity(user_id: int) -> [int, int, int]:
    act = parse_value_from_json(config.activity_file_path, user_id)
    if act is None:
        return [0, 0, 0]
    else:
        return act
