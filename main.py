import discord
from src import AQWVerifier
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    aqw = AQWVerifier(
        token=os.environ['TOKEN'],
        admins={"shell": 1143657502941122580},
        command_prefix="!",
        intents=discord.Intents.all()
    )
    aqw.start_bot()

if __name__ == "__main__":
    main()
