from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings
from src.cog_helpers import send_backend_text


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
        await send_backend_text(thread, str(settings.instructions_url), metadata, params={"remove": ""})

async def setup(bot):
    await bot.add_cog(Remove_Contexte(bot))
