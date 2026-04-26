from discord.ext import commands
from src.config import settings
from src.cog_helpers import send_gpt_images


class gptnewimage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gptnewimage", aliases=["ni"])
    async def gptnewimage(self, ctx, *, message):
        '''Genere une image avec GPT Image. Ne garde pas d'historique'''
        await send_gpt_images(ctx, message, settings.gpt_new_images, keep_history=False)


async def setup(bot):
    await bot.add_cog(gptnewimage(bot))
