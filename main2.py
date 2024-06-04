import os
import random
import requests
from datetime import datetime

import discord
from discord.ext import commands
from textblob import TextBlob

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from pass_generator import gen_pass
from modern_dict import m_dict
from NLP_Summary import summariztion
from model import get_class

# Initialize NLTK
nltk.download('punkt')
nltk.download('stopwords')

# to enable intents in discord 2.0
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

# on_ready event
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# on_message event
@bot.event
async def on_message(msg):
    username = msg.author.display_name 
    if msg.author == bot.user:
        return 
    elif msg.content.lower() in ["hello", "hi", "test"]:
        await msg.channel.send(f"Hi {username}! Type `$load` to start then type `$hello`")
    await bot.process_commands(msg)

# on_member_join event
@bot.event
async def on_member_join(member):
    guild = member.guild 
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f'Welcome to {guildname}!')
    await dmchannel.send('Type `$load` to start then type `$hello`')

# add and remove role
@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    member = payload.member
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    if emoji == "👨‍💻" and message_id == 1156402738717012038:  # adjust message ID as needed
        role = discord.utils.get(guild.roles, name="Developer")
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    user_id = payload.user_id
    emoji = payload.emoji.name
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)
    if emoji == "👨‍💻" and message_id == 1156402738717012038:  # adjust message ID as needed
        role = discord.utils.get(guild.roles, name="Developer")
        await member.remove_roles(role)

# Checks for root only
def is_me(ctx):
    return ctx.author.id == 689761236878884899

# prompt command
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hai! Saya adalah {bot.user} \U0001f642')
    await ctx.send(60 * '=')
    await ctx.send(f'1. Saya bisa membantumu untuk menghasilkan kata sandi dengan ketik `$pw`')
    await ctx.send(f'2. Saya bisa membantumu mencari arti kata dengan ketik `$dt <kata kapital>` contoh `$dt CRINGE`')
    await ctx.send(f'3. Saya bisa membantumu membuat emoji dengan ketik `$dt <kata>` contoh `$dt marah`')
    await ctx.send(f'4. Saya bisa membantumu memberikan gambar acak anjing dengan ketik `$dog`')
    await ctx.send(f'5. Saya bisa membantumu memberikan gambar acak bebek dengan ketik `$duck`')
    await ctx.send(f'6. Saya bisa membantumu memberikan meme acak hari ini dengan ketik `$meme`')
    await ctx.send(f'7. Saya bisa membantumu memberikan coinflip dengan ketik `$coinflip`')
    await ctx.send(f'8. Saya bisa membantumu memberikan random dice dengan ketik `$dice`')
    await ctx.send(f'9. Saya bisa membantumu memperbarui versi bot dengan ketik `$unload` lalu `$load`')
    await ctx.send(f'10. Saya bisa membantumu debug (memperbaiki) error dari bot dengan ketik `$reload`')
    await ctx.send(f'11. Saya bisa membantumu operasi matematika seperti $add 1 2')
    await ctx.send(f'12. Saya bisa membantumu membuat spam dengan contoh `$repeat 2 ayo bangun`')
    await ctx.send(f'13. Saya bisa membantumu menulis, baca, dan menambahkan ke file teks dengan `$tulis`, `$baca`, dan `$tambahkan`')
    await ctx.send(f'14. Saya bisa membantumu mencari keyword dari sebuah kalimat dengan `$analisis <kalimat>`')
    await ctx.send(f'15. Untuk bantuan/saran, ketik `$help`')
    await ctx.send(60 * '=')
    await ctx.send(f'daftar kata: CRINGE, BRB, LOL, GG, AFK, CREEPY (dev.)')
    await ctx.send(f'daftar kata penghasil emoji: marah, terbahak, keren, sedih, senyum, ok (dev.)')
    await ctx.send(f'Silakan pilih permintaanmu')

# main automations

