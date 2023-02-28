import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

files_path = 'files/'
activity_file_path = files_path + 'activity.json'
out_file_path = files_path + 'out.txt'
config_file_path = files_path + 'config.json'

rate_people_quantity = 10

tag_err_name = 'Неверно введён тег пользователя!'
tag_err_desc = 'Тег должен выглядеть примерно так: @Mavlo#7777, а так же подсвечиваться фиолетовым цветом.'
