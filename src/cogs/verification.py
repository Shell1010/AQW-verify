from __future__ import annotations
import discord

from discord.ext import commands
from discord import app_commands
from typing import TYPE_CHECKING
import random

from discord.types import user

from ..classes import VerifyTicket

if TYPE_CHECKING:
    from ..bot import AQWVerifier

class Verification(commands.Cog):
    def __init__(self, bot: AQWVerifier) -> None:
        self.bot = bot

    @app_commands.command(name="verify", description="Verify your AQW Account")
    @app_commands.describe(username="Your AQW username")
    async def verify(self, ctx: discord.Interaction, username: str):
        user_check = await self.bot.verify_username(username)
        if user_check:
            ccid = await self.bot.get_ccid(username)
            inventory = await self.bot.get_inventory(ccid)
            
            while True:
                specific_item = random.choice(inventory)
                if not self.bot.verify_item(username, specific_item['strName']):
                    break
            await ctx.response.send_message(view=VerifyTicket(self.bot, ccid, username, specific_item),embed=discord.Embed(title="Verification 50% complete", description=f"Now that we've verified your username. We will now verify that this account is yours. We ask you to equip this specific item\n\n`{specific_item['strName']}`\n\nPlease equip this item in-game then wait 30s-1m before clicking verify again."), ephemeral=True)
            
    @app_commands.command(name="sync", description="Syncs commands to the server.")
    async def sync(self, ctx: discord.Interaction):
        await self.bot.tree.sync()
        await ctx.response.send_message("Successfully synced commands!")


async def setup(bot: AQWVerifier):
    await bot.add_cog(Verification(bot))
