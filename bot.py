import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded cogs.{file[:-3]}")

async def main():
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())