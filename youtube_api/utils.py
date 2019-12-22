"""
    Модуль содержащий функции связанные с youtube_api_v3.py
    
    Преобразование времени (youtube) в секунды:
        ytdate_to_sec('PT1H24S') -> 3624
    Преобразование времени (youtube) в дельту:
        ytdate_to_timedelta('P10DT2H16M36S') -> 10days, 2:16:36
    Сохранение json в файл:
        save_json('myfile.json', content) -> Сохранить json в файл
    Загрузка json из файла:
        obj = load_json('myfile.json') -> Загрузить json из файла
    Загрузка json из url:
        obj = download_json('http://mysite/json') -> Загрузить из сети json
    Разбивка диапазона на периоды:
        parts = date_period_into_parts(datetime.datetime(2019,8,3), datetime.datetime(2019,11,5,12,30), part=5) # на 5 частей
        parts = date_period_into_parts(datetime.datetime(2019,8,3), datetime.datetime(2019,11,5,12,30), part_by='day') # по дням
    Урезание строки
        truncatechars('Длинный текст', 8, onestring=True) -> 'Длинн...'
"""


class DownloadException(Exception):
    def __init__(self, message, response_status, response_url, response_content, response_encoding):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # Now for your custom code...
        self.message = message
        self.response_status = response_status
        self.response_url = response_url
        self.response_content = response_content
        self.response_encoding = response_encoding
    def __str__(self):
        return 'Ошибка получения Json-данных: {}\nSTATUS: {}\nTEXT: {}\nURL: {}\nENCODING: {}'.format(self.message, self.response_status, self.response_content, self.response_url, self.response_encoding)


def ytdate_to_sec(ytdate):
    """ Преобразование времени ролика из Youtube-формата в секунды
        :param ytdate: Время в виде PT2H16M36S
        :return: Количество секунд
        :type ytdate: str
        :rtype: int
        
        Примеры:
        'PT1H24S' -> 3624
        'PT2H16M36S' -> 8196
    """
    import re
    res = 0
    re_days = re.search('(\d+)DT', ytdate)
    days = int(re_days.group(1)) if re_days else 0
    re_hour = re.search('(\d+)H', ytdate)
    hour = int(re_hour.group(1)) if re_hour else 0
    re_min = re.search('(\d+)M', ytdate)
    minute = int(re_min.group(1)) if re_min else 0
    re_sec = re.search('(\d+)S', ytdate)
    sec = int(re_sec.group(1)) if re_sec else 0
    #print(days, hour, minute, sec)
    res = days*24*60*60 + hour*60*60 + minute*60 + sec
    return res
    

def ytdate_to_timedelta(ytdate):
    """ Преобразование времени ролика из Youtube-формата в datetime.timedelta 
        :param ytdate: Время в виде PT2H16M36S
        :return: Время в виде объекта datetime.timedelta
        :type ytdate: str
        :rtype: datetime.timedelta
        
        Примеры:
        'PT1H24S' -> 1:00:24
        'PT2H16M36S' -> 2:16:36
        'P10DT2H16M36S' -> 10days, 2:16:36
    """
    from datetime import timedelta
    sec = ytdate_to_sec(ytdate)
    res = timedelta(seconds=sec)
    return res


def ytdate_to_str(ytdate):
    """ Преобразование времени ролика из Youtube-формата в форматированный текст
        :param ytdate: Время в виде PT2H16M36S
        :return: Время в виде строки: '02:16:36'
        :type ytdate: str
        :rtype: str
        
        Примеры:
        'PT1H24S' -> '01:00:24'
        'PT2H16M36S' -> '02:16:36'
        'P10DT2H16M36S' -> '10d 02:16:36'
    """
    import re

    re_days = re.search('(\d+)DT', ytdate)
    days = int(re_days.group(1)) if re_days else 0
    days_str = ''
    if days>0:
        days_str = f'{days}d '
    re_hour = re.search('(\d+)H', ytdate)
    hour = int(re_hour.group(1)) if re_hour else 0
    re_min = re.search('(\d+)M', ytdate)
    minute = int(re_min.group(1)) if re_min else 0
    re_sec = re.search('(\d+)S', ytdate)
    sec = int(re_sec.group(1)) if re_sec else 0
    res = '{}{:02}:{:02}:{:02}'.format(days_str, hour, minute, sec)
    return res


