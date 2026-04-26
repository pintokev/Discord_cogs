from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings
from src.cog_helpers import send_backend_text


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
        await send_backend_text(thread, str(settings.remove_historique), metadata)

async def setup(bot):
    await bot.add_cog(Remove_Historique(bot))
