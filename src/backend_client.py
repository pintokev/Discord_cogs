import asyncio
import json
from time import monotonic

import aiohttp

from src.config import settings

STREAM_TIMEOUT = aiohttp.ClientTimeout(total=None, sock_connect=30, sock_read=600)
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=180, sock_connect=30, sock_read=180)


def build_backend_headers(content_type: str | None = "application/json") -> dict[str, str]:
    headers = {}

    if content_type:
        headers["Content-Type"] = content_type

    if settings.INTERNAL_API_TOKEN:
        headers["X-Internal-Api-Token"] = settings.INTERNAL_API_TOKEN

    return headers


def cut_msg(msg: str) -> list[str]:
    return [msg[i:i + 1800] for i in range(0, len(msg), 1800)]


def trouver_debut_bloc_code(message: str) -> tuple[int, str]:
    parts = message.rsplit("```", 2)
    if len(parts) < 2:
        return 0, "```"

    last_open = parts[-2].splitlines()
    if not last_open:
        return 0, "```"

    fence = last_open[-1].strip()
    if fence.startswith("```") and len(fence) > 3:
        return 1, f"{fence}\n"

    return 0, "```"


def trouver_fin_bloc_code(message: str) -> int:
    return message.count("```")


def trouver_bloc_code_cut(message: str) -> bool:
    return trouver_debut_bloc_code(message)[0] == trouver_fin_bloc_code(message) % 2


async def send_msg(target, msg: str):
    return await target.send(content=str(msg))


async def edit_msg(message, msg: str):
    if msg:
        await message.edit(content=str(msg))


async def _flush_stream_buffer(target, msg: str, sent_message=None, last_edit_at: float = 0.0, *, force: bool = False):
    now = monotonic()
    if not force and now - last_edit_at < 1:
        return sent_message, msg, last_edit_at

    if len(msg) <= 1900:
        if sent_message is None:
            sent_message = await send_msg(target, msg)
        else:
            await edit_msg(sent_message, msg)
        return sent_message, msg, now

    chunks = cut_msg(msg)
    if len(chunks) > 1 and not trouver_bloc_code_cut(chunks[0]):
        chunks[0] += "```"
        chunks[1] = trouver_debut_bloc_code(chunks[0])[1] + chunks[1]

    if sent_message is None:
        sent_message = await send_msg(target, chunks[0])
    else:
        await edit_msg(sent_message, chunks[0])

    for chunk in chunks[1:]:
        sent_message = await send_msg(target, chunk)

    return sent_message, chunks[-1], now


async def stream_backend_response(target, url: str, payload: dict):
    msg = ""
    sent_message = await send_msg(target, "Message en cours...")
    last_edit_at = 0.0

    try:
        async with aiohttp.ClientSession(timeout=STREAM_TIMEOUT) as session:
            async with session.post(url, json=payload, headers=build_backend_headers()) as response:
                if response.status >= 400:
                    error_text = (await response.text())[:1500]
                    await edit_msg(sent_message, f"Erreur backend ({response.status}) : {error_text}")
                    return

                async for chunk in response.content.iter_chunked(1024):
                    msg += chunk.decode("utf-8")
                    sent_message, msg, last_edit_at = await _flush_stream_buffer(
                        target,
                        msg,
                        sent_message,
                        last_edit_at,
                    )
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        await edit_msg(sent_message, f"Erreur réseau/backend : {exc}")
        return

    await edit_msg(sent_message, msg or "Réponse vide.")


async def post_backend_json(url: str, payload: dict, *, params: dict | None = None) -> tuple[int, str]:
    try:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.post(
                url,
                json=payload,
                params=params,
                headers=build_backend_headers(),
            ) as response:
                return response.status, await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        return 502, f"Erreur réseau/backend : {exc}"


async def post_backend_form(
    url: str,
    *,
    fields: dict | None = None,
    json_payload: dict | None = None,
    files: list[dict] | None = None,
) -> tuple[int, str, str]:
    form_data = aiohttp.FormData()

    if json_payload is not None:
        form_data.add_field("data", json.dumps(json_payload), content_type="application/json")

    for key, value in (fields or {}).items():
        form_data.add_field(key, str(value))

    for file in files or []:
        form_data.add_field(
            file["field"],
            file["content"],
            filename=file["filename"],
            content_type=file["content_type"],
        )

    try:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.post(url, data=form_data, headers=build_backend_headers(content_type=None)) as response:
                return response.status, await response.text(), response.headers.get("Content-Type", "")
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        return 502, f"Erreur réseau/backend : {exc}", "text/plain"


async def read_attachments(attachments, *, field_name: str) -> list[dict]:
    files = []
    for attachment in attachments:
        files.append(
            {
                "field": field_name,
                "filename": attachment.filename,
                "content_type": attachment.content_type or "application/octet-stream",
                "content": await attachment.read(),
            }
        )
    return files
