import discord
from discord.ext import commands
import re

description="A discord bot to grab and post twitter links."

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description=description,
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_message(message: discord.Message):
     if message.author.id == bot.user.id:
        return
     if "twitter.com/" and "status" in message.content:
         channel = bot.get_channel(1123267527120797807)
         t_link = re.search(r"(https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(?:es)?\/(\d+)(?:\/.*)?)", f"{message.content}")      
         await channel.send(f"{t_link.group()} posted by {message.author.mention}")

bot.run('MTEyMzI1NzkxNzE0ODIzNzkxNQ.GbFM81.KKq71OFSPm6VIRjOkpkq1-FUJKWM2--pHsKH54')