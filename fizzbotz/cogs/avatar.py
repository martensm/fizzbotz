from __future__ import annotations

import discord
from discord.ext import commands

_embed_bg_color = discord.Color.from_rgb(54, 57, 63)


class Avatar(commands.Cog):
    @commands.command(aliases=["a", "A"])
    async def avatar(
        self, ctx: commands.Context, member: discord.Member = None
    ) -> None:
        """Get another member's or your own avatar."""
        if member is None:
            avatar_url = ctx.author.avatar_url
        else:
            avatar_url = member.avatar_url

        avatar_embed = discord.Embed(color=_embed_bg_color).set_image(url=avatar_url)
        await ctx.send(embed=avatar_embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Avatar())
