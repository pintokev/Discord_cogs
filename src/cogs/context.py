from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings
from src.cog_helpers import send_backend_text


class Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='contexte', aliases=["c"])
    async def contexte(self, ctx, *, message):
        """Modifie le contexte de la session en cours (ça écrase le contexte actuel)"""
        thread = await createThread(ctx, message)
        metadata = {
            "instruction": str(message),
            "id": str(thread.id)
        }
        await send_backend_text(thread, str(settings.instructions_url), metadata)

async def setup(bot):
    await bot.add_cog(Contexte(bot))
