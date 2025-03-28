from discord.ext import commands
from discordhandler import createThread, stream_reponse_file
from config import settings
import requests
import subprocess
import os


class Asf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def asf(self, ctx):
        thread = await createThread(ctx, "Voici les fichiers")

        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                response = requests.get(attachment.url)
                file_name = attachment.filename
                with open(file_name, 'wb') as f:
                    f.write(response.content)

                command = [
                    "curl",
                    "-X", "POST", settings.file_search,
                    "-H", f"Authorization: {settings.api_key}",
                    "-F", f"data={{\"id\":\"{str(thread.id)}\"}}",
                    "-F", "file=@"+file_name
                ]

                result = subprocess.run(command, capture_output=True, text=True)

                print(result.stdout)
                os.remove(file_name)
        else: return "Aucun fichier associé en pièces jointes\n"


async def setup(bot):
    await bot.add_cog(Asf(bot))
