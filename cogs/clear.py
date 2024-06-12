import requests
from discordhandler import createThread
from discord.ext import commands
from config import settings


class Cclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='cclear', aliases=["dcc"])
    async def cclear(self, ctx):
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "api_key": settings.api_key,
            "id": str(thread.id)
        }
        rep = requests.post(str(settings.clear), json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Cclear(bot))
