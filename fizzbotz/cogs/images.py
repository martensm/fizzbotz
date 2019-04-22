from __future__ import annotations

import imghdr
import io
import random
import string

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType, Context

import aiohttp

from ..utils import AsyncBuffer

embed_bg_color = discord.Color.from_rgb(54, 57, 63)


def _get_imgur_url(id_length) -> str:
    base_url = "https://i.imgur.com/"
    valid_characters = string.ascii_letters + string.digits

    async def generate_imgur_url():
        async with aiohttp.ClientSession() as session:
            while True:
                image_id = "".join(
                    random.choice(valid_characters) for _ in range(id_length)
                )

                base_image_url = f"{base_url}{image_id}"
                query_url = f"{base_image_url}.png"

                async with session.get(query_url) as r:
                    if str(r.url) != f"{base_url}removed.png":
                        ext = imghdr.what(io.BytesIO(await r.read())) or "png"
                        return f"{base_image_url}.{ext}"

    return generate_imgur_url


def _get_inspirobot_url() -> str:
    url = "https://inspirobot.me/api?generate=true"

    async def generate_inspirobot_url():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                return await r.text()

    return generate_inspirobot_url


async def _send_embed(ctx: Context, title: str, url: str) -> None:
    author = ctx.author
    image_embed = (
        discord.Embed(
            color=embed_bg_color, title=f":frame_photo: | Here is your {title} image:"
        )
        .set_author(name=author.display_name, icon_url=author.avatar_url)
        .set_image(url=url)
    )

    try:
        await ctx.send(embed=image_embed)
    except discord.Forbidden:
        await ctx.send(url)


class Images(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.imgur_buffers = [
            AsyncBuffer(_get_imgur_url(7), loop=bot.loop, maxsize=1000).fill(),
            AsyncBuffer(_get_imgur_url(5), loop=bot.loop).fill(),
        ]
        self.inspirobot_buffer = AsyncBuffer(
            _get_inspirobot_url(), loop=bot.loop
        ).fill()

    @commands.is_nsfw()
    @commands.cooldown(1, 3, type=BucketType.member)
    @commands.command(aliases=["i", "I"])
    async def imgur(self, ctx: Context) -> None:
        "Get a random image from Imgur. Only works in NSFW channels."
        if self.imgur_buffers[0].empty():
            image_url = await self.imgur_buffers[1].get()
        else:
            image_url = await self.imgur_buffers[0].get()

        await _send_embed(ctx, "Imgur", image_url)

    @commands.cooldown(1, 3, type=BucketType.member)
    @commands.command(aliases=["ib", "IB"])
    async def inspirobot(self, ctx: Context) -> None:
        "Get a random image from InspiroBot."
        image_url = await self.inspirobot_buffer.get()

        await _send_embed(ctx, "InspiroBot", image_url)


def setup(bot: Bot) -> None:
    bot.add_cog(Images(bot))
