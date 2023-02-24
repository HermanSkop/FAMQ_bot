import discord
import activity_manager
import file_manager

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guilds:\n')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print('\n')


@client.event
async def on_presence_update(before, after):
    r = [i.name for i in after.roles]
    if before.activity != after.activity and '💚#3 Shadows Family💚' in r:
        if before.activity is not None and before.activity.name == 'Grand Theft Auto V':
            activity_manager.update_activity(before)
            print(before.name + ' leaves game')


@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    if message.channel.id in file_manager.get_channels():
        await message.channel.send(embed=activity_manager.create_embed_message(message))


client.run('MTA3NzI3NTE1MDA5NDk2Njg3NQ.G_AqQG.7kyLGrUy0fRMF-wXDwi3VWikbu0Sg8fglcoLk0')
