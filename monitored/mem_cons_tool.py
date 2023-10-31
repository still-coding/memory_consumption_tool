#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import asyncio
from typing import Tuple
from time import time

from mem_cons_tool.alarmist import Alarmist
from mem_cons_tool.config import settings
from mem_cons_tool.logger import logger
from mem_cons_tool.memory_watcher import MemoryWatcher


def parse_args() -> Tuple[int, int, bool]:
    total_memory = MemoryWatcher.get_total_system_memory_mb()
    parser = argparse.ArgumentParser(
        prog="mem_cons_tool.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Memory consumption analyzer tool.\nSends alarms to REST API in cases of:\
            \n - Excessive total mem usage\n - Excessive mem usage by process",
    )
    parser.add_argument(
        "-t",
        "--total",
        type=int,
        metavar="[1-100]",
        choices=range(1, 101),
        help="Total memory usage limit, %%",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--proc",
        type=int,
        metavar=f"[1 - {total_memory}]",
        choices=range(1, total_memory),
        help="Memory usage limit by single process, Mb",
    )
    parser.add_argument(
        "-l",
        "--loop",
        help=f"If present, makes tool run in loop every {settings.alarm_interval_seconds} sec.",
        action="store_true",
    )
    args = parser.parse_args()
    return args.total, args.proc, args.loop


async def main() -> None:
    total, per_proc, loop = parse_args()

    mem_watcher = MemoryWatcher(per_process_limit_mb=per_proc)
    alarmist = Alarmist()

    while True:
        current_mem_usage = await MemoryWatcher.get_memory_usage_percent()

        if current_mem_usage >= total:
            await alarmist.send_alarm(
                timestamp=time(),
                message="Total memory usage, %",
                value=current_mem_usage
            )
            logger.warning(f"Alarm - Total memory usage: {current_mem_usage}%")

        if per_proc:
            for proc in await mem_watcher.get_fat_processes():
                await alarmist.send_alarm(
                    timestamp=time(),
                    message=f"Process {proc.name} memory usage, Mb",
                    value=proc.memory_usage
                )
                logger.warning(f"Alarm - Process {proc.name} memory usage: {proc.memory_usage} Mb")

        if not loop:
            break

        await asyncio.sleep(settings.alarm_interval_seconds)


if __name__ == "__main__":
    asyncio.run(main())
