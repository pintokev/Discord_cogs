from discord.ext import commands
from src.config import settings
from src.cog_helpers import stream_chat_command

class Cyber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cyber', aliases=["cy"])
    async def cyber(self, ctx, *, message):
        """Fonction de base qui permet d'envoyer un message à l'API d'openai GPT afin d'obtenir une réponse (chatGPT)"""
        await stream_chat_command(ctx, message, model=settings.model_cyber, instructions=settings.instructions)



async def setup(bot):
    await bot.add_cog(Cyber(bot))
