from src.discordhandler import createThread
from discord.ext import commands
from src.config import settings
from src.cog_helpers import send_backend_text


class Cclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='cclear', aliases=["cc"])
    async def cclear(self, ctx):
        """Supprime l'intégralité de la session, le contexte, l'historique, les images. Le thread est gardé côté discord"""
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        await send_backend_text(thread, str(settings.clear), metadata)

async def setup(bot):
    await bot.add_cog(Cclear(bot))
