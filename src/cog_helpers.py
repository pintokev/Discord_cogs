import base64
import json
from io import BytesIO

import discord

from src.backend_client import post_backend_form, post_backend_json, read_attachments, stream_backend_response
from src.config import settings
from src.discordhandler import createThread


def build_chat_payload(message: str, conversation_id: str, model: str, *, instructions: str | None = None, extra_payload: dict | None = None, attachment_urls: list[str] | None = None) -> dict:
    payload = {
        "content": str(message),
        "id": str(conversation_id),
        "model": model,
        "frequency_penalty": settings.frequency_penalty,
        "presence_penalty": settings.presence_penalty,
        "max_prompt_token": settings.max_prompt_token,
        "max_completion_token": settings.max_completion_token,
    }

    if instructions is not None:
        payload["instructions"] = instructions

    if attachment_urls:
        payload["image_url"] = attachment_urls

    if extra_payload:
        payload.update(extra_payload)

    return payload


async def stream_chat_command(ctx, message: str, *, model: str, instructions: str | None = None, extra_payload: dict | None = None, target=None, conversation_id: str | None = None):
    if target is None:
        target = await createThread(ctx, message)

    attachment_urls = [attachment.url for attachment in ctx.message.attachments] if ctx.message.attachments else None
    payload = build_chat_payload(
        message,
        conversation_id or str(target.id),
        model,
        instructions=instructions,
        extra_payload=extra_payload,
        attachment_urls=attachment_urls,
    )

    async with target.typing():
        await stream_backend_response(target, settings.stream, payload)

    return target


async def send_backend_text(target, url: str, payload: dict, *, params: dict | None = None):
    status, text = await post_backend_json(url, payload, params=params)
    if status >= 400:
        await target.send(f"Erreur backend ({status}) : {text[:1500]}")
    else:
        await target.send(text[:1900] if text else "Réponse vide.")


async def send_gemini_images(ctx, message: str, url: str, *, image_size: str):
    thread = await createThread(ctx, "Voici l'image")
    files = await read_attachments(ctx.message.attachments, field_name="files")
    prompt_data = {
        "message": str(message),
        "model": settings.model_gemini,
        "aspect_ratio": settings.image_aspect_ratio,
        "image_size": image_size,
        "thinking_level": settings.image_thinking_level,
        "file_prefix": f"image_{thread.id}",
        "max_input_images": settings.image_max_input_images,
        "id": str(thread.id),
    }

    async with thread.typing():
        status, body, _ = await post_backend_form(url, fields=prompt_data, files=files)

    if status >= 400:
        await thread.send(f"Erreur backend ({status}) : {body[:1500]}")
        return

    try:
        parsed = json.loads(body)
    except Exception:
        await thread.send("Réponse backend invalide.")
        return

    if not parsed.get("success"):
        await thread.send(parsed.get("error", "Erreur inconnue côté backend."))
        return

    if parsed.get("text"):
        await thread.send(parsed["text"])

    returned_images = parsed.get("images", [])
    if not returned_images:
        await thread.send("Aucune image générée.")
        return

    discord_files = []
    for img in returned_images:
        b64_data = img.get("b64_data")
        filename = img.get("filename", "image.png")

        if not b64_data:
            continue

        discord_files.append(discord.File(fp=BytesIO(base64.b64decode(b64_data)), filename=filename))

    if not discord_files:
        await thread.send("Aucune image exploitable reçue.")
        return

    await thread.send(files=discord_files)


async def send_gpt_images(ctx, message: str, url: str, *, keep_history: bool):
    thread = await createThread(ctx, "Voici l'image")
    files = await read_attachments(ctx.message.attachments, field_name="file")
    payload = {
        "prompt": str(message),
        "model": settings.model_gpt_image,
        "size": settings.gpt_image_size,
        "quality": settings.gpt_image_quality,
        "background": settings.gpt_image_background,
        "output_format": settings.gpt_image_output_format,
        "id": str(thread.id),
    }

    async with thread.typing():
        status, body, _ = await post_backend_form(
            url,
            json_payload=payload,
            files=files,
        )

    if status >= 400:
        await thread.send(f"Erreur backend ({status}) : {body[:1500]}")
        return

    raw_b64 = body.strip()
    if not raw_b64:
        await thread.send("Aucune image générée." if not keep_history else "Le backend n'a renvoyé aucune image.")
        return

    try:
        image_bytes = base64.b64decode(raw_b64)
    except Exception:
        await thread.send(f"Réponse backend invalide : {raw_b64[:1500]}")
        return

    extension = "png"
    if settings.gpt_image_output_format == "jpeg":
        extension = "jpg"
    elif settings.gpt_image_output_format == "webp":
        extension = "webp"

    await thread.send(
        files=[discord.File(fp=BytesIO(image_bytes), filename=f"gpt_image_{thread.id}.{extension}")]
    )


def build_mcp_tools() -> list[dict]:
    if not settings.SERVER_LABEL or not settings.ADRESSE_SERVEUR_MCP:
        return []

    return [
        {
            "type": "mcp",
            "server_label": settings.SERVER_LABEL,
            "server_url": settings.ADRESSE_SERVEUR_MCP,
            "server_description": settings.SERVER_DESCRIPTION,
            "require_approval": "never",
        }
    ]
