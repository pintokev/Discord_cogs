import requests
import discord
from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings


class Get_Contexte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='get_contexte', aliases=["gc"])
    async def get_contexte(self, ctx):
        """Permet d'ajouter du texte au contexte de la conversation"""
        maybeThread = ctx.channel
        if maybeThread.type != discord.ChannelType.public_thread:
            await maybeThread.send("A lancer dans un threead")
            return
        metadata = {
            "id": str(maybeThread.id)
        }
        rep = requests.post(str(settings.get_instructions_url), json=metadata)
        # print("on command:", rep.text, maybeThread.id)
        await maybeThread.send(rep.text)

async def setup(bot):
    await bot.add_cog(Get_Contexte(bot))
