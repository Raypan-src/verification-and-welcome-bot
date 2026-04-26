import discord
from discord.ext import commands
from discord import app_commands

class welcome_bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    welcome = app_commands.Group(name="welcome", description="Welcome commands")

    @welcome.command(name="set", description="Set a channel and welcome message for new members")
    @app_commands.describe(channel="The channel to send welcome messages in", message="The welcome message to send in the channel")
    async def set_welcome(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        await self.bot.db.execute(
            """
            INSERT INTO welcome (guild_id, channel_id, welcome_message) VALUES ($1, $2, $3)
            ON CONFLICT (guild_id)
            DO UPDATE SET channel_id = $2, welcome_message = $3
            """,
            channel.id,
            message
        )

        await interaction.response.send_message(f"Welcome channel set to {channel.mention} with message: {message}", ephemeral=True)

    async def on_member_join(self, member: discord.Member):
        welcome_data = await self.bot.db.fetchrow(
            """
            SELECT channel_id, welcome_message FROM welcome WHERE guild_id = $1
            """,
            member.guild.id
        )
        if welcome_data:
            channel = member.guild.get_channel(welcome_data["channel_id"])
            welcome_message = welcome_data["welcome_message"]
            message = welcome_message.replace("{member}", member.mention).replace("{user}", member.mention)
            await channel.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(welcome_bot(bot))