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


bot.run("MTA0OTM4MzU1MjI4ODA0MzA3OA.G1kVvz.4kUWkW4neQ9AoUVGx7lZo5cV89JeDlA-IeZ2XI")
    