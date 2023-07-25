import discord
from discord.ext import commands, tasks
import praw
from prawcore.exceptions import NotFound
import re
import asyncio
import tokens

#discord bot setup & intents
description="A discord bot to grab and post twitter links."
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
dupe_protection = []
subreddit_name='nba'

reddit = praw.Reddit("bot1")

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description=description,
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"Logged into Discord as {bot.user} (ID: {bot.user.id})")
    print("------")

#Reddit bot setup

def setSubreddit(name):
    global subreddit_name
    subreddit_name = name
def subredditExists(sub):
    try:
        reddit.redditor(sub).id
    except NotFound:
        try:
            reddit.redditor(sub[2:]).id
        except NotFound:
            return False
    return True

async def getRedList():
    subreddit = reddit.subreddit(subreddit_name)
    hot = subreddit.hot(limit=25)
    return hot

#Check hot section and post the twitter links to discord every 10 secs
@bot.slash_command(name="refresh")
async def postTwit(ctx: discord.ApplicationContext):
    await ctx.respond("Refreshing...")
    await bot.wait_until_ready()
    ann_chan = bot.get_channel(1123267527120797807)
    posts = await getRedList()
    new_post_count=0

    for item in posts:
        if re.search(r"(https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(?:es)?\/(\d+)(?:\/.*)?)", item.url) and item not in dupe_protection and new_post_count<10:
            await ann_chan.send(f"{item.url} posted by u/{item.author}")
            dupe_protection.append(item)
            new_post_count+=1
    if new_post_count != 0:
        await ctx.send(f"Found {new_post_count} new posts.")
    else:
        await ctx.send(f"Did not find any new posts.")
#clean duplicate post cache
@bot.slash_command(name="clean")
async def clean(ctx: discord.ApplicationContext):
    await bot.wait_until_ready()
    dupe_protection.clear()
    await ctx.respond("Cache Cleaned!")

@bot.slash_command(name="changesub")
async def changeSub(ctx: discord.ApplicationContext, input):
    await bot.wait_until_ready()
    print(reddit.subreddit(input))
    if input.startswith("r/") and subredditExists(input[2:]):
        setSubreddit(input[2:])
        await ctx.respond(f"Changed Subreddit to {input}")
    elif subredditExists(input):
        setSubreddit(input)
        await ctx.respond(f"Changed Subreddit to r/{input}")
    else:
        await ctx.respond("Please enter a correct subreddit name.")
bot.run(tokens.token1)