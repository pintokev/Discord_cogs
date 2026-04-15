from discord.ext import commands

import src.config.settings
from src.discordhandler import createThread, send_msg
from src.config import settings
import requests
import subprocess
import os


class Aci(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='aci', aliases=["ci"])
    async def asf(self, ctx):
        """Envoie des fichier à openai pour que gpt puisse recréer un envirpnnement virtuel sous python, coder et tester le code en utilisant les fichiers en pièces jointes"""
        thread = await createThread(ctx, "Voici les fichiers")
        command = [
            "curl",
            "-X", "POST", settings.code_interpreter,
            "-F", f"data={{\"id\":\"{str(thread.id)}\", \"model\":\"{settings.model}\"}}",
        ]
        filename = []
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                response = requests.get(attachment.url)
                file_name = attachment.filename
                with open(file_name, 'wb') as f:
                    f.write(response.content)

                command.append("-F")
                command.append("file=@" + file_name)
                filename.append(file_name)

            async with thread.typing():
                result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
                for file in filename:
                    os.remove(file)
                await send_msg(thread, result.stdout)
            # print(result.stdout)
        else: return "Aucun fichier associé en pièces jointes\n"


async def setup(bot):
    await bot.add_cog(Aci(bot))
