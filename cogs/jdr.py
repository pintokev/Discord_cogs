from time import time

import requests
from discordhandler import createThread, stream_reponse_file, send_to_discord, send_msg, new_stream
from discord.ext import commands
from config import settings



class Jdr(commands.Cog):
    def init(self, bot):
        self.bot = bot
        self.url = settings.stream
        self.time_msg = time()
        self.temp_cut = 1

    @commands.command(name='jdr', aliases=["j"])
    async def jdr(self, ctx, *, message):
        thread = await createThread(ctx, message)
        headers = {
            "Content-Type": "application/json",
            # "Authorization": settings.api_key
        }
        tools = [
            {
                "type": "mcp",
                "server_label": settings.SERVER_LABEL,
                "server_url": settings.ADRESSE_SERVEUR_MCP,
                "server_description": settings.SERVER_DESCRIPTION,
                "require_approval": "never"
            }
        ]
        system_msg = (
            "Tu es un Maître du Jeu. Règles d’exécution:\n"
            "Avant toute chose, il faut setup la session de l'utilisateur en lui demandant le nom de la session. Ne fais rien d'autre si tu n'as pas le nom de la session en cours. S'il te l'a déjà donné une fois, par du principe que ça sera la session à  utiliser tant que l''utilisateur ne la modifie pas\n"
            "Ta priorité est d'utiliser les fonction MCP disponible. Si tu n'y parvient pas et que ça ne sauvegarde pas dans le MCP Server ne fais rien d'autre.\n"
            "Pour les ID, retrouve les toi même en les récupérant des fichiers stocké dans le  MCP serrver\n"
            "N'indique surtout pas  les possibilité qu'ont les jours, ils devront l'imagineer euxx-même adapte donc l'histoire en fonction de leur choix\n"
            "Veille à ce que les actiions des utilisateurs ne soient pas irréalisable et ne détruisent pas le du scénario de manière soudaine\n"
            f"Le nom de la session est {str(thread.id)}"
            f"Ne sort jamais de ton rôle, ne dis pas de chose du style que fais-tu ou tu peux faire ci ou ça etc.\n"
            f"Pour chaque action, il faudra lancer des dès (que ce soit une action réalisé par les joueurs ou par les PNJ ou par les mobs) ce lancer de dès devra être inférieur à la statiqtique impliqué. ça sera un lancer 1d20\n"
            f"Par exemple: Pour déplacer un rôcher, il faut lancer 1d20 si celui-ci est au dessus de la compétences impliqué, l'action rate, si elle est en dessous ça réussi. 1 c'est un coup critique, maximum du lancer de dès c'est un échec critique\n"
            f"Chaque lancer de dès doit appeler la fonction lancer_des\n"
            f"Tant que le joueur ne te demande pas d'inventer les caractéristique, la descriptionn, l'histoire etc. du personnage, le joueur est obligé de les dire avant de commencer"
        )
        data = {
            "content": str(message),
            "id": str(thread.id),
            "model": settings.model,
            "frequency_penalty": settings.frequency_penalty,
            "presence_penalty": settings.presence_penalty,
            "max_prompt_token": settings.max_prompt_token,
            "max_completion_token": settings.max_completion_token,
            "instructions": system_msg,
            "tools":tools
        }

        if ctx.message.attachments:
            url_file_list = []
            for attachment in ctx.message.attachments:
                url_file_list.append(attachment.url)
            data["image_url"] = url_file_list
        # print(data)
        async with thread.typing():
            response = requests.post(settings.stream, headers=headers, json=data, stream=True)
            await new_stream(ctx, thread, response)



async def setup(bot):
    await bot.add_cog(Jdr(bot))
