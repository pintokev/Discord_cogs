from discord.ext import commands
from src.discordhandler import createThread
from src.config import settings
import requests
import io
import json
import base64
import discord
from io import BytesIO


class gptnewimage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gptnewimage", aliases=["ni"])
    async def gptnewimage(self, ctx, *, message):
        '''Genere une image avec GPT Image. Ne garde pas d'historique'''
        thread = await createThread(ctx, "Voici l'image")

        files = []
        opened_files = []

        prompt_data = {
            "prompt": str(message),
            "model": settings.model_gpt_image,
            "size": settings.gpt_image_size,
            "quality": settings.gpt_image_quality,
            "background": settings.gpt_image_background,
            "output_format": settings.gpt_image_output_format,
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
                    settings.gpt_new_images,
                    data={"data": json.dumps(prompt_data)},
                    files=files if files else None,
                    timeout=180,
                )

            if response.status_code != 200:
                await thread.send(f"Erreur backend ({response.status_code}) : {response.text[:1500]}")
                return

            raw_b64 = response.text.strip()
            if not raw_b64:
                await thread.send("Aucune image generee.")
                return

            try:
                image_bytes = base64.b64decode(raw_b64)
            except Exception:
                await thread.send(f"Reponse backend invalide : {response.text[:1500]}")
                return

            extension = "png"
            if settings.gpt_image_output_format == "jpeg":
                extension = "jpg"
            elif settings.gpt_image_output_format == "webp":
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
    await bot.add_cog(gptnewimage(bot))