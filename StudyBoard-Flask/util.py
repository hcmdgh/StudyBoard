from datetime import datetime, timedelta
from typing import Tuple

WEEKDAY_ARR = "零一二三四五六日"


def datetime2str(dt: datetime, format_: str) -> str:
    dict_ = {
        "d": f"{dt.year}年{dt.month}月{dt.day}日",
        "t": f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}",
        "w": f"星期{WEEKDAY_ARR[dt.isoweekday()]}",
    }
    return " ".join(dict_[ch] for ch in format_)


def format_minutes(minutes: int) -> str:
    if minutes <= 0:
        return "--"
    m = minutes % 60
    h = minutes // 60
    if h > 0:
        return f"{h} 时 {m} 分"
    else:
        return f"{m} 分"


def get_date_bounds(date: datetime) -> Tuple[datetime, datetime]:
    begin = date + timedelta(hours=5)
    end = begin + timedelta(days=1)
    return begin, end


def to_date(dt: datetime) -> datetime:
    date = datetime.fromordinal(dt.toordinal())
    if dt.hour < 5:
        date -= timedelta(days=1)
    return date


if __name__ == '__main__':
    print(datetime2str(datetime.now(), "dtw"))
