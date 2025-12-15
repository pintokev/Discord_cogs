from time import time

import requests
from discordhandler import createThread, stream_reponse_file, send_to_discord, send_msg, new_stream
from discord.ext import commands
from config import settings



class Jdr(commands.Cog):
    def init(self, bot):
        self.bot = bot
        self.url = settings.stream
        self.time_msg = time()
        self.temp_cut = 1
    @commands.command(name='jdr', aliases=["jd"])
    async def jdr(self, ctx, *, message):
        thread, flag = await createThread(ctx, message, jdr=True)
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
        if flag :
            data = {
                "content": str("Appelle la fonctio get_system_msg du MCP server. Ne mets aucun texte avant ni après, envoi le retour de la fonction brut seulement"),
                "id": str(thread.id),
                "model": settings.model,
                "frequency_penalty": settings.frequency_penalty,
                "presence_penalty": settings.presence_penalty,
                "max_prompt_token": settings.max_prompt_token,
                "max_completion_token": settings.max_completion_token,
                "tools": tools,
                "tool_choices": "required"
            }
            response = requests.post(settings.stream, headers=headers, json=data)
            with open("system_msg.txt", "w") as file:
                file.write(str(response.text))

        with open ("system_msg.txt", "r") as file:
            system_msg = file.read()
        data = {
            "content": str(message),
            "id": str(thread.id),
            "model": settings.model,
            "frequency_penalty": settings.frequency_penalty,
            "presence_penalty": settings.presence_penalty,
            "max_prompt_token": settings.max_prompt_token,
            "max_completion_token": settings.max_completion_token,
            "instructions": system_msg,
            "tools":tools
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
