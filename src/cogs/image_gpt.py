from io import BytesIO

from discord.ext import commands

from src.config import settings
from src.cog_helpers import send_gpt_images


class GPTImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gptimage", aliases=["i", "gpti"])
    async def gptimage(self, ctx, *, message):
        """Genere une image avec le modele OpenAI GPT Image via le backend Docker."""
        await send_gpt_images(ctx, message, settings.gpt_images, keep_history=True)


async def setup(bot):
    await bot.add_cog(GPTImage(bot))
