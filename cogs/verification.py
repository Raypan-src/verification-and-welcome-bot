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

        if role_unverified:
            await member.add_roles(role_unverified)

        for channels in member.guild.text_channels:
            if channels.name == "verification":
                await channels.set_permissions(role_unverified, view_channel=True, send_messages=True)
            else:
                await channels.set_permissions(role_unverified, view_channel=False)

    @app_commands.command(name="verify", description="Verify yourself")
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def member_verify(self, interaction: discord.Interaction, member: discord.Member):
        role_unverified = discord.utils.get(member.guild.roles, name="Unverified")
        role_verify = discord.utils.get(member.guild.roles, name="Verified")

        if role_verify:
            member.add_roles(role_verify)
            member.remove_roles(role_unverified)
        
        for channels in member.guild.text_channels:
            if channels.name == "verification":
                await channels.set_permissions(role_verify, view_channel=False)
            else:
                await channels.set_permissions(role_verify, view_channel=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(verify(bot))