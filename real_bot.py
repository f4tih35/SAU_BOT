import discord
from discord.ext    import commands
from discord.ext.commands   import Bot
import asyncio

# ön ek
bot = commands.Bot(command_prefix = 'sau')

@bot.event
async def on_ready():
    print('bot is ready')

# log
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(717402901017788417)
    users = bot.users 
    guild = member.guild
    lst = len(list(guild.members))

    await channel.send(f'{member.mention} sunucuya katıldı 🤙 Üye sayısı: {lst}')

# log
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(717402901017788417)
    users = bot.users 
    guild = member.guild
    lst = len(list(guild.members))

    await channel.send(f'{member.mention} sunucudan ayrıldı 👋 Üye sayısı: {lst+2}')
    


#sorular
@bot.event
async def on_message(message):
    if message.channel.id == 716895157194194984 or message.channel.id == 717708011602313276 or message.channel.id == 717746193186422825:
        await message.add_reaction("🇦")
        await message.add_reaction("🇧")
        await message.add_reaction("🇨")
        await message.add_reaction("🇩")
        await message.add_reaction("🇪")


# toplu mesaj silme
    if message.content.startswith('sausil'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit = count)
                    await message.channel.send('{} mesaj silindi'.format(len(deleted)-1))



# dogrulama
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 717786402728837120:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'sau':
            print('sau role ok')
            role = discord.utils.get(guild.roles, name='Member')

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('done')



# dogrulama
@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 717786402728837120:
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

bot.run('TOKEN')