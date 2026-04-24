import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv("DISCORD_TOKEN")
ext = "cogs.verification"

class main(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        await self.load_extension(ext)
        await self.tree.sync()
        print("Extension loaded and tree synced!")

    async def on_ready(self):
        print("Bot is ready!")

bot = main(command_prefix="!", intents=discord.Intents.all())
bot.run(Token)        