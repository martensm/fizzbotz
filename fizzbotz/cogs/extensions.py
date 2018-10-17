import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context


class Manage:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.group(aliases=["ext"], invoke_without_command=True)
    @commands.is_owner()
    async def extension(self, ctx: Context) -> None:
        await ctx.send("\n".join(f"\u2022 {key}" for key in self.bot.extensions))

    @extension.command(aliases=["l", "L"])
    @commands.is_owner()
    async def load(self, ctx: Context, extension: str) -> None:
        was_loaded = False
        if f"fizzbotz.cogs.{extension}" in self.bot.extensions:
            was_loaded = True

        self.bot.unload_extension(f"fizzbotz.cogs.{extension}")
        try:
            self.bot.load_extension(f"fizzbotz.cogs.{extension}")
            if was_loaded:
                await ctx.send(f"Reloaded extension `{extension}`")
            else:
                await ctx.send(f"Loaded extension `{extension}`")
        except (discord.ClientException, ImportError):
            if was_loaded:
                await ctx.send(f"Failed to reload extension `{extension}`")
            else:
                await ctx.send(f"Failed to load extension `{extension}`")

    @extension.command(aliases=["u", "U"])
    @commands.is_owner()
    async def unload(self, ctx: Context, extension: str) -> None:
        if f"fizzbotz.cogs.{extension}" not in self.bot.extensions:
            await ctx.send(f"Extension `{extension}` is not loaded")
            return

        self.bot.unload_extension(f"fizzbotz.cogs.{extension}")

        if f"fizzbotz.cogs.{extension}" not in self.bot.extensions:
            await ctx.send(f"Unloaded extension `{extension}`")


def setup(bot: Bot) -> None:
    bot.add_cog(Manage(bot))
