from discord.ext import commands
from src.config import settings
from src.cog_helpers import stream_chat_command

class AskHigh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ask_high', aliases=["h"])
    async def ask_high(self, ctx, *, message):
        """Fonction de base qui permet d'envoyer un message à l'API d'openai GPT afin d'obtenir une réponse (chatGPT) ==> configuré pour beaucoup parler..."""
        await stream_chat_command(
            ctx,
            message,
            model=settings.model,
            instructions=settings.instructions,
            extra_payload={"text": {"verbosity": "high"}},
        )



async def setup(bot):
    await bot.add_cog(AskHigh(bot))
