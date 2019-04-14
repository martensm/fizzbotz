from __future__ import annotations

import logging
import traceback
from typing import List, Optional, Union

import discord
from discord.ext.commands import Bot, CommandInvokeError, Context

from .environments import DEBUG, DEBUG_TOKEN, DESCRIPTION, PREFIX, STATUS, TOKEN

log = logging.getLogger(__name__)
initial_extensions = (
    "fizzbotz.cogs.admin",
    "fizzbotz.cogs.avatar",
    "fizzbotz.cogs.eightball",
    "fizzbotz.cogs.extensions",
    "fizzbotz.cogs.imgur",
    "fizzbotz.cogs.word",
)


class FizzBotz(Bot):
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

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except (discord.ClientException, ImportError):
                log.exception(f"Failed to load extension {extension}.")

    async def on_ready(self) -> None:
        activity = discord.Game(name=self.status)
        await self.change_presence(activity=activity)

    async def on_command_error(self, context: Context, exception: Exception) -> None:
        if isinstance(exception, CommandInvokeError):
            log.error(f"In {context.command.qualified_name}:")
            traceback.print_tb(exception.original.__traceback__)
            log.error(f"{exception.original.__class__.__name__}: {exception.original}")

    def launch(self) -> None:
        super().run(self.token)


__all__ = ("FizzBotz",)
