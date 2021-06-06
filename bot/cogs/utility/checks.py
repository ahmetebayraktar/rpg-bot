import discord
from pathlib import Path


# Kanalları bot-komut kanalı mı ya da özel mesaj mı diye kontrol eder.
async def check_channel(channel):
    with open(Path("./data/botcommand.0"), "r") as f:
        con = f.readlines()

    if isinstance(channel, discord.DMChannel):
        return False
    elif channel.id in con or con == "" or con == [""]:
        return True
    else:
        return False
