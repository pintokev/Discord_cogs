from discord.ext import commands
from src.config import settings
from src.cog_helpers import stream_chat_command

class Reasonning_High(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reasonning_high', aliases=["oh"])
    async def reasonning_high(self, ctx, *, message):
        """Un des modèles de réflexion profond de GPT, il s'agit de la version high (parmi [low, medium, high, xhigh])"""
        await stream_chat_command(
            ctx,
            message,
            model=settings.model_reasoning,
            instructions=settings.instructions,
            extra_payload={"reasoning": {"effort": "high"}},
        )



async def setup(bot):
    await bot.add_cog(Reasonning_High(bot))
