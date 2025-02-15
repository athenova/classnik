import os
import telebot
import json

import telebot.formatting
from datetime import date
from datetime import timedelta
from Task import as_task

tasks = json.load(open('files/tasks.json', 'rt', encoding='UTF-8'), object_hook=as_task)

BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
CHAT_ID = -1002374309134

check_date = date.today() + timedelta(days=1)
bot = telebot.TeleBot(BOT_TOKEN)

for i, task in enumerate(tasks):
    if task.task_date == check_date.strftime('%Y-%m-%d'):
        folder_name = f"files/{task.group}/{task.title}"
        image_propmpt_filename = f"{folder_name}/image.txt"
        output_image_filename = f"{folder_name}/image.png"
        if task.image_prompt is not None and not os.path.exists(output_image_filename):
            bot.send_message(chat_id=CHAT_ID, text=open(image_propmpt_filename, 'rt', encoding='UTF-8').read())                