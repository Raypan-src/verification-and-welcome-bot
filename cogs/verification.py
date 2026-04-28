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
        if payload.user_id == self.bot.user.id:
            return
        
        if str(payload.emoji) != "✅":
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        row = await self.bot.db.fetchrow("SELECT channel_id FROM verification WHERE guild_id = $1", payload.guild_id)
        if row is None or payload.channel_id != row["channel_id"]:
            return
        
        role = discord.utils.get(guild.roles, name="Verified")
        member = guild.get_member(payload.user_id)
        if role is None or member is None:
            return

        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        
        if str(payload.emoji) != "✅":
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        row = await self.bot.db.fetchrow("SELECT channel_id FROM verification WHERE guild_id = $1", payload.guild_id)
        if row is None or payload.channel_id != row["channel_id"]:
            return
        
        role = discord.utils.get(guild.roles, name="Verified")
        member = guild.get_member(payload.user_id)
        if role is None or member is None:
            return

        await member.remove_roles(role)


    @app_commands.command(name="set_verification_channel", description="Set a verification channel")
    @app_commands.describe(channel="Select the channel you want to set", message="Type the message you want to send")
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        await interaction.response.defer()
        await self.bot.db.execute(
            """
            INSERT INTO verification (guild_id, channel_id, message) VALUES ($1, $2, $3)
            ON CONFLICT (guild_id)
            DO UPDATE SET channel_id = $2, message = $3
            """,
            interaction.guild_id,
            channel.id,
            message
        )
        msg = await channel.send(message)
        await msg.add_reaction('✅')
        await interaction.followup.send(f"Channel {channel.mention} has been set with message: {message}")


async def setup(bot: commands.Bot):
    await bot.add_cog(verification(bot))