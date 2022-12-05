#basic discord bot
import discord
from discord.ext import commands
import asyncio
import random
import os
import sys
import time
import datetime
import greetings
from dotenv import load_dotenv
import youtube_dl
import ffmpeg
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from requests import get
#read from env file


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='.',intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready")
    

@bot.command(pass_context=True)
async def ping(ctx):
    #send a pong and mention user
    await ctx.send(f"Pong! **{round(bot.latency * 1000)}ms**")

@bot.command(pass_context=True)
async def hello(ctx):
    #send a random greeting
    await ctx.send("HAI")

@bot.command(pass_context=True)
async def roll(ctx):
    #send a random roll
    await ctx.send("Roll: " + str(random.randint(1,6)))

@bot.command(pass_context=True)
async def clear(ctx, amount=5):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)
        await ctx.send("https://giphy.com/gifs/power-starz-season6-final-episodes-RihiXYvJCRMMHWRI8l")
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)
    else:
        await ctx.send("https://tenor.com/view/i-dont-give-you-permission-to-do-this-no-permission-dont-do-it-angry-sales-person-gif-13505225")

@bot.command(pass_context=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        await member.kick(reason=reason)
    else:
        await ctx.send("You do not have permission to use this command")

@bot.command(pass_context=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        await member.ban(reason=reason)
    else:
        await ctx.send("You do not have permission to use this command")

@bot.command(pass_context=True)
async def unban(ctx, *, member):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return
    else:
        await ctx.send("You do not have permission to use this command")

@bot.command(pass_context=True)
async def mute(ctx, member : discord.Member):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        role = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.add_roles(role)
    else:
        await ctx.send("You do not have permission to use this command")

@bot.command(pass_context=True)
async def unmute(ctx, member : discord.Member):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        role = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(role)
    else:
        await ctx.send("You do not have permission to use this command")

@bot.command(pass_context=True)
async def warn(ctx, member : discord.Member, *, reason=None):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send(f"Warned {member.mention} for {reason}")
    else:
        await ctx.send("You do not have permission to use this command")

@bot.command(pass_context=True)
async def info(ctx):
    #send info about bot
    embed = discord.Embed(title="Info", description="Info about the bot", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="OSTips")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def helpi(ctx):
    #send help message
    embed = discord.Embed(title="Help", description="List of commands", color=0xeee657)

    embed.add_field(name=".ping", value="Returns Pong!", inline=False)
    embed.add_field(name=".hello", value="Returns a random greeting", inline=False)
    embed.add_field(name=".roll", value="Returns a random roll", inline=False)
    embed.add_field(name=".clear", value="Clears the chat", inline=False)
    embed.add_field(name=".kick", value="Kicks a member", inline=False)
    embed.add_field(name=".ban", value="Bans a member", inline=False)
    embed.add_field(name=".unban", value="Unbans a member", inline=False)
    embed.add_field(name=".mute", value="Mutes a member", inline=False)
    embed.add_field(name=".unmute", value="Unmutes a member", inline=False)
    embed.add_field(name=".warn", value="Warns a member", inline=False)
    embed.add_field(name=".info", value="Returns info about the bot", inline=False)
    embed.add_field(name=".help", value="Returns this message", inline=False)

    await ctx.send(embed=embed)

#Random number guesser with 5 tries and if not number throw message
@bot.command(pass_context=True)
async def guess(ctx):
    await ctx.send("Guess a number between 1 and 10")

    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    answer = random.randint(1, 10)
    for i in range(5):
        try:
            guess = await bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send('Sorry, you took too long it was {}.'.format(answer))

        if int(guess.content) == answer:
            return await ctx.send('You are right!')
        else:
            await ctx.send('{} is not right.'.format(guess.content))

    await ctx.send('Sorry, you are out of guesses. It was {}.'.format(answer))

#Restart bot with a command
@bot.command(pass_context=True)
async def restart(ctx):
    #check if user is OSTips
    if ctx.message.author.id == 479700399167897601:
        await ctx.send("Restarting bot...")
        python = sys.executable
        os.execl(python, python, * sys.argv)
    else:
        await ctx.send("You do not have permission to use this command")

#send a message to the user DM
@bot.command(pass_context=True)
async def dm(ctx, member : discord.Member, *, message=None):
    #send the message with author 
    await member.send(f"{ctx.message.author.name} sent you a message: {message}")
    await ctx.send("Message sent!")
    await ctx.message.delete()

#create role on .createrole with basic permissions
@bot.command(pass_context=True)
async def createrole(ctx, *, role):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        await ctx.guild.create_role(name=role, permissions=discord.Permissions(permissions=8))
        await ctx.send(f"Created role {role}")
    else:
        await ctx.send("You do not have permission to use this command")


#play sound
@bot.command(pass_context=True)
async def play(ctx, url):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        #check if bot is in a voice channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=url))
    else:
        await ctx.send("You do not have permission to use this command")


#play a sound when administrator uses .playthis and use message as filename
@bot.command(pass_context=True)
async def playthis(ctx, message):
    #check if user is admin
    if ctx.message.author.guild_permissions.administrator:
        #check if bot is in a voice channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()
        if(message == 'test'):
            ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="audio/test.mp3"))
        
    else:
        await ctx.send("You do not have permission to use this command")





load_dotenv()
token = os.getenv("SECRET_KEY")
bot.run(token)
    