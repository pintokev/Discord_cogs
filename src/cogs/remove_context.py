import requests
from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings


class Remove_Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='remove_contexte', aliases=["rc"])
    async def remove_contexte(self, ctx):
        """Supprime le contexte de la session sans en rajouter par dessus"""
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        rep = requests.post(str(settings.instructions_url)+"?remove", json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Remove_Contexte(bot))
