import asyncio

from src.dao.counter import get_counter_range, update_counter


class Counter:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def current_position(self):
        return self.__current_position

    async def initiate(self):
        async with self._lock:
            range_response = await get_counter_range()
            self.__starts_from = range_response["starts_from"]
            self.__end_to = range_response["ends_at"]
            self.__current_position = self.__starts_from
            self.__ref_id = range_response["ref_id"]
            print("counter initialized at", self.__starts_from, "to", self.__end_to)

    async def commit(self):
        async with self._lock:
            await update_counter(
                ref_id=self.__ref_id, last_commits_at=self.current_position
            )

    async def get_next(self) -> int:
        async with self._lock:
            if self.current_position < self.__end_to:
                self.__current_position += 1
            else:
                # reinitialize counter with new range
                await self.commit()
                await self.initiate()
            return self.__current_position


async def initiate_counter():
    counter = Counter()
    await counter.initiate()


async def commit_counter():
    counter = Counter()
    await counter.commit()
