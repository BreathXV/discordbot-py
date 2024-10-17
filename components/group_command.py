import discord 

from discord import app_commands
from discord.ext import commands

class Command(commands.Cog):
    group = app_commands.Group(name="commands", description="Test a command!")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @group.command(
        name="Ping",
        description="Ping the bot!"
    )
    async def ping(
        self, 
        interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_message("Pong!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Command(bot))