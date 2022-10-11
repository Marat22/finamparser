import datetime
import os
from pathlib import Path
from typing import Optional

from borders import make_ends_of_borders_list, closest_end_of_future


def make_filename(start_time: datetime.date, end_time: datetime.date, contract_name: str,
                  extension: str, end_of_futures: Optional[datetime.date]) -> str:
    if end_of_futures is None:
        return rf"{contract_name}_{start_time.strftime('%y%m%d')}_{end_time.strftime('%y%m%d')}{extension}"
    else:
        return rf"{contract_name}{end_of_futures.year}.{end_of_futures.month}_{start_time.strftime('%y%m%d')}_" \
               rf"{end_time.strftime('%y%m%d')}{extension}"


def make_file(closing_by_end_of_future: bool, file_content: str, start_time: datetime.date,now_date: datetime.date,
              contract_name: str, extension: str,
              daily: bool, result_folder: Path, separator: str,
              ends_of_futures: Optional[dict[datetime.date, datetime.date]]
              ) -> None:
    end_of_future: Optional[datetime.date] = None
    end_time: datetime.date = now_date
    if ends_of_futures is not None:
        if closing_by_end_of_future:
            end_of_future = ends_of_futures[now_date]
            end_time = end_of_future
        else:
            end_of_future = closest_end_of_future(now_date=now_date, ends_of_futures=ends_of_futures)

    file_name = make_filename(
        contract_name=contract_name, extension=extension,
        end_of_futures=end_of_future, start_time=start_time, end_time=end_time)
    result = open(os.path.join(result_folder, file_name), "w+")
    result.write(file_content)
    result.close()
    print(file_name)
