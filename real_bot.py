import discord
from discord.ext    import commands
from discord.ext.commands   import Bot
import asyncio

# ön ek
bot = commands.Bot(command_prefix = 'sau')
SORU_DOGRULUK_ORANI=93 # %93 Oraninda 1 ssecenegin on plana cikmasi gerekiyor
VERILEN_OY_SINIRI=30   # En az 30 oy kullanilmasi gerekiyor
class Soru():
    def __init__(self):
        self.soru = [[1000000000000,1,1,1,1,1]]
    def soru_sifirla(self):
        self.soru=[[1000000000000,1,1,1,1,1]]
    def soru_guncelle(self,message_id,number,count):
        for n,simdiki_soru in enumerate(self.soru, start=1):
            if len(self.soru) < simdiki_soru[0] and message_id == simdiki_soru[0]:
                simdiki_soru[number] = count

    def soru_secenekleri_say(self, message):
        for react in message.reactions:
            for secenek in enumerate(list("🇦🇧🇨🇩🇪"), start =1):
                print(secenek)
                if react.emoji == secenek[1]:
                    print("A secenek:"+str(react.count))
                    self.soru_guncelle(message.id,secenek[0],react.count)
                if react.emoji == secenek[1]:
                    print("B secenek:"+str(react.count))
                    self.soru_guncelle(message.id,secenek[0],react.count)
                if react.emoji == secenek[1]:
                    print("C secenek:"+str(react.count))
                    self.soru_guncelle(message.id,secenek[0],react.count)
                if react.emoji == secenek[1]:
                    print("D secenek:"+str(react.count))
                    self.soru_guncelle(message.id,secenek[0],react.count)
                if react.emoji == secenek[1]:
                    print("E secenek:"+str(react.count))
                    self.soru_guncelle(message.id,secenek[0],react.count)

    def soru_analiz(self,message_id):
        total_reaction_counts = 0
        new_rate = 0
        max_percent_reaction = 0,0,0 # number_of_selection, count_of_selection, percent_of_selection
        for soru_x in self.soru:
            if message_id in soru_x:
                for answers in soru_x[1:]: # toplam reaksiyon sayisi
                    total_reaction_counts += answers
                for answers in enumerate(soru_x[1:], start=1):
                    new_rate = (answers[1]/total_reaction_counts)*100
                    if max_percent_reaction[2] < new_rate:
                        max_percent_reaction = answers[0],answers[1],new_rate
        if total_reaction_counts > 2:
            print(max_percent_reaction[2])
            if max_percent_reaction[2] > ((total_reaction_counts*10)/100): # %80 den fazlasi dogru sikki ayni dusunuyorsa
                print("Maksimum Secenek Yuzdesi:")
                print(max_percent_reaction)
                return max_percent_reaction
    def soru_ekle(self,message_id,count_a,count_b,count_c,count_d,count_e):    
        self.soru.append([message_id, count_a, count_b, count_c, count_d, count_e])

soru = Soru() # Soru sayimi icin nesne turetildi

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
        soru.soru_ekle(message_id,1,1,1,1,1)

# toplu mesaj silme
    if message.content.startswith('sausil'):
        soru.soru_sifirla()
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
    channel_id = payload.channel_id
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    soru.soru_secenekleri_say(message)
    durum=soru.soru_analiz(message_id)
    if durum is not None and durum[2] > VERILEN_OY_SINIRI and durum[1] > SORU_DOGRULUK_ORANI:
         await message.add_reaction("✅")
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
    channel_id = payload.channel_id
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    soru.soru_secenekleri_say(message)
    durum=soru.soru_analiz(message_id)
    if durum is not None and durum[2] > VERILEN_OY_SINIRI and durum[1] > SORU_DOGRULUK_ORANI:
         await message.add_reaction("✅")
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