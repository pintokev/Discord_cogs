import requests
from discord.ext import commands
from discordhandler import createThread
from config import settings
from get_token_google import get_token


class Remove_Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='remove_contexte', aliases=["rc"])
    async def remove_contexte(self, ctx):
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        headers = {
            'Authorization': f'Bearer {get_token(settings.instructions_url)}'
        }
        rep = requests.post(str(settings.instructions_url)+"?remove", json=metadata, headers=headers)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Remove_Contexte(bot))
