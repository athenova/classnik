import os
import telebot
import json

import telebot.formatting
from datetime import date
import time
from Task import as_task

tasks = json.load(open('files/tasks.json', 'rt', encoding='UTF-8'), object_hook=as_task)

BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
CHAT_ID = '@class5nik'
#CHAT_ID = -1002374309134

for i, task in enumerate(tasks):
    if task.task_date == date.today().strftime('%Y-%m-%d'):
        folder_name = f"files/{task.group}/{task.title}"
        if os.path.exists(folder_name):
            text_filename = f"{folder_name}/text.txt"
            output_image_filename = f"{folder_name}/image.png"
            bot = telebot.TeleBot(BOT_TOKEN)
            if os.path.exists(output_image_filename):
                bot.send_photo(chat_id=CHAT_ID, photo=open(output_image_filename, 'rb'), disable_notification=True)
            if os.path.exists(text_filename):
                bot.send_message(chat_id=CHAT_ID, text=open(text_filename, 'rt', encoding='UTF-8').read(), parse_mode="Markdown")
                time.sleep(60)