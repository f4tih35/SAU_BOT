import discord
from discord.ext    import commands
from discord.ext.commands   import Bot
import asyncio

bot = commands.Bot(command_prefix = 'sau')

@bot.event
async def on_ready():
    print('bot is ready')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    users = bot.users 
    guild = member.guild
    lst = len(list(guild.members))

    await channel.send(f'{member.mention} sunucuya katıldı 🤙 Üye sayısı: {lst}')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    users = bot.users 
    guild = member.guild
    lst = len(list(guild.members))

    await channel.send(f'{member.mention} sunucudan ayrıldı 👋 Üye sayısı: {lst+2}')
    


@bot.event
async def on_message(message):
    if message.channel.id == YOUR_CHANNEL_ID:
        await message.add_reaction("🇦")
        await message.add_reaction("🇧")
        await message.add_reaction("🇨")
        await message.add_reaction("🇩")
        await message.add_reaction("🇪")

    if message.content.startswith('sausil'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit = count)
                    await message.channel.send('{} mesaj silindi'.format(len(deleted)-1))


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == YOUR_MESSAGE_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'sau':
            print('sau role ok')
            role = discord.utils.get(guild.roles, name='Member')

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('add done')

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == YOUR_MESSAGE_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'sau':
            print('sau role deleted')
            role = discord.utils.get(guild.roles, name='Member')

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('delete done')

bot.run('YOUR_TOKEN')