from time import time

from discord.ext import commands
from src.config import settings
from src.cog_helpers import stream_chat_command

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_help_map(self, prefix="!"):
        parts = []
        for cmd in self.bot.walk_commands():
            if cmd.hidden:
                continue

            help_txt = (cmd.help or cmd.brief or "").strip().replace("\n", " ")

            # 1er alias si dispo, sinon le nom de la commande
            name = (cmd.aliases[0] if getattr(cmd, "aliases", None) else cmd.name)

            parts.append(f"{{{prefix}{name}:{help_txt}}}")

        return "\n".join(parts)

    @commands.command(name='help')
    async def help(self, ctx):
        """Ressort toute la liste de commande disponible"""
        await stream_chat_command(
            ctx,
            self.format_help_map(),
            model=settings.model,
            instructions="Tu devras reformater la liste de commandes Discord en indiquant la commande en gras et ce qu'elle fait, les ranger par categorie tout en les triant. Formatte la reponse en style documentation Discord, chaque categorie devra etre entre ``` ```.",
            target=ctx,
            conversation_id=f"help_{int(time())}",
        )



async def setup(bot):
    await bot.add_cog(Help(bot))
