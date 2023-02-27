import disnake


def is_admin(user: disnake.Member, channel: disnake.TextChannel) -> bool:
    return channel.permissions_for(user).administrator
