from time import time

import requests
from discordhandler import createThread, stream_reponse_file, send_to_discord, send_msg, new_stream
from discord.ext import commands
from config import settings



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = settings.stream
        self.time_msg = time()
        self.temp_cut = 1

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
        headers = {
            "Content-Type": "application/json",
            # "Authorization": settings.api_key
        }
        data = {
            "content": str(self.format_help_map()),
            "id": "help_"+str(int(time())),
            "model": settings.model,
#            "temperature": settings.temperature,
#            "top_p": settings.top_p,
            "frequency_penalty": settings.frequency_penalty,
            "presence_penalty": settings.presence_penalty,
            "max_prompt_token": settings.max_prompt_token,
            "max_completion_token": settings.max_completion_token,
            "instructions": "Tu devras reformatter la liste de commande discord en indiquant la commande en gras et ce qu'elle fait"
        }

        if ctx.message.attachments:
            url_file_list = []
            for attachment in ctx.message.attachments:
                url_file_list.append(attachment.url)
            data["image_url"] = url_file_list
        # print(data)
        response = requests.post(settings.stream, headers=headers, json=data, stream=True)
        await new_stream("", ctx, response)



async def setup(bot):
    await bot.add_cog(Help(bot))
