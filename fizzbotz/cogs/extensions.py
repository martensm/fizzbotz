from __future__ import annotations

import discord
from discord.ext import commands


class Extensions(commands.Cog):
    @commands.group(aliases=["ext"], invoke_without_command=True)
    @commands.is_owner()
    async def extension(self, ctx: commands.Context) -> None:
        await ctx.send("\n".join(f"\u2022 {key}" for key in ctx.bot.extensions))

    @extension.command(aliases=["l", "L"])
    @commands.is_owner()
    async def load(self, ctx: commands.Context, extension: str) -> None:
        was_loaded = False
        if f"fizzbotz.cogs.{extension}" in ctx.bot.extensions:
            was_loaded = True

        ctx.bot.unload_extension(f"fizzbotz.cogs.{extension}")
        try:
            ctx.bot.load_extension(f"fizzbotz.cogs.{extension}")
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
    async def unload(self, ctx: commands.Context, extension: str) -> None:
        if f"fizzbotz.cogs.{extension}" not in ctx.bot.extensions:
            await ctx.send(f"Extension `{extension}` is not loaded")
            return

        ctx.bot.unload_extension(f"fizzbotz.cogs.{extension}")

        if f"fizzbotz.cogs.{extension}" not in ctx.bot.extensions:
            await ctx.send(f"Unloaded extension `{extension}`")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Extensions())
