import discord
from discord.ext import commands
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import db

build_num = "0"


class RPGBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        self.scheduler = AsyncIOScheduler()
        super().__init__(
            command_prefix=self.prefix,
            case_insensitive=True,
            intents=discord.Intents.all()
        )

        db.autosave(self.scheduler)

    def setup(self):
        print("Kurulum başlıyor...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" `{cog}` adlı modül yüklendi.")

        print("Kurulum tamamlandı.")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            token = f.read()

        print("Bot çalıştırılıyor...")
        super().run(token, reconnect=True)

    async def shutdown(self):
        print("Discord'a olan bağlantı kapatılıyor...")
        await super().close()

    async def close(self):
        print("Terminalden kapanıyor...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Discord'a bağlantı kuruldu. (gecikme: {self.latency * 1000:,.0f} ms).")

    @staticmethod
    async def on_resumed():
        print("Bot bağlantısı devam ettirildi.")

    @staticmethod
    async def on_disconnect():
        print("Bot bağlantısı kapatıldı.")

    # noinspection PyAttributeOutsideInit
    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print(f"Bot hazır. Sürüm: {build_num}")
        print(f"RPG BOT HAZIR!")

    @staticmethod
    async def prefix(bot, msg):
        return commands.when_mentioned_or(">")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="HATA",
                description=f"Bu komut şu an beklemede.",
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(exception, commands.MissingPermissions):
            embed = discord.Embed(
                title="HATA",
                description=f"Bu eylemi yapmaya izniniz yok.",
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="HATA",
                description=f"Gerekli komut parametresi boş bırakıldı.",
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(exception, commands.UserNotFound):
            embed = discord.Embed(
                title="HATA",
                description=f"Böyle bir kullanıcı bulunulamadı.",
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(exception, commands.MemberNotFound):
            embed = discord.Embed(
                title="HATA",
                description=f"Böyle bir üye bulunulamadı.",
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(exception, commands.CommandNotFound):
            embed = discord.Embed(
                title="HATA",
                description=f"Böyle bir komut bulunulamadı.",
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(exception, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="HATA",
                description=f"Botun yetkisi buna yetmiyor.",
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed, delete_after=5)
        else:
            pass
