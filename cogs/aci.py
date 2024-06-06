from json import dumps

import aiohttp
import discord
from discord.ext import commands
import requests
import os

from bot.discordhandler import createThread, send_to_discord, edit_msg, stream_reponse_file
from config import settings
from bot.discordhandler import stream_reponse


class Aci(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def aci(self, ctx, *, message):
    #     print("Message", message)
    #     thread = await createThread(ctx, "Voici les fichiers")
    #     headers = {"Content-Type": "multipart/form-data"}
    #     if ctx.message.attachments:
    #         async with aiohttp.ClientSession() as session:
    #             for attachment in ctx.message.attachments:
    #                 temp_filename = attachment.filename
    #                 metadata = {
    #                     "api_key": settings.api_key,
    #                     "id": str(thread.id),
    #                     "content": message,
    #                     "for_code_interpreter": True
    #                 }
    #                 form_data = aiohttp.FormData()
    #                 form_data.add_field('metadata', dumps(metadata), content_type="multipart/form-data")
    #                 file_data = await attachment.read()
    #                 form_data.add_field('file', file_data, filename=attachment.filename)
    #                 print(form_data)
    #                 # await stream_reponse_file(thread, form_data, headers)
    #
    #                 async with session.post(settings.url, data=form_data) as response:
    #                     await ctx.send(f"Fichier envoyé avec succès : {response.status}")

    # @commands.command()
    # async def aci(self, ctx):
    #     thread = await createThread(ctx, "Voici les fichiers")
    #     if ctx.message.attachments:
    #         async with aiohttp.ClientSession() as session:
    #             for attachment in ctx.message.attachments:
    #                 temp_filename = attachment.filename
    #                 metadata = {
    #                     "api_key": settings.api_key,
    #                     "id": str(thread.id),
    #                     "content": "Voici les fichiers",
    #                     "for_code_interpreter": True
    #                 }
    #                 form_data = aiohttp.FormData()
    #                 form_data.add_field('metadata', dumps(metadata), content_type="multipart/form-data")
    #                 file_data = await attachment.read()
    #                 form_data.add_field('file', file_data, filename=attachment.filename)
    #                 # print(file_data)
    #             try:
    #                 async with session.post(settings.url, data=form_data) as response:
    #                     if response.status == 200:
    #                         await ctx.send(f"Fichier envoyé avec succès : {response.status}")
    #                     else:
    #                         await ctx.send(f"Erreur lors de l'envoi du fichier : {response.status}")
    #             except aiohttp.ClientError as e:
    #                 await ctx.send(f"Erreur lors de l'envoi du fichier : {str(e)}")
    #
    # @commands.command()
    # async def aci(self, ctx):
    #     thread = await createThread(ctx, "Voici les fichiers")
    #     if ctx.message.attachments:
    #         async with aiohttp.ClientSession() as session:
    #             form_data = aiohttp.FormData()
    #             metadata = {
    #                 "api_key": settings.api_key,
    #                 "id": str(thread.id),
    #                 "content": "Voici les fichiers. Retourne moi seulement un . et rien d'autre",
    #                 "for_code_interpreter": True
    #             }
    #             form_data.add_field('metadata', dumps(metadata), content_type="multipart/form-data")
    #             for attachment in ctx.message.attachments:
    #                 file_data = await attachment.read()
    #                 form_data.add_field('file', file_data, filename=attachment.filename)
    #             try:
    #                 async with session.post(settings.url, data=form_data) as response:
    #                     if response.status == 200:
    #                         await ctx.send(f"Fichier(s) envoyé(s) avec succès : {response.status}")
    #                     else:
    #                         await ctx.send(f"Erreur lors de l'envoi du fichier : {response.status}")
    #             except aiohttp.ClientError as e:
    #                 await ctx.send(f"Erreur lors de l'envoi du fichier : {str(e)}")
    @commands.command()
    async def aci(self, ctx):
        thread = await createThread(ctx, "Voici les fichiers")
        metadata = {
            "api_key": settings.api_key,
            "id": str(thread.id),
            "content": "Voici les fichiers. Retourne moi seulement une phrase m'indiquant que les fichiers ont été sauvegarder, donne moi les file_id de chacun des fichiers présent et rien d'autre",
            "for_code_interpreter": True
        }
        if ctx.message.attachments: await stream_reponse_file(ctx, metadata)


async def setup(bot):
    await bot.add_cog(Aci(bot))
