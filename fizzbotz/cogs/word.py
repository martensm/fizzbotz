from __future__ import annotations

import pathlib
import random

from discord.ext import commands
from discord.ext.commands import Bot, Context

import aiofiles
import aiofiles.os

_words_path = pathlib.PurePath(__file__).parents[1] / "data/words.txt"


class Word(commands.Cog):
    @commands.command(aliases=["w", "W"])
    async def word(self, ctx: Context) -> None:
        """Get a random word."""
        stat = await aiofiles.os.stat(_words_path)
        file_size = stat.st_size
        random_byte = random.randint(0, file_size)

        async with aiofiles.open(_words_path) as words_file:
            await words_file.seek(random_byte)

            await words_file.readline()
            word = await words_file.readline()

        await ctx.send(word)


def setup(bot: Bot) -> None:
    bot.add_cog(Word())
