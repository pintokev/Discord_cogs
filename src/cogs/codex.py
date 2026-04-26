from discord.ext import commands
from src.config import settings
from src.cog_helpers import stream_chat_command

class Codex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='codex', aliases=["d"])
    async def codex(self, ctx, *, message):
        """Permet d'interroger le modèle codex d'openai, adapté au code et disposant d'une longue fenêtre de contexte (il se souvient de plus de choses)"""
        await stream_chat_command(ctx, message, model=settings.model_codex, instructions=settings.instructions)



async def setup(bot):
    await bot.add_cog(Codex(bot))
