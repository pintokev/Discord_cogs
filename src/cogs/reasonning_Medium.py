from discord.ext import commands
from src.config import settings
from src.cog_helpers import stream_chat_command

class reasonning_Medium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reasonning_medium', aliases=["om"])
    async def reasonning_medium(self, ctx, *, message):
        """Un des modèles de réflexion profond de GPT, il s'agit de la version medium (parmi [low, medium, high, xhigh])"""
        await stream_chat_command(
            ctx,
            message,
            model=settings.model_reasoning,
            instructions=settings.instructions,
            extra_payload={"reasoning": {"effort": "medium"}},
        )



async def setup(bot):
    await bot.add_cog(reasonning_Medium(bot))
