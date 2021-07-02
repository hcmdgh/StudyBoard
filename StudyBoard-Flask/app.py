from flask import Flask, abort, request, jsonify, g
from flask_cors import CORS
from typing import Dict
import functools
import db
import util
from bean import *
import config

app = Flask(__name__)
if config.dev:
    CORS(app, supports_credentials=True)
db.init_mongo(app=app, uri="mongodb://localhost:27017/study_board")


def login_required(func):
    @functools.wraps(func)
    def decorated_func(*args, **kwargs):
        token = request.json["token"]
        try:
            username, token = db.login_by_token(token)
            g.username = username
            return func(*args, **kwargs)
        except ValidationError:
            return jsonify(error="invalid")

    return decorated_func


@app.route('/login-by-pswd/', methods=["POST"])
def login_by_pswd():
    json_obj = request.json
    username = json_obj["username"]
    password = json_obj["password"]
    try:
        username, token = db.login_by_pswd(username, password)
        return jsonify(username=username, token=token)
    except ValidationError:
        return jsonify(error="invalid")


@app.route('/get-username/', methods=["POST"])
@login_required
def get_username():
    return jsonify(username=g.username)


@app.route('/get-daily-states/', methods=["POST"])
@login_required
def get_daily_states():
    resp_dict = dict()

    # 获取正在进行的学习任务
    study_task = db.get_running_task(g.username)
    if study_task:
        resp = study_task.to_json()
        resp["remain_seconds"] = study_task.get_remain_seconds()
        resp_dict["running_task"] = resp
    else:
        resp_dict["running_task"] = { "error": "not studying" }

    # 获取当日已经完成的学习任务
    tasks = []
    for task in db.get_finished_tasks(date=datetime.now(), username=g.username):
        tasks.append(task.to_json())
    resp_dict["finished_tasks"] = tasks

    # 获取当日学习时长
    minutes = db.get_daily_study_time(g.username)
    resp_dict["duration_str"] = util.format_minutes(minutes)

    return jsonify(resp_dict)


@app.route('/add-study-task/', methods=["POST"])
@login_required
def add_study_task():
    json_obj = request.json
    duration = json_obj["duration"]
    desc = json_obj.get("desc", "")
    username = g.username
    if db.get_running_task(username) is None:
        study_task = StudyTask(
            duration=duration,
            desc=desc,
            username=username,
        )
        study_task.save()
        return jsonify(error=None)
    else:
        return jsonify(error="studying")


@app.route('/interrupt-task/', methods=["POST"])
@login_required
def interrupt_task():
    db.interrupt_task(g.username)
    return jsonify(error=None)


@app.route('/get-notification/', methods=["POST"])
@login_required
def get_notification():
    return jsonify(durations=db.get_notification(g.username))


@app.route('/update-diary/', methods=["POST"])
@login_required
def update_diary():
    db.update_diary(
        username=g.username,
        content=request.json["content"],
        date=datetime.now(),
    )
    return jsonify(error=None)


@app.route('/get-diaries/', methods=["POST"])
@login_required
def get_diaries():
    diaries = []
    for diary in db.get_diaries(g.username):
        diaries.append(diary.to_json())
    return jsonify(diaries=diaries)


@app.route('/get-book-records/', methods=["POST"])
@login_required
def get_book_records():
    records = []
    for record in db.get_book_records(g.username):
        records.append(record.to_json())
    return jsonify(book_records=records)


@app.route('/update-excerpt/', methods=["POST"])
@login_required
def update_excerpt():
    db.update_excerpt(
        username=g.username,
        content=request.json["content"],
        source=request.json["source"],
        date=datetime.now(),
    )
    return jsonify(error=None)


@app.route('/get-excerpts/', methods=["POST"])
@login_required
def get_excerpts():
    excerpts = []
    for excerpt in db.get_excerpts(g.username):
        excerpts.append(excerpt.to_json())
    return jsonify(excerpts=excerpts)


@app.route('/get-recent-study-time/', methods=["POST"])
@login_required
def get_recent_study_time():
    return jsonify(recent_study_time=db.get_recent_study_time(g.username))


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)
