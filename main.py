import disnake
from disnake.ext import commands
import activity_manager
import file_manager

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())


# 694078814585880598


@bot.slash_command(name='stats', description='Узнай свою статистику')
async def print_stats(ctx: disnake.ApplicationCommandInteraction):
    await ctx.send(embed=activity_manager.create_stats_message(ctx.author))


@bot.slash_command(name='help', description='Команды и условия использования')
async def print_help(ctx):
    await ctx.send(embed=activity_manager.create_help_message())


@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:\n')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print('\n')


@bot.event
async def on_presence_update(before, after):
    roles = [i.name for i in after.roles]
    if before.activity != after.activity and activity_manager.match_roles(roles):
        print(after.name + ' enters ' + after.activity.name)
        if before.activity is not None and before.activity.name in file_manager.get_games():
            activity_manager.update_activity(before)
            print(before.name + ' leaves ' + before.activity.name)


bot.run(token='MTA3NzI3NTE1MDA5NDk2Njg3NQ.G_AqQG.7kyLGrUy0fRMF-wXDwi3VWikbu0Sg8fglcoLk0')
