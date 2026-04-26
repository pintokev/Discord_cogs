from discord.ext import commands

from src.config import settings
from src.discordhandler import createThread
from src.backend_client import post_backend_form, read_attachments


class Asf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='asf', aliases=["sf"])
    async def asf(self, ctx):
        """Envoie des fichiers à openai pour << étendre >> sa base de connaissance"""
        thread = await createThread(ctx, "Voici les fichiers")
        if not ctx.message.attachments:
            await thread.send("Aucun fichier associé en pièces jointes")
            return

        files = await read_attachments(ctx.message.attachments, field_name="file")
        async with thread.typing():
            status, text, _ = await post_backend_form(
                settings.file_search,
                json_payload={"id": str(thread.id), "model": settings.model},
                files=files,
            )

        if status >= 400:
            await thread.send(f"Erreur backend ({status}) : {text[:1500]}")
        else:
            await thread.send(text[:1900] if text else "Réponse vide.")


async def setup(bot):
    await bot.add_cog(Asf(bot))
