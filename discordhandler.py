import logging
import os
from json import dumps
from time import time
import re

import aiohttp
import discord
from discord.ext import commands

from config import settings
from config.settings import DISCORD_TOKEN

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)
threadPrompt = {}
time_msg = time()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await load_cogs(bot)

async def createThread(ctx, message):
    if ctx.channel.type != discord.ChannelType.public_thread: thread = await ctx.message.create_thread(name="prompt " + str(message[0:92]), auto_archive_duration=4320, reason="PasTesOignons")
    else: thread = ctx.channel
    clear_thread_prompt(ctx.guild)
    return thread

def clear_thread_prompt(guild):
    threads = guild.threads
    thread_to_delete = []
    for thread in threadPrompt.keys():
        if thread not in map(lambda x: x.id, threads): thread_to_delete.append(thread)
    for thread in thread_to_delete: del threadPrompt[thread]

async def load_cogs(bot):
    logging.basicConfig(level=logging.DEBUG)
    try: cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    except Exception as e:
        print(f"Erreur lors de la construction du chemin : {e}")
        return
    if not os.path.isdir(cogs_dir):
        print(f"Le répertoire {cogs_dir} n'existe pas")
        return
    for filename in os.listdir(cogs_dir):
        try:
            if filename.endswith('.py') and "__" not in filename:
                cog_name = f'cogs.{filename[:-3]}'
                print(f'Chargement du cog : {cog_name}')
                await bot.load_extension(cog_name)
        except Exception as e:
            print(f'Echec du chargement de l\'extension {filename}: {e}')
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.content.lower() == 'ping':
        await ctx.channel.send('Pong!')
    await bot.process_commands(ctx)

def cut_msg(msg): return [msg[i:i + 1900] for i in range(0, len(msg), 1900)]
def trouver_debut_bloc_code(message):
    pattern = r'```(\w+)'
    matches = re.findall(pattern, message)
    print("```"+matches[-1])
    return len(matches), "```"+matches[-1]
def trouver_fin_bloc_code(message):
    pattern = r'```(?=\s|\n|$)'
    matches = re.findall(pattern, message)
    return len(matches)
def trouver_bloc_code_cut(message): print(trouver_debut_bloc_code(message)[0], trouver_fin_bloc_code(message)) ; return trouver_debut_bloc_code(message)[0] == trouver_fin_bloc_code(message)
async def send_msg(ctx, msg): return await ctx.send(content=str(msg))
async def edit_msg(M, msg):
    copy_msg = msg
    if msg and msg!="":await M.edit(content=str(msg))
async def send_to_discord(ctx, msg, M=None):
    global time_msg
    if not time() - time_msg < 1:
        time_msg = time()
        if len(msg) <= 1900:
            if M is None: M = await send_msg(ctx, msg)
            else: await edit_msg(M, msg)
        else:
            msg = cut_msg(msg)
            if trouver_bloc_code_cut(msg[0]) != False: msg[0] += "```"
            await edit_msg(M, msg[0])
            if trouver_bloc_code_cut(msg[0]) != False: msg[1] = trouver_debut_bloc_code(msg[0])[1] + msg[1]
            msg = msg[1]
            M = await send_msg(ctx, msg)
    return M, msg

async def stream_reponse(thread, metadata, headers):
    async with aiohttp.ClientSession() as session:
        msg = ""
        M = await send_msg(thread, "Message en cours...")
        async with session.post(settings.url, json=metadata, headers=headers) as response:
            # print(metadata)
            async for chunk in response.content.iter_chunked(1024):
                # print(chunk.decode('utf-8'), end="", flush=True)
                msg += chunk.decode('utf-8')
                M, msg = await send_to_discord(thread, msg, M)
        await edit_msg(M, msg)

async def stream_reponse_file(ctx, thread, metadata):
    form_data = aiohttp.FormData()
    form_data.add_field('metadata', dumps(metadata), content_type="multipart/form-data")

    async with aiohttp.ClientSession() as session:
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                file_data = await attachment.read()
                form_data.add_field('file', file_data, filename=attachment.filename)
        msg = ""
        M = await send_msg(thread, "Message en cours...")
        async with session.post(settings.url, data=form_data) as response:
            async for chunk in response.content.iter_chunked(1024):
                # print(chunk.decode('utf-8'), end="", flush=True)
                msg += str(chunk.decode('utf-8'))
                M, msg = await send_to_discord(thread, msg, M)
        await edit_msg(M, msg)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
