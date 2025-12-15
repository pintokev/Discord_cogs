import requests
from discord.ext import commands
from discordhandler import createThread
from config import settings


class Remove_Historique(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='remove_historique', aliases=["rh"])
    async def remove_historique(self, ctx):
        """Supprime seulement l'historique de conversation côté GPT tout en gardant le contexte"""
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        rep = requests.post(str(settings.remove_historique), json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Remove_Historique(bot))
