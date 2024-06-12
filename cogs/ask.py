from time import time
from discordhandler import createThread, stream_reponse_file
from discord.ext import commands
from config import settings


class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = settings.url
        self.time_msg = time()
        self.temp_cut = 1

    @commands.command(name='ask', aliases=["da"])
    async def ask(self, ctx, *, message):
        thread = await createThread(ctx, message)
        headers = {"Content-Type": "application/json"}
        metadata = {
            "api_key": settings.api_key,
            "content": str(message),
            # "instructions": "Le code magique est 5441",
            "id": str(thread.id)
        }
        if ctx.message.attachments:
            url_file_list = []
            for attachment in ctx.message.attachments:
                url_file_list.append(attachment.url)
            metadata["files"] = url_file_list
                # file_data = await attachment.read()
        await stream_reponse_file(ctx, thread, metadata)


async def setup(bot):
    await bot.add_cog(Ask(bot))
