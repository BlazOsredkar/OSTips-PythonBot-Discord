import discord
import youtube_dl
import asyncio
import os

from discord.ext import commands

TOKEN = 'MTA0OTM4MzU1MjI4ODA0MzA3OA.GhY-tx.mtQoaDMRyodcSNms8qRaxoTJxf8bBSCL6HZChc'

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=')', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def play(ctx, *, search_query):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return
    else:
        channel = ctx.author.voice.channel

    voice_client = await channel.connect()
    source = await get_source(search_query)
    voice_client.play(source)

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

async def get_source(search_query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)['entries'][0]
        filename = ydl.prepare_filename(info_dict)
        ydl.download([info_dict['webpage_url']])
        source = discord.FFmpegPCMAudio(filename)
    os.remove(filename)
    return source

@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(f"Pong! Latency: {round(latency * 1000)}ms")

bot.run(TOKEN)
