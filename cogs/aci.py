from discord.ext import commands
from bot.discordhandler import createThread, stream_reponse_file
from config import settings


class Aci(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def aci(self, ctx):
        thread = await createThread(ctx, "Voici les fichiers")
        metadata = {
            "api_key": settings.api_key,
            "id": str(thread.id),
            "content": "Voici les fichiers. Retourne moi seulement une phrase m'indiquant que les fichiers ont été sauvegarder, donne moi les file_id de chacun des fichiers présent et rien d'autre",
            "for_code_interpreter": True
        }
        if ctx.message.attachments: await stream_reponse_file(ctx, thread, metadata)


async def setup(bot):
    await bot.add_cog(Aci(bot))
