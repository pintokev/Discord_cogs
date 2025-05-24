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


class new_image(commands.Cog):
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

    @commands.command(name='new_image', aliases=["ni"])
    async def image(self, ctx, *, message):
        thread = await createThread(ctx, "Voici l'image")

        prompt_data = {
            "model": "gpt-image-1",
            "quality": "high",  # ou autre valeur si besoin
            "size": "1024x1024",  # adapte selon ce que tu veux
            "prompt": str(message),
            "id": str(thread.id)
        }
        if ctx.message.attachments:
            async with thread.typing():
                await thread.send("Cette commande n'accepte pas de pièces jointes, donc pas de modification d'image. Pour modifier une image, il faut utiliser !i")
                return

        data = {'data': json.dumps(prompt_data)}
        headers = {'Authorization': settings.api_key}

        async with thread.typing():
            response = requests.post(settings.images, headers=headers, data=data)
            image_b64 = response.text
            img_data = base64.b64decode(image_b64)
            file = discord.File(BytesIO(img_data), filename='image.png')
            await thread.send(file=file)


async def setup(bot):
    await bot.add_cog(new_image(bot))
