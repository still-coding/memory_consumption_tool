import asyncio
import psutil

from typing import Optional, List, NamedTuple

from .logger import logger


class ProcessInfo(NamedTuple):
    name: str
    memory_usage: int


class MemoryWatcher:
    BYTES_TO_MB_DIVIDER = 1024 ** 2

    def __init__(self, per_process_limit_mb: Optional[int]=None) -> None:
        self.per_process_limit_mb = per_process_limit_mb


    @classmethod
    def __get_memory_usage_percent(cls) -> int:    
        return int(psutil.virtual_memory().percent)

    @classmethod
    async def get_memory_usage_percent(cls):
        return await asyncio.to_thread(cls.__get_memory_usage_percent)

    @classmethod
    def get_total_system_memory_mb(cls) -> int:
        return psutil.virtual_memory().total // cls.BYTES_TO_MB_DIVIDER


    def __get_fat_processes(self) -> List[ProcessInfo]:
        fat_processes = []
        if not self.per_process_limit_mb:
            return fat_processes
        for proc in psutil.process_iter():
            try:
                name = proc.name()
                usage_mb = proc.memory_info().rss // self.__class__.BYTES_TO_MB_DIVIDER
                if usage_mb >= self.per_process_limit_mb:
                    fat_processes.append(
                        ProcessInfo(name=name, memory_usage=usage_mb)
                    )
            except (psutil.NoSuchProcess) as excn:
                logger.error(f"Failed to find process {proc}. Details: {excn}")
            except (psutil.AccessDenied) as exca:
                logger.error(f"Failed to access process {proc}. Details: {exca}")
        return fat_processes

    async def get_fat_processes(self):
        return await asyncio.to_thread(self.__get_fat_processes)
