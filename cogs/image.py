from discord.ext import commands
from discordhandler import createThread, stream_reponse_file
from discord import File
from config import settings
import requests
import subprocess
import os
import io
import json
import base64
import discord
from io import BytesIO


class image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def split_json_and_text(self, message):
        import re
        match = re.match(r'(\{.*\})(.*)', message, re.DOTALL)
        if match:
            json_part = match.group(1).strip()
            text_part = match.group(2).strip()
            try:
                data = json.loads(json_part)
                return data, text_part
            except Exception:
                pass
        return None, message.strip()

    @commands.command(name='image', aliases=["i"])
    async def image(self, ctx, *, message):
        """Génère une image avec l'api d'openai. Garde l'historique de conversation et la dernière image. Utile pour modifier la dernière image générée"""
        thread = await createThread(ctx, "Voici l'image")

        files = []
        if ctx.message.attachments:
            prompt_data = {
                "model": "gpt-image-1",
                "prompt": str(message),
                "id": str(thread.id)
            }
            for attachment in ctx.message.attachments:
                response = requests.get(attachment.url)
                file_bytes = io.BytesIO(response.content)
                file_bytes.name = attachment.filename
                files.append(('file', (attachment.filename, file_bytes)))
        else:
            prompt_data = {
                "model": "gpt-image-1",
                "quality": "high",  # ou autre valeur si besoin
                "size": "1024x1024",  # adapte selon ce  que tu veux
                "prompt": str(message),
                "id": str(thread.id)
            }

        data = {'data': json.dumps(prompt_data)}
        headers = {'Authorization': settings.api_key}


        async with thread.typing():
            response = requests.post(settings.images, headers=headers, data=data, files=files)
            # print(response.text)
            image_b64 = response.text  # extrait la chaîne base64
            img_data = base64.b64decode(image_b64)
            file = discord.File(BytesIO(img_data), filename='image.png')
            await thread.send(file=file)


async def setup(bot):
    await bot.add_cog(image(bot))