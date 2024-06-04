from json import dumps

import aiohttp
import discord
from discord.ext import commands
import requests
import os

from bot.discordhandler import createThread
from config import settings


class Aci(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def aci(self, ctx):
        thread = await createThread(ctx, "Voici les fichiers")
        if ctx.message.attachments:
            async with aiohttp.ClientSession() as session:
                for attachment in ctx.message.attachments:
                    temp_filename = attachment.filename
                    metadata = {
                        "api_key": settings.api_key,
                        "id": str(thread.id),
                        "content": "Repond moi seulement . sans rien d'autre",
                        "for_code_interpreter": True
                    }
                    form_data = aiohttp.FormData()
                    form_data.add_field('metadata', dumps(metadata), content_type="multipart/form-data")
                    file_data = await attachment.read()
                    form_data.add_field('file', file_data, filename=attachment.filename)
                    async with session.post(settings.url, data=form_data) as response:
                        await ctx.send(f"Fichier envoyé avec succès : {response.status}")


async def setup(bot):
    await bot.add_cog(Aci(bot))
