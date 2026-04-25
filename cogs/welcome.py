import discord
from discord.ext import commands
from discord import app_commands

class welcome_bot(commands.Cog):
    def __init__(self):
        super().__init__()

    welcome = app_commands.Group(name="welcome", description="Welcome commands")

    @welcome.command(name="set_channel", description="Set a welcome channel and message")
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def set_channel(self, interaction: discord.Interaction, textchannel: discord.TextChannel, message: str):
        await self.bot.db.execute(
            """
            INSERT INTO welcome (guild_id, channel_id, message_welcome)
            VALUES ($1, $2, $3)
            ON CONFLICT (guild_id) DO UPDATE SET channel_id = $2, message_welcome = $3
            """,
            interaction.guild.id,
            textchannel.id,
            message
        )

        await interaction.response.send_message(f"Welcome channel set to {textchannel.mention}", ephemeral=True)

    @welcome.command(name="send_message", description="Send a welcome message")
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def send_message(self, interaction: discord.Interaction, textchannel: discord.TextChannel, message: str):
        await self.bot.db.fetchrow(
            """
            SELECT channel_id FROM welcome WHERE guild_id = $1
            """,
            interaction.guild.id
        )
        await textchannel.send(message)
        await interaction.response.send_message(f"Message sent to {textchannel.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(welcome_bot())