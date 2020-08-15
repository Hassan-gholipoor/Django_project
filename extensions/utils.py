from . import jalali
from django.utils import timezone


def persian_number(mystr):
    numbers = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }
    for e, p in numbers.items():
        mystr = mystr.replace(e, p)
    return mystr


def jalali_converter(time):
    jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'ابان', 'آذر', 'دی', 'بهمن', 'اسفند']
    time = timezone.localtime(time)
    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_tuple = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_tuple[1] == index + 1:
            time_to_tuple[1] = month
            break
    output = f'{time_to_tuple[2]} {time_to_tuple[1]} {time_to_tuple[0]}, {time.minute} : {time.hour}'
    return persian_number(output)
