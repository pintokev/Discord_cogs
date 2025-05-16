import requests
from discord.ext import commands
from discordhandler import createThread
from config import settings
from get_token_google import get_token


class Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='contexte', aliases=["c"])
    async def contexte(self, ctx, *, message):
        thread = await createThread(ctx, message)
        metadata = {
            "instruction": str(message),
            "id": str(thread.id)
        }
        headers = {
            'Authorization': f'Bearer {get_token(settings.instructions_url)}'
        }
        rep = requests.post(str(settings.instructions_url), json=metadata, headers=headers)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Contexte(bot))
