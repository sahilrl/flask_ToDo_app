import json
from .app import app
from flask import render_template, redirect
from flask import url_for
from flask import request


def get_data():
    with open('db.json', 'r+') as f:
        tasks = json.load(f)
        return tasks


def write_data(tasks):
    with open('db.json', 'w+') as f:
                json.dump(tasks, f, indent=4)
            

@app.route('/', methods=['POST', 'GET'])
def home():
    """
    Homepage
    """
    tasks = get_data()
    if request.method == 'POST':
        newtask = request.values['task']
        if newtask:
            if newtask not in tasks["task"]:
                tasks["task"].append(newtask)
                write_data(tasks)
            else:
                errors = ['the task already exists']
                return render_template('index.html', tasks=tasks, errors=errors)
    return render_template('index.html', tasks=tasks)


@app.route('/removetask', methods=['POST'])
def removetask():
    """
    Remove a Task
    """
    task = request.get_json()
    tasks = get_data()
    if task:
        if task in tasks["task"]:
            tasks["task"].remove(task)
        if task in tasks["completed"]:
            tasks["completed"].remove(task)
        write_data(tasks)
    return 'OK'


@app.route('/markcomplete', methods=['POST'])
def markcomplete():
    """
    Mark task as complete
    """
    task = request.get_json()
    tasks = get_data()
    if task:
        tasks["task"].remove(task)
        tasks["completed"].append(task)
        write_data(tasks)
    return 'OK'


@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset
    """
    tasks = get_data()
    tasks["task"] = []
    tasks["completed"] = []
    write_data(tasks)
    return 'OK'