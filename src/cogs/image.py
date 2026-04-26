from discord.ext import commands
from src.config import settings
from src.cog_helpers import send_gemini_images


class image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="image", aliases=["gi"])
    async def image(self, ctx, *, message):
        '''Génère une image avec le dernier modèle de Gemini. Garde la dernière image généré en historique'''
        await send_gemini_images(ctx, message, settings.images, image_size=settings.image_size)


async def setup(bot):
    await bot.add_cog(image(bot))
