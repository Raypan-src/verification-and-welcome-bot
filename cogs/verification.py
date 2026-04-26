import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

Database = os.getenv("VERIFY_DB")
Verfication_emoji = "✅"

class verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild = self.bot.get_guild(payload.guild_id)
        verification_role = discord.utils.get(guild.roles, "Verified")
        member = guild.get_member(payload.user_id)

        if payload.emoji != Verfication_emoji:
            return
        
        await member.add_roles(verification_role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        guild = self.bot.get_guild(payload.guild_id)
        verification_role = discord.utils.get(guild.roles, "Verified")
        member = guild.get_member(payload.user_id)

        if payload.emoji == Verfication_emoji:
            await member.remove_roles(verification_role)


    @app_commands.command(name="set_verification_channel", description="Set a verification channel")
    @app_commands.describe(channel="Select the channel you want to set", message="Type the message you want to send")
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        set_record = self.bot.db.execute(
            """
            INSERT INTO verification (guild_id, channel_id, message) VALUES ($1, $2, $3)
            ON CONFLICT (guild_id)
            DO UPDATE SET channel_id = $2, message = $3
            """,
            interaction.guild_id,
            channel.id,
            message
        )
        await interaction.response.defer()
        await interaction.followup.send(f"Channel {channel.mention} has been set with message: {message}")
        await channel.send(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(verification(bot))