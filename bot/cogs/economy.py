import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utility import currency as curr


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(curr.change_all_money(100), CronTrigger(hour=12, minute=0, second=0))
        self.scheduler.start()


def setup(bot):
    bot.add_cog(Economy(bot))
