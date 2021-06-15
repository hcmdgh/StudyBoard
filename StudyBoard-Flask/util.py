from datetime import datetime, timedelta
from typing import Tuple

WEEKDAY_ARR = "一二三四五六日"


def datetime2str(dt: datetime, format_: str) -> str:
    dict_ = {
        "d": f"{dt.year}年{dt.month}月{dt.day}日",
        "t": f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}",
        "w": f"星期{WEEKDAY_ARR[dt.isoweekday()]}",
    }
    return " ".join(dict_[ch] for ch in format_)


def get_date_bounds(dt: datetime) -> Tuple[datetime, datetime]:
    begin = to_date(dt)
    end = begin + timedelta(days=1)
    return begin, end


def to_date(dt: datetime) -> datetime:
    return datetime.fromordinal(dt.toordinal())


if __name__ == '__main__':
    print(datetime2str(datetime.now(), "dtw"))
