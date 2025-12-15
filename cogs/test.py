from time import time

import requests
from discordhandler import createThread, stream_reponse_file, send_to_discord, send_msg, new_stream
from discord.ext import commands
from config import settings



class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = settings.stream
        self.time_msg = time()
        self.temp_cut = 1

    @commands.command(name='test', aliases=["t"])
    async def codex(self, ctx, *, message):
        """Sert de test pendant le développement, ne fait rien la majorité du temps"""
        pass
#         thread = await createThread(ctx, message)
#         headers = {
#             "Content-Type": "application/json",
#             # "Authorization": settings.api_key
#         }
#         data = {
#             "content": str(message),
#             "id": str(thread.id),
#             "model": settings.model_test,
# #            "temperature": settings.temperature,
# #            "top_p": settings.top_p,
#             "frequency_penalty": settings.frequency_penalty,
#             "presence_penalty": settings.presence_penalty,
#             "max_prompt_token": settings.max_prompt_token,
#             "max_completion_token": settings.max_completion_token,
#             "instructions": settings.instructions,
#             "reasonning": {"effort": "high"},
#         }
#
#         if ctx.message.attachments:
#             url_file_list = []
#             for attachment in ctx.message.attachments:
#                 url_file_list.append(attachment.url)
#             data["image_url"] = url_file_list
#         # print(data)
#         async with thread.typing():
#             response = requests.post(settings.stream, headers=headers, json=data, stream=True)
#             await new_stream(ctx, thread, response)



async def setup(bot):
    await bot.add_cog(Test(bot))
