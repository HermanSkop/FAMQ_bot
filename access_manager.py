import disnake

import config
import file_manager


def is_admin(user: disnake.Member, channel: disnake.TextChannel) -> bool:
    return channel.permissions_for(user).administrator


def add_shop(guild: disnake.Guild, content: [[str, int]]):
    file_manager.write_shop({guild.id: content})


def is_shop(interaction: disnake.Interaction, message_id: int):
    if interaction.data.get('custom_id'):
        id = interaction.data['custom_id'].split('_')
        if id[0] == config.custom_shop_id and id[1] == str(message_id):
            return True
    return False


def is_buy_button(interaction: disnake.Interaction, message_id: int):
    if interaction.data.get('custom_id'):
        id = interaction.data['custom_id'].split('_')
        if id[0] == config.custom_buy_button_id and id[1] == str(message_id):
            return True
    return False
