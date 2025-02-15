import os
import telebot
import json

import telebot.formatting
from datetime import datetime
import time
from Task import as_task

tasks = json.load(open('files/tasks.json', 'rt', encoding='UTF-8'), object_hook=as_task)

for i, task in enumerate(tasks):
    weekday = datetime.strptime(task.task_date, '%Y-%m-%d').weekday()
    if weekday == 5 or weekday == 6:
        print(task.task_date)