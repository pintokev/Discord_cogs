import discord
from discord.ext import commands
from src.config import settings
from src.cog_helpers import send_backend_text


class Get_Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='get_contexte', aliases=["gc"])
    async def get_contexte(self, ctx):
        """Permet de retoutner le contexte du thread en cours"""
        maybeThread = ctx.channel
        if maybeThread.type != discord.ChannelType.public_thread:
            await maybeThread.send("A lancer dans un threead")
            return
        metadata = {
            "id": str(maybeThread.id)
        }
        await send_backend_text(maybeThread, str(settings.get_instructions_url), metadata)

async def setup(bot):
    await bot.add_cog(Get_Contexte(bot))
