from time import time
import requests
from src.discordhandler import createThread, stream_reponse_file, send_to_discord, send_msg, new_stream
from discord.ext import commands
from src.config import settings
import discord
from datetime import datetime
import pytz
import os

PURGEDATE = 604_800

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, member: discord.Member = None):
        """
        Purge les fils où un utilisateur spécifique est présent ou tous les fils selon la date.
        :param ctx: Contexte Discord.
        :param member: (Optionnel) Membre dont la présence dans les fils doit être vérifiée.
        """
        async with ctx.channel.typing():
            if member:
                await ctx.channel.send(f"Suppression des threads contenant le membre {member.display_name}")
                guild = ctx.guild

                threads_to_purge = []
                for thread in guild.threads:
                    for thread_member in await thread.fetch_members():
                        if (member.id == thread_member.id):
                            threads_to_purge.append(thread)
                            break

                for channel in guild.text_channels:
                    async for thread in channel.archived_threads(limit=None):
                        if thread_member in await thread.fetch_members():
                            if (member.id == thread_member.id):
                                threads_to_purge.append(thread)
                                break
            else:
                await ctx.channel.send(
                    f"Suppression des threads inactifs depuis plus de {int(PURGEDATE / 86_400)} jours.")
                time_to_delete = time() - PURGEDATE
                guild = ctx.guild

                # Filtrer les fils par date
                threads_to_purge = list(
                    filter(lambda x: x.created_at is not None and x.created_at <= datetime.fromtimestamp(time_to_delete,
                                                                                                         tz=pytz.utc),
                           guild.threads)
                )

                # Ajouter les fils archivés (peut prendre du temps) et filtrer par date
                for channel in guild.text_channels:
                    threads_to_purge += [thread async for thread in channel.archived_threads(limit=None) if
                                         thread.created_at is not None and thread.created_at <= datetime.fromtimestamp(
                                             time_to_delete, tz=pytz.utc)]

        # Supprimer les fils
        for thread in threads_to_purge:
            await thread.delete()
        await ctx.channel.send(f"{len(threads_to_purge)} threads purgés")



async def setup(bot):
    await bot.add_cog(Purge(bot))
