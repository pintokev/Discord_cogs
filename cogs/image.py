from discord.ext import commands
from discordhandler import createThread, stream_reponse_file
from discord import File
from config import settings
import requests
import subprocess
import os
import io
import json


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

    async def edit_image(self, message, filename, thread):
        import base64
        if os.path.exists("image.png"):
            os.remove("image.png")
        prompt_data = {
            "model": "gpt-image-1",
            "prompt": str(message)
        }

        command = [
            "curl",
            "-X", "POST", settings.edit_images,
            "-H", f"Authorization: {settings.api_key}",
            "-F", f"data={json.dumps(prompt_data)}",
            "-F", "file=@"+filename
        ]

        img_response = subprocess.run(command, capture_output=True)
        image_b64 = img_response.stdout.decode().strip()
        image_bytes = base64.b64decode(image_b64)
        file = File(io.BytesIO(image_bytes), filename="image.png")
        await thread.send(file=file)

    async def create_image(self, message, thread):
        import base64
        if os.path.exists("image.png"):
            os.remove("image.png")
        prompt_data = {
            "model": "gpt-image-1",
            "quality": "high",  # ou autre valeur si besoin
            "size": "1024x1024",  # adapte selon ce que tu veux
            "prompt": str(message)
            # "response_format":"b64_json"
        }

        command = [
            "curl",
            "-X", "POST", settings.images,
            "-H", f"Authorization: {settings.api_key}",
            "-F", f"data={json.dumps(prompt_data)}",
            # "-F", "file=@"+file_name
        ]
        img_response = subprocess.run(command, capture_output=True)
        img_url = img_response.stdout.decode().strip()
        try:
            response = requests.get(img_url)
            image = response.content
        except:
            image = base64.b64decode(img_url)
        file = File(io.BytesIO(image), filename="image.png")
        await thread.send(file=file)

    @commands.command(name='image', aliases=["i"])
    async def image(self, ctx, *, message):
        thread = await createThread(ctx, "Voici l'image")
        if os.path.exists("image.png"):
            os.remove("image.png")
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                response = requests.get(attachment.url)
                file_name = attachment.filename
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                await self.edit_image(message, file_name, thread)
                break
        else:
            await self.create_image(message, thread)


async def setup(bot):
    await bot.add_cog(image(bot))