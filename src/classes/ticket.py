from __future__ import annotations
import discord
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from ..bot import AQWVerifier

class VerifyTicket(discord.ui.View):
    def __init__(self, bot: AQWVerifier, ccid: int, username: str, specific_item: dict[str, str|int]):
        super().__init__(timeout=None)
        self.bot = bot
        self.ccid = ccid
        self.username = username
        self.specific_item = specific_item

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.primary)
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        is_there = await self.bot.verify_item(self.username, self.specific_item['strName'])
        if  not is_there:
            await interaction.response.send_message(embed=discord.Embed(title="Your verification failed", description="We found this item in your inventory but you're not wearing it! Please verify again."), ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Verification complete!", description="Welcome to the server."), ephemeral=True)
            if self.bot.verify_guild(self.username, "drift"):
                await interaction.user.add_roles(discord.Object(id=1370919058542952649))
            await interaction.user.add_roles(discord.Object(id=1371202583947116614))
            await interaction.user.edit(nick=f"{interaction.user.display_name} ({self.username})")



