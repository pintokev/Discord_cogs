from discord.ext import commands
from src.config import settings
from src.cog_helpers import build_mcp_tools, stream_chat_command

class Jdr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='jdr', aliases=["j"])
    async def jdr(self, ctx, *, message):
        """Permet de lancer une session de JDR avec chatGPT. Utilise un système de sauvegarde pour avoir des données correctes et réelles"""
        tools = build_mcp_tools()
        extra_payload = {
            "reasoning": {"effort": "low"},
        }
        if tools:
            extra_payload["tools"] = tools
            extra_payload["tool_choice"] = "required"

        await stream_chat_command(
            ctx,
            message,
            model=settings.model,
            instructions=settings.system_jdr_msg,
            extra_payload=extra_payload,
        )

async def setup(bot):
    await bot.add_cog(Jdr(bot))
