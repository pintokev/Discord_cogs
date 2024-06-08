from time import time

import requests
from discord.ext import commands
from bot.discordhandler import createThread
from config import settings


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='clear', aliases=["clear"])
    async def clear(self, ctx):
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "api_key": settings.api_key,
            "id": str(thread.id)
        }
        rep = requests.post(str(settings.clear), json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Clear(bot))
