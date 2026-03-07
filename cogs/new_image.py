from discord.ext import commands
from discordhandler import createThread
from config import settings
import requests
import io
import base64
import discord
from io import BytesIO


class new_image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="new_image", aliases=["i"])
    async def new_image(self, ctx, *, message):
        thread = await createThread(ctx, "Voici l'image")

        files = []
        opened_files = []

        prompt_data = {
            "message": str(message),
            "model": settings.model_gemini,
            "aspect_ratio": settings.image_aspect_ratio,
            "image_size": settings.image_size,
            "thinking_level": settings.image_thinking_level,
            "file_prefix": f"image_{thread.id}",
            "max_input_images": settings.image_max_input_images,
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
                    files.append(("files", (attachment.filename, file_bytes, content_type)))

            async with thread.typing():
                response = requests.post(
                    settings.new_images,
                    data=prompt_data,
                    files=files if files else None,
                    timeout=180,
                )

            if response.status_code != 200:
                await thread.send(f"Erreur backend ({response.status_code}) : {response.text[:1500]}")
                return

            payload = response.json()

            if not payload.get("success"):
                await thread.send(payload.get("error", "Erreur inconnue côté backend."))
                return

            if payload.get("text"):
                await thread.send(payload["text"])

            returned_images = payload.get("images", [])
            if not returned_images:
                await thread.send("Aucune image générée.")
                return

            discord_files = []
            for img in returned_images:
                b64_data = img.get("b64_data")
                filename = img.get("filename", "image.png")

                if not b64_data:
                    continue

                image_bytes = base64.b64decode(b64_data)
                discord_files.append(
                    discord.File(
                        fp=BytesIO(image_bytes),
                        filename=filename,
                    )
                )

            if not discord_files:
                await thread.send("Aucune image exploitable reçue.")
                return

            await thread.send(files=discord_files)

        except requests.Timeout:
            await thread.send("Le backend Gemini a mis trop de temps à répondre.")
        except requests.RequestException as e:
            await thread.send(f"Erreur réseau/backend : {e}")
        except ValueError:
            await thread.send("Réponse backend invalide.")
        except Exception as e:
            await thread.send(f"Erreur inattendue : {e}")
        finally:
            for file_obj in opened_files:
                try:
                    file_obj.close()
                except Exception:
                    pass


async def setup(bot):
    await bot.add_cog(new_image(bot))