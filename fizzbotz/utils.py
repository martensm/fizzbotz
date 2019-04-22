from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, Generic, Optional, TypeVar

Item = TypeVar("Item")


class AsyncBuffer(Generic[Item]):
    def __init__(
        self,
        get_item: Callable[[], Awaitable[Item]],
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        maxsize: int = 20
    ) -> None:
        self._get_item = get_item
        self._loop = loop if loop is not None else asyncio.get_event_loop()

        self._q = asyncio.Queue(maxsize=maxsize)
        self._task = None

    def empty(self) -> bool:
        return self._q.empty()

    def full(self) -> bool:
        return self._q.full()

    async def get(self) -> Awaitable[Item]:
        return await self._q.get()

    def get_nowait(self) -> Item:
        return self._q.get_nowait()

    def qsize(self) -> int:
        return self._q.qsize()

    def fill(self) -> AsyncBuffer:
        self.stop_fill()
        self._task = self._loop.create_task(self._fill_task())
        return self

    def stop_fill(self) -> AsyncBuffer:
        if self._task:
            self._task.cancel()
            self._task = None
        return self

    async def _fill_task(self) -> None:
        while True:
            item = await self._get_item()
            await self._q.put(item)
