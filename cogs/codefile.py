import os
from json import dumps
from time import time
import aiohttp
import requests
from discord.ext import commands
from bot.discordhandler import createThread, send_msg, edit_msg, send_to_discord


class Codefile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = 'http://localhost:25789/stream'
        self.time_msg = time()
        self.temp_cut = 1

    @commands.command(name='codefile', aliases=["cf"])
    async def codefile(self, ctx, *, message):
        thread = await createThread(ctx, message)

        metadata = {
            "api_key": "sk-proj-te1zqNtIhQKBG7vCFcdeT3BlbkFJc1HSZ3RSl6XKWPyhYJEj",
            "id": "DEBUG",
            "for_code_interpreter": True
        }
        files = {
            'metadata': (None, str(metadata), 'application/json'),
            'file': open('/home/pintok/Projets/assistantAI/data/code_interpreter.json', 'rb')
        }
        response = requests.post(self.url, files=files)
        # metadata = {
        #     "api_key": os.environ.get("tokenGPT"),
        #     "content": str(message),
        #     "id": ctx.channel.id
        # }
        # if ctx.message.attachments:
        #     url_file_list = []
        #     for attachment in ctx.message.attachments:
        #         url_file_list.append(attachment.url)
        #     metadata["files"] = url_file_list
        #         # file_data = await attachment.read()
        # async with aiohttp.ClientSession() as session:
        #     msg = ""
        #     M = await send_msg(thread, "Message en cours...")
        #     async with session.post(self.url, headers=headers, json=metadata) as response:
        #         async for chunk in response.content.iter_chunked(1024):
        #             print(chunk.decode('utf-8'), end="", flush=True)
        #             msg += chunk.decode('utf-8')
        #             M, msg = await send_to_discord(thread, M, msg)
        #     await edit_msg(M, msg)

async def setup(bot):
    await bot.add_cog(Codefile(bot))