def save_json(filename, content, format=True, encoding='utf-8'):
    """ Сохранение json данных в файл 
        :param filename: Имя файла
        :param content: Объект с данными которые необходимо записать в файл
        :param format: Форматировать ли текст с json. По умолчанию да, с отступами = 4
        :param encoding: Кодировка файла. По умолчанию utf-8
        :return: True
    """
    import json
    with open(filename, 'w', encoding=encoding) as fw:
        if format:
            json.dump(content, fw, sort_keys=True, ensure_ascii=False, indent=4) 
        else:    
            json.dump(content, fw, sort_keys=True, ensure_ascii=False) 
    return True


def load_json(filename, encoding='utf-8'):
    """ Загрузка json данных из файла
        :param filename: Имя файла
        :param encoding: Кодировка файла. По умолчанию utf-8
        :return: Объект в виде списка или словаря
    """
    import json
    with open(filename, 'r', encoding=encoding) as f:
        return json.load(f)


def download_json(url):
    """ Загрузка json """
    import json.decoder
    import requests
    res = {}
    response = requests.get(url)
    try:
        res = response.json()
    except json.decoder.JSONDecodeError as e:
        raise DownloadException(str(e), response.status_code, response.url, response.text, response.encoding)
    except Exception as e:
        raise e

    return res


