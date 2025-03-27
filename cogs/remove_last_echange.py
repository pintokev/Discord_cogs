import requests
from discord.ext import commands
from discordhandler import createThread
from config import settings


class Remove_Last_Echange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='remove_last_echange', aliases=["rl"])
    async def remove_last_echange(self, ctx):
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        rep = requests.post(str(settings.remove_historique)+"?remove_last", json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Remove_Last_Echange(bot))
