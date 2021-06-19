from datetime import datetime, timedelta
from typing import Dict, List
import util
import db


class StudyTask:
    def __init__(self, *,
                 _id=None,
                 begin_time: datetime = None,
                 end_time: datetime = None,
                 duration: int,
                 desc: str,
                 username: str,
                 notified: bool = False):
        self._id = _id
        if not begin_time:
            self.begin_time = datetime.now()
            self.end_time = self.begin_time + timedelta(minutes=duration)
        else:
            self.begin_time = begin_time
            self.end_time = end_time
        self.duration = duration
        self.desc = desc
        self.username = username
        self.notified = notified

    def save(self):
        entry = dict(self.__dict__)
        if self._id is None:
            del entry["_id"]
        db.get_collection("study_task").save(entry)

    @classmethod
    def find(cls, query: Dict) -> List['StudyTask']:
        entries = db.get_collection("study_task").find(query)
        res = []
        for entry in entries:
            res.append(StudyTask(**entry))
        return res

    def to_json(self) -> Dict:
        json_obj = dict(self.__dict__)
        del json_obj["_id"]
        json_obj["begin_time"] = util.datetime2str(json_obj["begin_time"], "t")
        json_obj["end_time"] = util.datetime2str(json_obj["end_time"], "t")
        return json_obj

    def get_remain_seconds(self) -> int:
        return int((self.end_time - datetime.now()).total_seconds())


class Diary:
    def __init__(self, *, _id=None, content: str, date: datetime = None, username: str):
        self._id = _id
        self.content = content
        if date:
            self.date = date
        else:
            self.date = util.to_date(datetime.now())
        self.username = username

    def save(self):
        entry = dict(self.__dict__)
        if self._id is None:
            del entry["_id"]
        db.get_collection("diary").save(entry)

    @classmethod
    def find(cls, query: Dict) -> List['Diary']:
        entries = db.get_collection("diary").find(query)
        res = []
        for entry in entries:
            res.append(Diary(**entry))
        return res

    def to_json(self) -> Dict:
        json_obj = dict(self.__dict__)
        del json_obj["_id"]
        json_obj["date"] = util.datetime2str(json_obj["date"], "dw")
        return json_obj


class Excerpt:
    def __init__(self, *, _id=None, content: str, source: str, date: datetime = None, username: str):
        self._id = _id
        self.content = content
        self.source = source
        if date:
            self.date = date
        else:
            self.date = util.to_date(datetime.now())
        self.username = username

    def save(self):
        entry = dict(self.__dict__)
        if self._id is None:
            del entry["_id"]
        db.get_collection("excerpt").save(entry)

    @classmethod
    def find(cls, query: Dict) -> List['Excerpt']:
        entries = db.get_collection("excerpt").find(query)
        res = []
        for entry in entries:
            res.append(Excerpt(**entry))
        return res

    def to_json(self) -> Dict:
        json_obj = dict(self.__dict__)
        del json_obj["_id"]
        json_obj["date"] = util.datetime2str(json_obj["date"], "dw")
        return json_obj


class ValidationError(RuntimeError):
    pass