# upload file to local computer
@bot.command()
async def simpan(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                await attachment.save(f"./files/{file_name}")
                await ctx.send(f"Gambar {file_name} berhasil disimpan!")
            else:
                await ctx.send(f"Maaf, {file_name} bukan file gambar yang didukung.")
    else:
        await ctx.send("Anda lupa mengunggah gambar :(")

# Computer Vision
@bot.command()
async def deteksi(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            await attachment.save(f"./CV/{file_name}")
            await ctx.send(get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=f"./CV/{file_name}"))
    else:
        await ctx.send("Anda lupa mengunggah gambar :(")

# help
@bot.command(aliases=["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title="Help", description="available contacts to help you", color=discord.Colour.dark_blue())
    MyEmbed.set_thumbnail(url="https://logodownload.org/wp-content/uploads/2017/11/discord-logo-1-1.png")
    MyEmbed.add_field(name="Contacts", value="vensiandoe@gmail.com or +6281298190169", inline=False)
    await ctx.send(embed=MyEmbed)

# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1, 2)
    if num == 1:
        await ctx.send('It is Head!')
    else:
        await ctx.send('It is Tail!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1, 6)
    await ctx.send(f'It is {nums}!')

# password generator
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

# random local meme image
@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('meme'))
    with open(f'meme/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

# API to get random dog and duck image
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command()
async def dog(ctx):
    image_url = get_dog_image_url
    await ctx.send(image_url)

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command()
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

# modern dictionary
@bot.command()
async def dt(ctx, arg):
    await ctx.send(f"{m_dict(arg)}")

# text analytics
@bot.command()
async def analisis(ctx, *, kalimat: str):
    await ctx.send(f"{summariztion(kalimat)}")

# adding two numbers
@bot.command()
async def add(ctx, left: float, right: float):
    """Adds two numbers together."""
    await ctx.send(left + right)

# subtraction
@bot.command()
async def min(ctx, left: float, right: float):
    """Subtraction."""
    await ctx.send(left - right)

# multiplying two numbers
@bot.command()
async def times(ctx, left: float, right: float):
    """Multiply two numbers together."""
    await ctx.send(left * right)

# division
@bot.command()
async def div(ctx, left: float, right: float):
    """division."""
    await ctx.send(left / right)

# exponentiation
@bot.command()
async def pow(ctx, left: float, right: float):
    """exponent."""
    await ctx.send(left ** right)

# spamming word
@bot.command()
async def repeat(ctx, times: int, *, content: str):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

# overwriting kalimat.txt
@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        text = my_string
        t.write(text)

# append kalimat.txt
@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        text = "\n" + my_string
        t.write(text)

# reading kalimat.txt
@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)

# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

# ---other tasks---

# moderation bot (visible for root only)
@bot.group()
@commands.has_role("Developer")  # checks
async def edit(ctx):
    pass

@edit.command()
async def createtextchannel(ctx, *, input):
    await ctx.guild.create_text_channel(name=input)

@edit.command()
async def createvoicechannel(ctx, *, input):
    await ctx.guild.create_voice_channel(name=input)

@bot.command()
@commands.check(is_me)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.guild.kick(member, reason=reason)

@bot.command()
@commands.check(is_me)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.guild.ban(member, reason=reason)

@bot.command()
@commands.check(is_me)
async def unban(ctx, *, input):
    name, discriminator = input.split("#")
    banned_members = await ctx.guild.bans()
    for bannedmember in banned_members:
        username = bannedmember.user.name
        disc = bannedmember.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(bannedmember.user)

# clear message (e.g. $purge 1 the last one message and $purge 20 9 from 20 september till now)
@bot.command()
@commands.check(is_me)
async def purge(ctx, amount, day: int = None, month: int = None, year: int = datetime.now().year):
    if amount == "/":
        if day is None or month is None:
            return
        else:
            await ctx.channel.purge(after=datetime(year, month, day))
            print(datetime(year, month, day))
    else:
        await ctx.channel.purge(limit=int(amount) + 1)

# bot moderation for voice channel
@bot.command()
@commands.check(is_me)
async def mute(ctx, user: discord.Member):
    await user.edit(mute=True)

@bot.command()
@commands.check(is_me)
async def unmute(ctx, user: discord.Member):
    await user.edit(mute=False)

@bot.command()
@commands.check(is_me)
async def deafen(ctx, user: discord.Member):
    await user.edit(deafen=True)

@bot.command()
@commands.check(is_me)
async def undeafen(ctx, user: discord.Member):
    await user.edit(deafen=False)

@bot.command()
@commands.check(is_me)
async def voicekick(ctx, user: discord.Member):
    await user.edit(voice_channel=None)

# footer
# Cogs (related to class) is still running even there are changing (updating)
@bot.command()
async def load(ctx):
    await bot.load_extension("Cogs")
    await ctx.send('loaded')

@bot.command()
async def unload(ctx):
    await bot.unload_extension("Cogs")
    await ctx.send('unloaded')

@bot.command()
async def reload(ctx):
    await bot.reload_extension("Cogs")
    await ctx.send('reloaded')

# error handling
@purge.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error; You have to type correctly such as `$purge 2` (number of last text) or `$purge 20 9` ($purge date month)")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error; You have to type correctly such as `$purge 2` (number of last text) or `$purge 20 9` ($purge date month)")

# Keyword command
@bot.command()
async def keyword(ctx, *, kalimat: str):
    stop_words = set(stopwords.words('indonesian'))  # Adjust language as needed
    word_tokens = word_tokenize(kalimat)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    await ctx.send(f"Kata kunci: {', '.join(filtered_sentence)}")

# Analisis command
@bot.command()
async def analisis_text(ctx, *, kalimat: str):
    stop_words = set(stopwords.words('indonesian'))  # Adjust language as needed
    word_tokens = word_tokenize(kalimat)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    await ctx.send(f"Kata kunci: {', '.join(filtered_sentence)}")
    
# Sentiment analysis of sentence
@bot.command()
async def sentimen(ctx, *, kalimat: str):
    analysis = TextBlob(kalimat)
    sentiment = analysis.sentiment
    if sentiment.polarity > 0:
        sentiment_label = "Positif"
    elif sentiment.polarity == 0:
        sentiment_label = "Netral"
    else:
        sentiment_label = "Negatif"
    await ctx.send(f"Sentimen: {sentiment_label}")

# bot token
bot.run("")
