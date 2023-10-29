#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Add logging support


import argparse
from typing import Tuple, NamedTuple
import psutil
import time


BYTES_TO_MB_DIVIDER = 1024 ** 2
SLEEP_INTERVAL_SECONDS = 2


class Proc(NamedTuple):
    name: str
    memory_usage: int

# helper functions
def get_memory_usage_percent() -> int:
    return int(psutil.virtual_memory().percent)

def get_total_system_memory_mb() -> int:
    return psutil.virtual_memory().total // BYTES_TO_MB_DIVIDER



def parse_args() -> Tuple[int, int]:
    total_memory = get_total_system_memory_mb()
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
    args = parser.parse_args()
    return args.total, args.proc



def main() -> None:
    total_usage_percent, per_proc_usage_mb = parse_args()
    while True:
        current_mem_usage_percent = get_memory_usage_percent()
        if current_mem_usage_percent >= total_usage_percent:
            print("ALARM: Total nemory usage:", current_mem_usage_percent)

        if per_proc_usage_mb:
            fat_processes = []
            for proc in psutil.process_iter():
                try:
                    name = proc.name()
                    usage_mb = proc.memory_info().rss // BYTES_TO_MB_DIVIDER
                    if usage_mb >= per_proc_usage_mb:
                        fat_processes.append(
                            Proc(name, usage_mb)
                        )
                except (psutil.NoSuchProcess):
                    pass
                    # TODO: log no process exception
                except (psutil.AccessDenied):
                    pass
                    # TODO: log access denied exception
            for proc in fat_processes:
                print(f"ALARM: {proc.name} uses {proc.memory_usage} MB")

        
        time.sleep(SLEEP_INTERVAL_SECONDS)



if __name__ == "__main__":
    main()