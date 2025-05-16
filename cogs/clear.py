import requests
from discordhandler import createThread
from discord.ext import commands
from config import settings
from get_token_google import get_token


class Cclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='cclear', aliases=["cc"])
    async def cclear(self, ctx):
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        headers = {
            'Authorization': f'Bearer {get_token(settings.instructions_url)}'
        }
        rep = requests.post(str(settings.clear), headers=headers, json=metadata)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Cclear(bot))
