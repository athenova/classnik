import os
import telebot
import json
from datetime import date
from datetime import timedelta
from helpers.Task import as_task

tasks = json.load(open('files/tasks.json', 'rt', encoding='UTF-8'), object_hook=as_task)

BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
check_date = date.today() + timedelta(days=1)
CHAT_ID = -1002374309134

for i, task in enumerate(tasks):
    if task.task_date == check_date.strftime('%Y-%m-%d'):
        folder_name = f"files/{task.group}/{task.title}"
        if os.path.exists(folder_name):
            text_filename = f"{folder_name}/text.txt"
            output_image_filename = f"{folder_name}/image.png"
            bot = telebot.TeleBot(BOT_TOKEN)
            if os.path.exists(output_image_filename) and os.path.exists(text_filename):
                bot.send_photo(chat_id=CHAT_ID,parse_mode="Markdown", photo=open(output_image_filename, 'rb'), caption=open(text_filename, 'rt', encoding='UTF-8').read())
            else:
                if os.path.exists(output_image_filename):
                    bot.send_photo(chat_id=CHAT_ID,parse_mode="Markdown", photo=open(output_image_filename, 'rb'), disable_notification=True)
                if os.path.exists(text_filename):
                    bot.send_message(chat_id=CHAT_ID, text=open(text_filename, 'rt', encoding='UTF-8').read(), parse_mode="Markdown")                