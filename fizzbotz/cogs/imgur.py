from __future__ import annotations

import asyncio
import imghdr
import io
import random
import string

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType, Context

import aiohttp

image_queue = asyncio.Queue(maxsize=20)

base_url = "https://i.imgur.com/"
valid_characters = string.ascii_letters + string.digits
id_length = 5


async def fill_queue():
    while True:
        image_id = "".join(random.choice(valid_characters) for _ in range(id_length))
        base_image_url = f"{base_url}{image_id}"
        query_url = f"{base_image_url}.png"

        async with aiohttp.ClientSession() as session:
            async with session.get(query_url) as r:
                if str(r.url) != f"{base_url}removed.png":
                    ext = imghdr.what(io.BytesIO(await r.read())) or "png"
                    image_url = f"{base_image_url}.{ext}"

                    await image_queue.put(image_url)


embed_bg_color = discord.Color.from_rgb(54, 57, 63)


class Imgur(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        bot.loop.create_task(fill_queue())

    @commands.is_nsfw()
    @commands.cooldown(1, 1, type=BucketType.member)
    @commands.command(aliases=["i", "I", "¡"])
    async def imgur(self, ctx: Context) -> None:
        "Get a random image from Imgur. Only works in NSFW channels."
        image_url = await image_queue.get()

        author = ctx.author
        image_embed = (
            discord.Embed(
                color=embed_bg_color, title=":frame_photo: | Here is your Imgur image:"
            )
            .set_author(name=author.display_name, icon_url=author.avatar_url)
            .set_image(url=image_url)
        )

        try:
            await ctx.send(embed=image_embed)
        except discord.Forbidden:
            await ctx.send(image_url)


def setup(bot) -> None:
    bot.add_cog(Imgur(bot))
