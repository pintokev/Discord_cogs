from bot.discordhandler import load_cogs
from config.settings import DISCORD_TOKEN
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
