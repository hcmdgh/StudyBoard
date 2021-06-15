from flask_pymongo import PyMongo
from uuid import uuid4
from typing import Dict, Tuple, List

import util
from bean import *

_mongo = PyMongo()


def init_mongo(*args, **kwargs):
    _mongo.init_app(*args, **kwargs)


def get_collection(collection: str):
    return _mongo.db[collection]


def get_running_task(username: str) -> StudyTask:
    tasks = StudyTask.find({
        "username": username,
        "end_time": { "$gt": datetime.now() },
    })
    if not tasks:
        return None
    elif len(tasks) == 1:
        return tasks[0]
    else:
        raise RuntimeError


def _fetch_session(token: str) -> Dict:
    entry = _mongo.db.session.find_one({
        "_id": token,
    })
    return entry


def login_by_token(token: str) -> Tuple[str, str]:
    session = _fetch_session(token)
    if session is None:
        raise ValidationError
    username = session["username"]
    session["login_time"] = datetime.now()
    _mongo.db.session.save(session)
    return username, token


def login_by_pswd(username: str, password: str) -> Tuple[str, str]:
    entry = _mongo.db.user.find_one({
        "username": username,
        "password": password,
    })
    if entry is None:
        raise ValidationError
    while True:
        token = str(uuid4())
        if _fetch_session(token) is None:
            break
    _mongo.db.session.insert_one({
        "_id": token,
        "username": username,
        "login_time": datetime.now(),
    })
    return username, token


def get_daily_study_time(username: str) -> int:
    total = 0
    for task in get_finished_tasks(date=datetime.now(), username=username):
        total += task.duration
    return total


def interrupt_task(username: str):
    task = get_running_task(username)
    if task:
        now = datetime.now()
        task.end_time = now
        task.duration = int((now - task.begin_time).total_seconds() // 60)
        task.save()


def get_finished_tasks(*, date: datetime, username: str) -> List[StudyTask]:
    begin, end = util.get_date_bounds(date)
    tasks = StudyTask.find({
        "username": username,
        "begin_time": { "$gt": begin, "$lt": end },
        "end_time": { "$lt": datetime.now() },
    })
    return tasks


def get_notification(username: str) -> List[int]:
    tasks = StudyTask.find({
        "username": username,
        "end_time": { "$lt": datetime.now() },
        "notified": False,
    })
    durations = []
    for task in tasks:
        durations.append(task.duration)
        task.notified = True
        task.save()
    return durations


def update_diary(*, username: str, date: datetime, content: str):
    date = util.to_date(date)
    diaries = Diary.find({
        "username": username,
        "date": date,
    })
    if not diaries:
        Diary(content=content, date=date, username=username).save()
    elif len(diaries) == 1:
        diaries[0].content = content
        diaries[0].save()
    else:
        raise RuntimeError


def get_diaries(username: str) -> List[Diary]:
    return Diary.find({
        "username": username,
    })
