import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

Token = os.getenv("DISCORD_TOKEN") 
Database_token = os.getenv("VERIFY_DB")
ext = {"cogs.verification", "cogs.welcome"}

class main(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        self.db = await asyncpg.create_pool(Database_token, min_size=4, max_size=5)
        for extension in ext:
            await self.load_extension(extension)
        await self.tree.sync()
        print("Extension loaded and tree synced!")

    async def on_ready(self):
        print("Bot is ready!")

bot = main(command_prefix="!", intents=discord.Intents.all())
bot.run(Token)