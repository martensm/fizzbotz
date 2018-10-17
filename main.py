import asyncio
import contextlib
import logging
from logging.handlers import RotatingFileHandler
from typing import Generator

from fizzbotz import FizzBotz

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


@contextlib.contextmanager
def setup_logging() -> Generator[None, None, None]:
    logging.getLogger("discord").setLevel(logging.INFO)
    logging.getLogger("discord.http").setLevel(logging.WARNING)

    log = logging.getLogger()

    try:
        log.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            filename="fizzbotz.log",
            mode="w",
            maxBytes=5 * 1024 * 1024,
            encoding="utf-8",
        )
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter(
            "[{asctime}] [{levelname:<7}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        handlers = log.handlers[:]
        for handler in handlers:
            handler.close()
            log.removeHandler(handler)


with setup_logging():
    FizzBotz().launch()
