from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings
from src.cog_helpers import send_backend_text


class Add_Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='add_contexte', aliases=["ac"])
    async def add_contexte(self, ctx, *, message):
        """Permet d'ajouter du texte au contexte de la conversation"""
        thread = await createThread(ctx, message)
        metadata = {
            "instruction": str(message),
            "id": str(thread.id)
        }
        await send_backend_text(thread, str(settings.instructions_url), metadata, params={"add": ""})

async def setup(bot):
    await bot.add_cog(Add_Contexte(bot))
