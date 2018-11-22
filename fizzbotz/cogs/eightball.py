from __future__ import annotations

import random

from discord.ext import commands
from discord.ext.commands.context import Context

responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
]


class Eightball:
    @commands.command(aliases=["8", "8ball", "eb", "e", "E"])
    async def eightball(self, ctx: Context) -> None:
        """Get a random answer from an eight ball."""
        index = random.randrange(0, len(responses))
        msg = responses[index]

        if index < 10:
            format_char = "+"
        elif index < 15:
            format_char = " "
        else:
            format_char = "-"

        msg = f"```diff\n{format_char}🎱 | {msg}\n```"

        await ctx.send(msg)


def setup(bot) -> None:
    bot.add_cog(Eightball())
