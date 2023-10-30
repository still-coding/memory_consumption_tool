from typing import Optional, List, Tuple, NamedTuple
import psutil
from logger import logger

class ProcessInfo(NamedTuple):
    name: str
    memory_usage: int


class MemoryAnalyzer:
    BYTES_TO_MB_DIVIDER = 1024 ** 2

    def __init__(self, total_limit_percent: int, per_process_limit_mb: Optional[int]=None) -> None:
        self.total_limit_percent = total_limit_percent
        self.per_process_limit_mb = per_process_limit_mb



    @staticmethod
    def get_memory_usage_percent() -> int:
        return int(psutil.virtual_memory().percent)

    @classmethod
    def get_total_system_memory_mb(cls) -> int:
        return psutil.virtual_memory().total // cls.BYTES_TO_MB_DIVIDER


    def get_fat_processes(self) -> List[ProcessInfo]:
        fat_processes = []
        for proc in psutil.process_iter():
            try:
                name = proc.name()
                usage_mb = proc.memory_info().rss // self.__class__.BYTES_TO_MB_DIVIDER
                if usage_mb >= self.per_process_limit_mb:
                    fat_processes.append(
                        ProcessInfo(name=name, memory_usage=usage_mb)
                    )
            except (psutil.NoSuchProcess) as exc:
                logger.error(f"Failed to find process {name}. Details: {exc.msg}")
            except (psutil.AccessDenied):
                logger.error(f"Failed to access process {name}. Details: {exc.msg}")
            except (psutil.ZombieProcess):
                logger.error(f"Process {name} is zombie. Details: {exc.msg}")
        return fat_processes
