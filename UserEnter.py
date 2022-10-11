from datetime import date
from pathlib import Path

import parser

# FILE FORMATS FOR NOT TICKS
# 1 TICKER PER DATE TIME OPEN HIGH LOW CLOSE VOL
# 2 TICKER PER DATE TIME OPEN HIGH LOW CLOSE
# 3 TICKER PER DATE TIME CLOSE VOL
# 4 TICKER PER DATE TIME CLOSE
# 5 DATE TIME OPEN HIGH LOW CLOSE VOL
# 6 DATE TIME LAST VOL ID OPER

# FILE FORMATS FOR TICKS
# 7 TICKER, DATE, TIME, LAST, VOL
# 8 TICKER, DATE, TIME, LAST
# 9 DATE, TIME, LAST, VOL
# 10 DATE, TIME, LAST
# 11 DATE, TIME, LAST, VOL, ID
# 12 DATE, TIME, LAST, VOL, ID, OPER

# TIMEFRAME CODES
# 'tick': 1, 'min': 2, '5min': 3, '10min': 4, '15min': 5, '30min': 6, 'hour': 7, 'daily': 8, 'week': 9, 'month': 10

# a = {"x": 1, "y": 2,}
#
# def f(x, y, z):
#     print(x * y + z)
#
# f(**a, 7)


parser.take_files_from_finam(start_time=date(year=2022, month=10, day=3), end_time=date(year=2022, month=10, day=7),
                             daily=True,
                             market='14', em='17455',
                             contract_name='spfb.rts',  # (code)
                             time_frame=1,
                             borders=Path(r"C:\programs\python\mathclub\parser\boards\90futures_RTS.csv"),
                             result_folder=Path(r"C:\Users\Home\Desktop\test"),
                             separator=",",
                             extension='.csv',
                             form=12)

