from discord.ext import commands
from src.config import settings
from src.cog_helpers import send_gemini_images


class new_image_mid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="new_image_mid", aliases=["gnim"])
    async def new_image_mid(self, ctx, *, message):
        '''Génère une image avec le dernier modèle de Gemini. Ne garde pas d'historique'''
        await send_gemini_images(ctx, message, settings.new_images, image_size=settings.image_size_mid)


async def setup(bot):
    await bot.add_cog(new_image_mid(bot))
