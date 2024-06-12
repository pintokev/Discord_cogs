import requests
from discord.ext import commands
from discordhandler import createThread
from config import settings


class Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='contexte', aliases=["c"])
    async def contexte(self, ctx, *, message):
        thread = await createThread(ctx, message)
        metadata = {
            "api_key": settings.api_key,
            "instructions": str(message),
            "id": str(thread.id)
        }
        rep = requests.post(str(settings.contexte), json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Contexte(bot))
