from time import time

import requests
from discordhandler import createThread, stream_reponse_file, send_to_discord, send_msg, new_stream
from discord.ext import commands
from config import settings



class Jdr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = settings.stream
        self.time_msg = time()
        self.temp_cut = 1

    @commands.command(name='jdr', aliases=["jd"])
    async def jdr(self, ctx, *, message):
        """Permet de lancer une session de JDR avec chatGPT. Utilise un système de sauvegarde pour avoir des données correctes et réelles"""
        thread = await createThread(ctx, message)
        headers = {
            "Content-Type": "application/json",
            # "Authorization": settings.api_key
        }
        tools = [
            {
                "type": "mcp",
                "server_label": settings.SERVER_LABEL,
                "server_url": settings.ADRESSE_SERVEUR_MCP,
                "server_description": settings.SERVER_DESCRIPTION,
                "require_approval": "never"
            }
        ]

        data = {
            "content": str(message),
            "id": str(thread.id),
            "model": settings.model,
            "frequency_penalty": settings.frequency_penalty,
            "presence_penalty": settings.presence_penalty,
            "max_prompt_token": settings.max_prompt_token,
            "max_completion_token": settings.max_completion_token,
            "instructions": settings.system_jdr_msg,
            "tools":tools,
            "tool_ressource":"required",
            "reasoning":{"effort": "low"}
        }

        if ctx.message.attachments:
            url_file_list = []
            for attachment in ctx.message.attachments:
                url_file_list.append(attachment.url)
            data["image_url"] = url_file_list
        # print(data)
        async with thread.typing():
            response = requests.post(settings.stream, headers=headers, json=data, stream=True)
            await new_stream(ctx, thread, response)

async def setup(bot):
    await bot.add_cog(Jdr(bot))
