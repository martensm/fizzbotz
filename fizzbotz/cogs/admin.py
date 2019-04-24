from __future__ import annotations

import discord
from discord.ext import commands


class Admin(commands.Cog):
    @commands.has_permissions(manage_channels=True)
    @commands.command(aliases=["vk"])
    async def voicekick(self, ctx: commands.Context, member: discord.Member) -> None:
        """Kick a member from voice."""
        voice_channel = await ctx.guild.create_voice_channel("rip")
        await member.move_to(voice_channel)
        await voice_channel.delete()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Admin())
