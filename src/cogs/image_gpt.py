from io import BytesIO
import base64
import io
import json

import discord
import requests
from discord.ext import commands

from src.config import settings
from src.discordhandler import createThread


class GPTImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = settings.gpt_images
        self.model = settings.model_gpt_image
        self.size = settings.gpt_image_size
        self.quality = settings.gpt_image_quality
        self.background = settings.gpt_image_background
        self.output_format = settings.gpt_image_output_format

    @commands.command(name="gptimage", aliases=["i", "gpti"])
    async def gptimage(self, ctx, *, message):
        """Genere une image avec le modele OpenAI GPT Image via le backend Docker."""
        thread = await createThread(ctx, "Voici l'image")

        files = []
        opened_files = []

        payload = {
            "prompt": str(message),
            "model": self.model,
            "size": self.size,
            "quality": self.quality,
            "background": self.background,
            "output_format": self.output_format,
            "id": str(thread.id),
        }

        try:
            if ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    response = requests.get(attachment.url, timeout=30)
                    response.raise_for_status()

                    file_bytes = io.BytesIO(response.content)
                    file_bytes.name = attachment.filename
                    opened_files.append(file_bytes)

                    content_type = attachment.content_type or "application/octet-stream"
                    files.append(("file", (attachment.filename, file_bytes, content_type)))

            async with thread.typing():
                response = requests.post(
                    self.url,
                    data={"data": json.dumps(payload)},
                    files=files if files else None,
                    timeout=180,
                )

            if response.status_code != 200:
                await thread.send(f"Erreur backend ({response.status_code}) : {response.text[:1500]}")
                return

            raw_b64 = response.text.strip()
            if not raw_b64:
                await thread.send("Le backend n'a renvoye aucune image.")
                return

            try:
                image_bytes = base64.b64decode(raw_b64)
            except Exception:
                await thread.send(f"Reponse backend invalide : {raw_b64[:1500]}")
                return

            extension = "png"
            if self.output_format == "jpeg":
                extension = "jpg"
            elif self.output_format == "webp":
                extension = "webp"

            discord_file = discord.File(
                fp=BytesIO(image_bytes),
                filename=f"gpt_image_{thread.id}.{extension}",
            )
            await thread.send(files=[discord_file])

        except requests.Timeout:
            await thread.send("Le backend GPT Image a mis trop de temps a repondre.")
        except requests.RequestException as e:
            await thread.send(f"Erreur reseau/backend : {e}")
        except Exception as e:
            await thread.send(f"Erreur inattendue : {e}")
        finally:
            for file_obj in opened_files:
                try:
                    file_obj.close()
                except Exception:
                    pass


async def setup(bot):
    await bot.add_cog(GPTImage(bot))
