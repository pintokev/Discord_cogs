import requests
from discord.ext import commands
from discordhandler import createThread
from config import settings


class Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='contexte', aliases=["c"])
    async def contexte(self, ctx, *, message):
        """Modifie le contexte de la session en cours (ça écrase le contexte actuel)"""
        thread = await createThread(ctx, message)
        metadata = {
            "instruction": str(message),
            "id": str(thread.id)
        }
        rep = requests.post(str(settings.instructions_url), json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Contexte(bot))
