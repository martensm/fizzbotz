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


class ImgurBuffer:
    _base_url = "https://i.imgur.com/"
    _valid_characters = string.ascii_letters + string.digits

    def __init__(self, maxsize=20, *, loop=None, id_length: int) -> None:
        self._id_length = id_length
        self._q = asyncio.Queue(maxsize=maxsize)
        self._task = None
        self._loop = loop

    async def _generate_image_url(self) -> str:
        async with aiohttp.ClientSession() as session:
            while True:
                image_id = "".join(
                    random.choice(self._valid_characters)
                    for _ in range(self._id_length)
                )

                base_image_url = f"{self._base_url}{image_id}"
                query_url = f"{base_image_url}.png"

                async with session.get(query_url) as r:
                    if str(r.url) != f"{self._base_url}removed.png":
                        ext = imghdr.what(io.BytesIO(await r.read())) or "png"
                        return f"{base_image_url}.{ext}"

    async def _put(self, item) -> None:
        await self._q.put(item)

    async def _fill_task(self) -> None:
        while True:
            image_url = await self._generate_image_url()
            await self._put(image_url)

    def empty(self) -> bool:
        return self._q.empty()

    async def get(self) -> str:
        return await self._q.get()

    def fill(self) -> ImgurBuffer:
        self.stop_fill()
        self._task = self._loop.create_task(self._fill_task())
        return self

    def stop_fill(self) -> ImgurBuffer:
        if self._task:
            self._task.cancel()
            self._task = None
        return self


embed_bg_color = discord.Color.from_rgb(54, 57, 63)


class Imgur(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.buffers = [
            ImgurBuffer(1000, loop=bot.loop, id_length=7).fill(),
            ImgurBuffer(loop=bot.loop, id_length=5).fill(),
        ]

    @commands.is_nsfw()
    @commands.cooldown(1, 3, type=BucketType.member)
    @commands.command(aliases=["i", "I", "¡"])
    async def imgur(self, ctx: Context) -> None:
        "Get a random image from Imgur. Only works in NSFW channels."
        if self.buffers[0].empty():
            image_url = await self.buffers[1].get()
        else:
            image_url = await self.buffers[0].get()

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


def setup(bot: Bot) -> None:
    bot.add_cog(Imgur(bot))
