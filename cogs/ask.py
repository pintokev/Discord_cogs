import os
from json import dumps
from time import time
import aiohttp
from discord.ext import commands
from bot.discordhandler import createThread, send_msg, edit_msg, send_to_discord


class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = 'http://localhost:25789/stream'
        self.time_msg = time()
        self.temp_cut = 1


    # @commands.command(name='ask', aliases=["da"])
    # async def ask(self, ctx, *, message):
    #     thread = await createThread(ctx, message)
    #     metadata = {
    #         "api_key": os.environ.get("tokenGPT"),
    #         "content": str(message),
    #         "id": ctx.channel.id
    #     }
    #     files = {
    #         'metadata': ('metadata.json', dumps(metadata), 'application/json')
    #     }
    #     print(files)
    #     if ctx.message.attachments:
    #         files['file'] = open('/home/pintok/Projets/assistantAI/data/code_interpreter.json', 'rb')
    #     form_data = aiohttp.FormData()
    #     for key, (filename, content, content_type) in files.items():
    #         form_data.add_field(
    #             name=key,
    #             value=content,
    #             filename=filename,
    #             content_type=content_type
    #         )
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(self.url, data=form_data) as response:
    #             if response.status != 200:
    #                 await ctx.send(f"Error: {response.status}")
    #                 return
    #             response_text = await response.text()
    #             msg = ""
    #             M = await send_msg(thread, "Message en cours...")
    #             for chunk in response_text.split('\n'):
    #                 msg += chunk
    #                 M, msg = await send_to_discord(thread, M, msg)
    #             if not msg.strip():
    #                 await edit_msg(M, "La réponse est vide.")
    #             else:
    #                 await edit_msg(M, msg)

    @commands.command(name='ask', aliases=["da"])
    async def ask(self, ctx, *, message):
        thread = await createThread(ctx, message)

        headers = {"Content-Type": "application/json"}

        metadata = {
            "api_key": os.environ.get("tokenGPT"),
            "content": str(message),
            "id": ctx.channel.id
        }
        if ctx.message.attachments:
            url_file_list = []
            for attachment in ctx.message.attachments:
                url_file_list.append(attachment.url)
            metadata["files"] = url_file_list
                # file_data = await attachment.read()
        async with aiohttp.ClientSession() as session:
            msg = ""
            M = await send_msg(thread, "Message en cours...")
            async with session.post(self.url, headers=headers, json=metadata) as response:
                async for chunk in response.content.iter_chunked(1024):
                    print(chunk.decode('utf-8'), end="", flush=True)
                    msg += chunk.decode('utf-8')
                    M, msg = await send_to_discord(thread, M, msg)
            await edit_msg(M, msg)

async def setup(bot):
    await bot.add_cog(Ask(bot))
async def setup(bot):
    await bot.add_cog(Ask(bot))
