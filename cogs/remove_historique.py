import requests
from discord.ext import commands
from discordhandler import createThread
from config import settings
from get_token_google import get_token


class Remove_Historique(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='remove_historique', aliases=["rh"])
    async def remove_historique(self, ctx):
        thread = await createThread(ctx, "Thread créé")
        metadata = {
            "id": str(thread.id)
        }
        headers = {
            'Authorization': f'Bearer {get_token(settings.instructions_url)}'
        }
        rep = requests.post(str(settings.remove_historique), json=metadata, headers=headers)
        await thread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Remove_Historique(bot))
