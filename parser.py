import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen
from os.path import exists


import typing

from request import make_request
from borders import make_ends_of_borders_list
from make_file import make_file


class TimeError(Exception):
    """raised when start_time is bigger than end_time"""
    pass


class ExtensionError(Exception):
    """raised when impossible extension is entered(It can be either '.csv' either '.txt')"""
    pass


class SeparatorError(Exception):
    """raised when impossible separator is entered"""
    pass


class FormError(Exception):
    pass


def check_for_errors(start_time: datetime.date, end_time: datetime.date, extension: str, separator: str,
                     timeframe: int, form: int) -> None:
    if start_time > end_time:
        raise TimeError("start_time is bigger than end_time")
    if extension != '.csv' and extension != '.txt':
        raise ExtensionError("impossible extension is entered(It can be either '.csv' either '.txt')")
    if separator != ',' and separator != ';':
        raise SeparatorError(f"impossible separator is entered(It can be either ',' either ';'). Not \"{separator}\"")
    if type(form) != int:
        raise TypeError("form type should be int")
    elif 13 <= form or form <= 0:
        raise FormError("Form can equal only 1-12")
    elif timeframe != 1 and (7 <= form or form <= 0):
        raise FormError("If timeframe is not 1(ticks) form can equal only 1-6")
    elif timeframe == 1 and (13 <= form or form <= 6):
        raise FormError("If timeframe is 1(ticks) form can equal only 7-12")


def separator_reformat(separator: str) -> dict[str, typing.Union[int, str]]:
    if separator == ',':
        return {"int": 1, "str": ","}
    elif separator == '.':
        return {"int": 2, "str": "."}
    elif separator == ';':
        return {"int": 3, "str": ";"}
    elif separator == ' ':
        return {"int": 4, "str": " "}


def get_date_from_file(form: int, line: str, separator: str) -> datetime.date:
    """gets date from needed line"""
    if form <= 4:
        return (datetime.strptime(line.split(separator)[2], f"%Y%m%d")).date()
    elif form == 5 or form == 6 or form >= 9:
        return (datetime.strptime(line.split(separator)[0], f"%Y%m%d")).date()
    elif form == 7 or form == 8:
        return (datetime.strptime(line.split(separator)[1], f"%Y%m%d")).date()

def make_or_clear_result_folder(result_folder: Path) -> None:
    if exists(result_folder):
        all_files = os.listdir(result_folder)
        for f in all_files:
            os.remove(str(result_folder) + "\\" + f)

        result_folder.mkdir(parents=True, exist_ok=True)
    else:
        result_folder.mkdir(parents=True, exist_ok=True)


def make_ticks_file(date: datetime.date, market: str, em: str, time_frame: int, form: int,
                    contract_name: str, extension: str, daily: bool, result_folder: Path,
                    separator: dict[str, typing.Union[int, str]], borders: Path) -> None:
    request = make_request(end_time=date, start_time=date, market=market,
                           contract_name=contract_name, em=em, separator=separator["int"],
                           extension=extension, time_frame=time_frame, form=form)
    if borders is None:
        ends_of_futures = None
    else:
        ends_of_futures = make_ends_of_borders_list(borders_path=borders)

    with urlopen(request) as f:

        file_content = f.read().decode().replace("\r", "")
        lines = file_content.split("\n")

        if lines != [""]:
            day = get_date_from_file(line=lines[1], form=form, separator=separator["str"])

            make_file(start_time=day, file_content=file_content, now_date=day, separator=separator["int"],
                      contract_name=contract_name, extension=extension, ends_of_futures=ends_of_futures,
                      daily=daily, result_folder=result_folder, closing_by_end_of_future=False)
        else:
            print(f"On {date} there were no trades")


def make_files_for_not_ticks(form: int, daily: bool, f: any, ends_of_futures: dict[datetime.date, datetime.date],
                             entered_params: dict[str, typing.Union[str, int]],
                             separator: dict[str, typing.Union[int, str]], borders: Path):
    """if not ticks runs through the file and writes information from it into the file(-s) in the needed folder"""
    first_string = (next(f)).decode().replace("\r", "")
    file = f.read().decode().replace("\r", "").split("\n")
    file_content: str = first_string
    start_file_date = get_date_from_file(line=file[1], form=form, separator=separator["str"])
    for line_index in range(0, len(file) - 1):
        line = file[line_index]
        now_date = get_date_from_file(form=form, line=line, separator=separator["str"])
        fixed_params = {
            "now_date": now_date,
            "ends_of_futures": ends_of_futures,
        }
        fixed_params.update(entered_params)
        if borders is not None and now_date in ends_of_futures.keys() and daily is False:
            start_file_date = get_date_from_file(form=form, line=file_content.split("\n")[1],
                                                 separator=separator["str"])
            make_file(True, file_content, start_file_date, **fixed_params)

            del ends_of_futures[now_date]

        elif line_index == len(file) - 2 or (daily and file_content != first_string
                                             and get_date_from_file(form=form, line=file[line_index + 1],
                                                                    separator=separator["str"]) != now_date):
            if line_index != len(file) - 2:
                start_file_date = get_date_from_file(form=form, line=file_content.split("\n")[1],
                                                     separator=separator["str"])
            file_content += f"{line}\n"
            make_file(False, file_content, start_file_date, **fixed_params)

            file_content = first_string
        else:
            file_content += f"{line}\n"


def take_files_from_finam(start_time: datetime.date, end_time: datetime.date, daily: bool,
                          market: str, em: str,  # em это цифровой символ, который соответствует бумаге
                          contract_name: str, time_frame: int, result_folder: Path, separator: str,
                          extension: str, form: int, borders: Path = None) -> None:
    """the main function that sorts in needed way data parsed from Finam and then saves this data in files"""
    check_for_errors(start_time, end_time, extension, separator, time_frame, form)

    make_or_clear_result_folder(result_folder=result_folder)

    separator = separator_reformat(separator)
    entered_params = {
        "contract_name": contract_name, "extension": extension, "daily": daily,
        "result_folder": result_folder, "separator": separator
    }

    if time_frame == 1:
        date = start_time
        while end_time >= date:
            make_ticks_file(date=date, market=market, em=em, time_frame=time_frame, form=form,
                            borders=borders, **entered_params)
            date += timedelta(1)

    else:

        if borders is None:
            ends_of_futures = None
        else:
            ends_of_futures = make_ends_of_borders_list(borders_path=borders)

        request = make_request(end_time=end_time, start_time=start_time, market=market,
                               contract_name=contract_name, em=em, separator=separator["int"],
                               extension=extension, time_frame=time_frame, form=form)

        with urlopen(request) as f:
            make_files_for_not_ticks(form=form, daily=daily, f=f, ends_of_futures=ends_of_futures,
                                     entered_params=entered_params, separator=separator, borders=borders)
