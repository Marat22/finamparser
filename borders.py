import os
import shutil
import urllib
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from os.path import exists
from request import make_request


def make_ends_of_borders_list(borders_path: Path) -> dict[datetime.date, datetime.date]:
    ends_of_futures = {}
    with borders_path.open("r") as borders:
        # next(borders)
        borders = borders.readlines()
        for border_index in range(1, len(borders)-1):
            end_of_future = (datetime.strptime(borders[border_index].split(";")[-2], "%Y-%m-%d")).date()

            start_of_next_future = (datetime.strptime(borders[border_index+1].split(";")[-2], "%Y-%m-%d")).date()

            ends_of_futures[start_of_next_future] = end_of_future
    return ends_of_futures

def closest_end_of_future(now_date: datetime.date,
                          ends_of_futures: dict[datetime.date, datetime.date]) -> datetime.date:
    keys = ends_of_futures.keys()
    difference = timedelta(days=10 ** 5)
    closest_end = datetime(year=1000, month=10, day=10)
    for key in keys:
        if (difference >
                (ends_of_futures[key]
                 - now_date)
                > timedelta(days=0)):
            difference = key - now_date
            closest_end = key

    # return min(items, key=lambda x: abs(x - pivot))

    return closest_end

