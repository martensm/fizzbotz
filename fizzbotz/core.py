from __future__ import annotations

import io
import traceback
from typing import List, Optional, Union

import discord
from discord.ext import commands

from .environments import DEBUG, DEBUG_TOKEN, DESCRIPTION, PREFIX, STATUS, TOKEN
from .log import logger

_initial_extensions = (
    "fizzbotz.cogs.admin",
    "fizzbotz.cogs.avatar",
    "fizzbotz.cogs.eightball",
    "fizzbotz.cogs.extensions",
    "fizzbotz.cogs.images",
    "fizzbotz.cogs.word",
)


class FizzBotz(commands.Bot):
    def __init__(
        self,
        token: Optional[str] = None,
        command_prefix: Optional[Union[List[str], str]] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        command_prefix = PREFIX if command_prefix is None else command_prefix
        description = DESCRIPTION if description is None else description

        if DEBUG:
            token = DEBUG_TOKEN if token is None else token
        else:
            token = TOKEN if token is None else token
        assert token is not None
        self.token = token

        self.status = STATUS if status is None else status

        super().__init__(
            command_prefix=command_prefix,
            description=description,
            pm_help=None,
            help_attrs=dict(hidden=True),
        )

        for extension in _initial_extensions:
            try:
                self.load_extension(extension)
            except (discord.ClientException, ImportError):
                logger.exception(f"Failed to load extension {extension}.")

    async def on_ready(self) -> None:
        activity = discord.Game(name=self.status)
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx: Context, error: Exception) -> None:
        if isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                tb = io.StringIO()
                traceback.print_tb(original.__traceback__, None, tb)
                logger.error(
                    f'Exception raised from command "{ctx.command.qualified_name}":'
                    f"\n{tb.getvalue().rstrip()}"
                )

                logger.error(f"{original.__class__.__name__}: {original}")
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    def launch(self) -> None:
        super().run(self.token)


__all__ = ("FizzBotz",)
