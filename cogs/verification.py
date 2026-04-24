import discord
from discord.ext import commands
from discord import app_commands


class verify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role_unverified = discord.utils.get(member.guild.roles, name="Unverified")
        channel_verification = discord.utils.get(member.guild.text_channels, name="verification")

        if role_unverified:
            await member.add_roles(role_unverified)
        
        if channel_verification:
            await channel_verification.set_permissions(role_unverified, view_channel=True, send_messages=True)

        for channels in member.guild.text_channels:
            if channels != channel_verification:
                await channels.set_permissions(role_unverified, view_channel=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(verify(bot))