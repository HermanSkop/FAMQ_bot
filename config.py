import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

files_path = 'files/'
activity_file_path = files_path + 'activity.json'
out_file_path = files_path + 'out.txt'
config_file_path = files_path + 'config.json'
