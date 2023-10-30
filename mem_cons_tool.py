#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from logger import logger
import argparse
from typing import Tuple, NamedTuple
import psutil
import time
import requests
from memory_analyzer import MemoryAnalyzer
from alarmist import Alarmist


ALARM_INTERVAL_SECONDS = 10







def parse_args() -> Tuple[int, int]:
    total_memory = MemoryAnalyzer.get_total_system_memory_mb()
    parser = argparse.ArgumentParser(
        prog="mem_cons_tool.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Memory consumption analyzer tool.\nSends alarms to REST API in cases of:\
            \n - Excessive total mem usage\n - Excessive mem usage by process"
    )
    parser.add_argument(
        "-t", "--total", type=int, metavar='[1-100]',
        choices=range(1,101), help="Total memory usage limit, %%",
        required=True
    )
    parser.add_argument(
        "-p", "--proc", type=int,
        metavar=f"[1 - {total_memory}]",
        choices=range(1, total_memory),
        help="Memory usage limit by single process, Mb",
    )
    # TODO: make choice 1 time or interval
    parser.add_argument(
        "-l", "--loop",
        help=f"If present, makes tool run in loop every {ALARM_INTERVAL_SECONDS}",
        action="store_true"        
    )
    args = parser.parse_args()
    return args.total, args.proc, args.loop







def main() -> None:
    total, per_proc, loop = parse_args()
    
    ma = MemoryAnalyzer(
        total_limit_percent=total,
        per_process_limit_mb=per_proc
    )
    


    while True:
        current_mem_usage = ma.get_memory_usage_percent()
        if current_mem_usage >= total:
            logger.warning(f"Sent alarm - Total nemory usage: {current_mem_usage} %")

        if per_proc:            
            for proc in ma.get_fat_processes():
                logger.warning(f"Sent alarm - {proc.name} uses {proc.memory_usage} MB")

        
        time.sleep(ALARM_INTERVAL_SECONDS)



if __name__ == "__main__":
    main()
