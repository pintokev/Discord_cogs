from json import dumps

import aiohttp
import discord
from discord.ext import commands
import requests
import os

from bot.discordhandler import createThread, stream_reponse_file
from config import settings


class Asf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def asf(self, ctx):
        thread = await createThread(ctx, "Voici les fichiers")
        metadata = {
            "api_key": settings.api_key,
            "id": str(thread.id),
            "content": "Voici les fichiers. Retourne moi seulement une phrase m'indiquant que les fichiers ont été sauvegardé et stocker dans un vector openai",
            "for_file_search": True
        }
        if ctx.message.attachments: await stream_reponse_file(ctx, metadata)


async def setup(bot):
    await bot.add_cog(Asf(bot))
