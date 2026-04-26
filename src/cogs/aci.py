from discord.ext import commands

from src.config import settings
from src.cog_helpers import send_backend_text
from src.discordhandler import createThread
from src.backend_client import post_backend_form, read_attachments


class Aci(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='aci', aliases=["ci"])
    async def asf(self, ctx):
        """Envoie des fichier à openai pour que gpt puisse recréer un envirpnnement virtuel sous python, coder et tester le code en utilisant les fichiers en pièces jointes"""
        thread = await createThread(ctx, "Voici les fichiers")
        if not ctx.message.attachments:
            await thread.send("Aucun fichier associé en pièces jointes")
            return

        files = await read_attachments(ctx.message.attachments, field_name="file")
        async with thread.typing():
            status, text, _ = await post_backend_form(
                settings.code_interpreter,
                json_payload={"id": str(thread.id), "model": settings.model},
                files=files,
            )

        if status >= 400:
            await thread.send(f"Erreur backend ({status}) : {text[:1500]}")
        else:
            await thread.send(text[:1900] if text else "Réponse vide.")


async def setup(bot):
    await bot.add_cog(Aci(bot))
