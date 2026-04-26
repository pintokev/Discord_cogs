from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings
from src.cog_helpers import send_backend_text


class Remove_Last_Echange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='remove_last_echange', aliases=["rl"])
    async def remove_last_echange(self, ctx):
        """Supprime le dernier échange de la discussion (une demande utilisateur + réponse GPT). Cette commande peut être spammé pour supprimer plusieurs échanges"""
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        await send_backend_text(thread, str(settings.remove_historique), metadata, params={"remove_last": ""})

async def setup(bot):
    await bot.add_cog(Remove_Last_Echange(bot))
