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

    @commands.command(name='image', aliases=["i"])
    async def image(self, ctx, *, message):
        thread = await createThread(ctx, "Voici les fichiers")
        param_dict, message = self.split_json_and_text(message)

        prompt_data = {
            "model": "dall-e-3",
            "quality": "hd",  # ou autre valeur si besoin
            "size": "1024x1024",  # adapte selon ce que tu veux
            "style": "vivid",  # ou "natural", etc.
            "prompt": str(message)
        }
        print(prompt_data)
        try:
            for k in prompt_data:
                if k in param_dict and k != "prompt":
                    prompt_data[k] = param_dict[k]
            prompt_data["prompt"] = message
        except: pass

        command = [
            "curl",
            "-X", "POST", settings.images,
            "-H", f"Authorization: {settings.api_key}",
            "-F", f"data={json.dumps(prompt_data)}",
            # "-F", "file=@"+file_name
        ]

        img_response = subprocess.run(command, capture_output=True)
        img_url = img_response.stdout.decode().strip()
        response = requests.get(img_url)
        if response.status_code == 200:
            file = File(io.BytesIO(response.content), filename="image.png")
            await ctx.send(file=file)
        else:
            await ctx.send("Impossible de récupérer l'image !")

async def setup(bot):
    await bot.add_cog(image(bot))
