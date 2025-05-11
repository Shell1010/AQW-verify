from typing import List, Optional
from discord.ext import commands
import discord
import aiohttp
import os
import re

class AQWVerifier(commands.Bot):
    def __init__(self, token: str, admins: dict[str, int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admins = admins
        self.token = token

    async def load_all_cogs(self):
        
        print("Loading cogs...")
        for file in os.listdir("./src/cogs"):
            if file.endswith(".py") and "__init__" not in file:
                try:
                    await self.load_extension(f"src.cogs.{file[:-3]}")
                except Exception as e:
                    print(f"Failed to load cog\n{e}")
        
        print("Cogs loaded.")

    async def verify_guild(self, username: str, guild_name: str) -> bool:
        resp = await self.session.get(f"https://account.aq.com/CharPage?id={username}")
        if resp.ok:
            if guild_name in (await resp.text()):
                return True
        return False

    async def verify_item(self, username: str, item_name: str) -> bool:
        resp = await self.session.get(f"https://account.aq.com/CharPage?id={username}")
        if resp.ok:
            if item_name in (await resp.text()):
                return True
        return False
 

    async def verify_username(self, username: str) -> bool:
        resp = await self.session.get(f"https://account.aq.com/CharPage?id={username}")
        if resp.ok:
            if not "Not Found" in (await resp.text()):
                return True
        return False

    async def get_ccid(self, username: str) -> Optional[int]:
        resp = await self.session.get(f"https://account.aq.com/CharPage?id={username}")
        if resp.ok:
            text = await resp.text()
            match = re.search(r'var\s+ccid\s*=\s*(\d+);', text)
            if match:
                return int(match.group(1))

    async def get_inventory(self, ccid: int) -> List[dict[str, int|str]]:
        resp = await self.session.get(f"https://account.aq.com/CharPage/inventory?ccid={ccid}")
        if resp.ok:
            json = await resp.json()
            unwanted = {"floor item", "wall item", "misc", "house", "item", "quest item", "resource", "necklace"}

            filtered = [
                item for item in json
                if all(v.lower() not in unwanted for v in item.values() if isinstance(v, str))
]

                

            return filtered
        return []
            



    def start_bot(self):
        self.run(self.token)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")
        # await self.tree.sync()


    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()
        await self.load_all_cogs()
        return await super().setup_hook()
