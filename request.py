from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import urllib

def make_request(start_time: datetime.date, end_time: datetime.date,
                 contract_name: str,
                 market: str, em: str,  # em  это цифровой символ, который соответствует бумаге
                 time_frame: int,
                 separator: int,
                 extension: str,
                 form: int) -> Request:
    url = make_url(end_time=end_time, start_time=start_time, market=market,
                   contract_name=contract_name, em=em, separator=separator,
                   extension=extension, form=form, time_frame=time_frame)

    return Request(url=url,
                   headers={'User-Agent': 'Mozilla/5.0'})

def make_url(start_time: datetime.date, end_time: datetime.date,
             contract_name: str,
             market: str, em: str,  # em  это цифровой символ, который соответствует бумаге
             time_frame: int,
             separator: int,
             extension: str,
             form: int) -> str:
    # url = "http://export.finam.ru/spfb.rts_130101_171231.txt?market=14&em=17455&code=spfb.rts&apply=0&df=1&mf=0&yf" \
    #       "=2013&from=01.01.2013&dt=31&mt=11&yt=2017&to=31.12.2017&p=1&f=spfb.rts_130101_171231&e=.csv&cn=spfb.rts" \
    #       "&dtf=1&tmf=1&msor=0&mstime=on&mstimever=1&separator=1&separator2=1&datf=6&at=1"
    params = {
        'market': market,
        'em': em,
        'code': contract_name,
        'df': str(start_time.day),
        'mf': str(start_time.month - 1),
        'yf': str(start_time.year),
        'from': str(start_time.day).zfill(2) + str('.') + str(start_time.month).zfill(2) + str(
            '.') + str(start_time.year),
        'dt': str(end_time.day),
        'mt': str(end_time.month - 1),
        'yt': str(end_time.year),
        'to': str(end_time.day).zfill(2) + str('.') + str(start_time.month).zfill(2) + str('.') + str(
            start_time.year),
        'p': str(time_frame),
        'f': "filename",
        'e': extension,
        'cn': contract_name,
        'dtf': 1,
        'tmf': 1,
        'msor': 0,
        'mstime': 'on',
        'mstimever': 1,
        'sep': separator,
        'sep2': 1,
        'datf': form,
        'at': 1
    }
    params = urllib.parse.urlencode(params)  # datetime.strptime(start, '%d.%m.%Y').strftime('%Y%m%d')
    start_time_rev: str = start_time.strftime("%y%m%d")
    end_time_rev: str = end_time.strftime("%y%m%d")
    before_params = "http://export.finam.ru/" + contract_name + "_" + start_time_rev + "_" + end_time_rev + extension
    return fr"http://export.finam.ru/{before_params}.txt?{params}"