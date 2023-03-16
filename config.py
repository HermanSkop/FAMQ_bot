import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

files_path = 'files/'
activity_file_path = files_path + 'activity.json'
out_file_path = files_path + 'out.txt'
config_file_path = files_path + 'config.json'
logs_file_path = files_path + 'logs.txt'
shops_file_path = files_path + 'shops.json'
last_join_path = files_path + 'last_join.json'

rate_people_quantity = 10
shop_time_delay = 60

tag_err_name = 'Неверно введён тег пользователя!'
tag_err_desc = 'Тег должен выглядеть примерно так: @Mavlo#7777, а так же подсвечиваться фиолетовым цветом.'

custom_shop_id = 'shop'
custom_buy_button_id = 'button'
