import disnake

import file_manager


def is_admin(roles: list[int]) -> bool:
    admins = file_manager.get_admin_roles()
    for role in roles:
        if role in admins:
            return True
    return False