def date_period_into_parts(fromdate, todate, partion_by=1): #part=1, part_by=None
    """
    Получить разбивку дат по периодам
    :param fromdate: Дата начала периода
    :param todate:  Дата окончания периода
    :param partion_by: Количество частей на которые необходимо поделить период или
                        деление по дням, месяцам, годам 'year|month|day'
    :return: Список словарей с периодом fromdate, todate
    :type fromdate: datetime.datetime
    :type todate: datetime.datetime
    :rtype: list

    Пример:
        from datetime import datetime as dt
        date_period_into_parts(dt(2019,8,1,10,31), dt(2019,12,4,8,18), partion_by=3) # Разбить период на 3 части
        [{'fromdate': datetime.datetime(2019, 8, 1, 10, 31),      'todate': datetime.datetime(2019, 9, 12, 1, 46, 39)},
         {'fromdate': datetime.datetime(2019, 9, 12, 1, 46, 40),  'todate': datetime.datetime(2019, 10, 23, 17, 2, 19)},
         {'fromdate': datetime.datetime(2019, 10, 23, 17, 2, 20), 'todate': datetime.datetime(2019, 12, 4, 8, 17, 59)}]
        date_period_into_parts(dt(2019, 8, 6, 10, 31), dt(2019, 10, 4, 8, 18), partion_by='month') # Разбить по месяцам
        2019-08-06 10:31:00 - 2019-08-31 23:59:59
        2019-09-01 00:00:00 - 2019-09-30 23:59:59
        2019-10-01 00:00:00 - 2019-10-31 23:59:59
    """

    from datetime import timedelta
    from dateutil.relativedelta import relativedelta
    #assert partion_by in (None, '', 'day', 'month', 'year')
    assert partion_by != 0

    #if type(fromdate) == str:
    #    fromdate = datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #    fromdate = datetime.strptime(fromdate, '%')        #            published += '&publishedAfter={}Z'.format(fromdate.replace(microsecond=0).isoformat(sep='T'))
    #if type(todate) == str:
    #    todate = todate

    #print(fromdate,todate)
    delta_list = []
    if partion_by=='day':
        # Первый день
        fromdate_part_begin = fromdate
        todate_part_begin = min(fromdate + relativedelta(hour=23, minute=59, second=59, microsecond=0), todate)
        delta_list.append({'fromdate':fromdate_part_begin, 'todate':todate_part_begin})
        #print(fromdate_part_begin, '-', todate_part_begin, 'BEGIN')
        delta = todate - fromdate
        days = delta.days if delta.seconds==0 else delta.days+1
        for i in range(1,days-1):
            fromdate_part = fromdate.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=i)
            todate_part = fromdate.replace(hour=23, minute=59, second=59, microsecond=0) + timedelta(days=i)
            delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
        # Последний день
        if delta_list[-1]['todate']  < todate.replace(microsecond=0):
            fromdate_part_end = (todate + relativedelta(hour=0, minute=0, second=0)).replace(microsecond=0)
            todate_part_end = todate.replace(microsecond=0) #+ relativedelta(day=31, hour=23, minute=59, second=59, microsecond=0)
            delta_list.append({'fromdate':fromdate_part_end, 'todate':todate_part_end})
            #print(fromdate_part_end, '-', todate_part_end, 'END')

    elif partion_by=='month':
        # Первый месяц
        fromdate_part_begin = fromdate # + relativedelta(hour=0, minute=0, second=0)
        todate_part_begin = min(fromdate + relativedelta(day=31, hour=23, minute=59, second=59, microsecond=0), todate)
        delta_list.append({'fromdate':fromdate_part_begin, 'todate':todate_part_begin})

        fromdate_part = todate_part_begin + timedelta(seconds=1)
        while fromdate_part < todate.replace(day=1,hour=0,minute=0,second=0,microsecond=0):
            #print(fromdate_part, todate.replace(hour=0,minute=0,second=0,microsecond=0))
            todate_part = fromdate_part + relativedelta(day=31, hour=23, minute=59, second=59, microsecond=0)
            delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
            fromdate_part = (fromdate_part + timedelta(days=31)).replace(day=1)

        # Последний месяц
        if delta_list[-1]['todate']  < todate.replace(microsecond=0):
            fromdate_part_end = (todate + relativedelta(day=1, hour=0, minute=0, second=0)).replace(microsecond=0)
            todate_part_end = todate.replace(microsecond=0) #+ relativedelta(day=31, hour=23, minute=59, second=59, microsecond=0)
            delta_list.append({'fromdate':fromdate_part_end, 'todate':todate_part_end})
            #print(fromdate_part_end, '-', todate_part_end, 'END')

    elif partion_by=='year':
        # Первый год
        fromdate_part_begin = fromdate # + relativedelta(hour=0, minute=0, second=0)
        todate_part_begin = min(fromdate + relativedelta(month=12, day=31, hour=23, minute=59, second=59, microsecond=0), todate)
        delta_list.append({'fromdate':fromdate_part_begin, 'todate':todate_part_begin})
        #print(fromdate_part_begin, '-', todate_part_begin, 'BEGIN')
        for i in range(fromdate.year+1, todate.year):
            fromdate_part = fromdate + relativedelta(year=i, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            todate_part = fromdate + relativedelta(year=i, month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
            delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
            #print(fromdate_part, '-', todate_part)
        # Последний год
        if delta_list[-1]['todate']  < todate.replace(microsecond=0):
            fromdate_part_end = (todate + relativedelta(month=1, day=1, hour=0, minute=0, second=0)).replace(microsecond=0)
            todate_part_end = todate.replace(microsecond=0)
            delta_list.append({'fromdate':fromdate_part_end, 'todate':todate_part_end})
            #print(fromdate_part_end, '-', todate_part_end, 'END')
    elif type(partion_by) == int and partion_by>0:
        delta = todate - fromdate
        delta_by_part = delta/partion_by
        #print('Кол-во часте:', part)
        #print('Всего дней:', delta)
        #print('Дней на часть:', delta_by_part)
        for i in range(partion_by):
            fromdate_part = (fromdate + i*delta_by_part).replace(microsecond=0)
            todate_part = (fromdate.replace(microsecond=0) + i*delta_by_part + delta_by_part - timedelta(seconds=1)).replace(microsecond=0)
            delta_list.append({'fromdate':fromdate_part, 'todate':todate_part})
            #print(i, fromdate_part, '-', todate_part)

    return delta_list


def truncatechars(text, length, onestring=True):
    """
    Урезает текст до указанного кол-ва символов (length)
        Если текст урезается, в конце ставятся три точки ...
    :param text: Текст которы надо укоротить
    :param length: Длина текста
    :param onestring: Многострочный текст превращается в однострочный
    :return: Укороченный текст
    :type text: str
    :type length: int
    :type onestring: bool
    :rtype: str

    Примеры:
        truncatechars('Длинный текст', 8, onestring=True) -> 'Длинн...'
    """
    if onestring:
        text = text.replace('\n',' ').strip()
    if len(text)>length:
        res = '{}...'.format(text[:length-3])
    else:
        res = text
    return res


def clean_text(text, replace_newline='\n'):
    """

    :param text: Текст содержащий спецсимволы
    :return: Текст без спецсимволов
    :type text: str
    :rtype: str
    """
    rus_chars = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЪЫЭЮЯабвгдеёжзийклмнопрстуфхцчшщьъыэюя'
    eng_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    number_chars = '0123456789'
    sign_chars = ' `~!@#$%^&*()_+=-/\\|?.,"№;:'
    spec_chars = '\n'
    legal_char = rus_chars + eng_chars + sign_chars + number_chars + spec_chars
    res = ''
    for char in text:
        if char in legal_char:
            res += char
        # else:
        #     res += '?'
    res = res.replace('\n', replace_newline)
    return res

if __name__ == '__main__':
    pass
    #from pprint import pprint
    #from datetime import datetime as dt



