
from openai import OpenAI
import os
import json
import requests
from PIL import Image
from datetime import date
import time
from helpers.Task import as_task
import telebot
import schedule

AI_TEXT_MODEL = 'gpt-4o-mini'
AI_IMAGE_MODEL = 'dall-e-3'
AI_PROMPT_LIMIT = 4000
TOPIC_WORD_LIMIT = 300
TOPIC_IMAGE_PROMPT_WORD_LIMIT = 300
BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
CHAT_ID = '@class5nik'
#CHAT_ID = -1002374309134

tasks = json.load(open('files/tasks.json', 'rt', encoding='UTF-8'), object_hook=as_task)

client = OpenAI()

def job(index):
    j = 0
    for i, task in enumerate(tasks):
        if task.task_date == date.today().strftime('%Y-%m-%d'):
            j += 1
            if j == index:
                if not os.path.exists("files"):
                    os.mkdir("files")
                folder_name = f"files/{task.group}"
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                folder_name = f"files/{task.group}/{task.title}"

                title_filename = f"{folder_name}/title.txt"
                text_filename = f"{folder_name}/text.txt"
                image_propmpt_filename = f"{folder_name}/image.txt"
                input_image_filename = f"{folder_name}/image.webp"
                output_image_filename = f"{folder_name}/image.png"

                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                    
                if not os.path.exists(title_filename):
                    open(title_filename, 'wt', encoding="UTF-8").write(task.title)
                
                if not os.path.exists(text_filename):
                    text = client.chat.completions.create(
                        model=AI_TEXT_MODEL,
                        messages=[
                            { "role": "system", "content": f"Ты - блогер с 1000000 подписчиков и целевой аудиторией {task.age} лет, используешь в разговоре сленг и смайлики" },
                            { "role": "user", "content": task.prompt },
                        ]
                    ).choices[0].message.content
                    open(text_filename, 'wt', encoding="UTF-8").write(text)
                
                if task.image_prompt is not None:
                    if not os.path.exists(image_propmpt_filename):
                        image_prompt = client.chat.completions.create(
                            model=AI_TEXT_MODEL,
                            messages=[
                                { "role": "system", "content": f"Ты - блогер с 1000000 подписчиков и целевой аудиторией {task.age} лет" },
                                { "role": "user", "content": task.image_prompt },
                            ],
                        ).choices[0].message.content
                        open(image_propmpt_filename, 'wt', encoding="UTF-8").write(image_prompt)

                    if not os.path.exists(input_image_filename):
                        image_url = client.images.generate(
                            model=AI_IMAGE_MODEL,
                            prompt=image_prompt,
                            size="1024x1024",
                            quality="standard",
                            n=1,
                        ).data[0].url
                        response = requests.get(image_url)
                        with open(input_image_filename, 'wb') as f:
                            f.write(response.content)

                    if os.path.exists(input_image_filename) and not os.path.exists(output_image_filename):
                        webp_image = Image.open(input_image_filename)
                        png_image = webp_image.convert("RGBA")
                        png_image.save(output_image_filename)
                
                bot = telebot.TeleBot(BOT_TOKEN)
                if os.path.exists(output_image_filename):
                    bot.send_photo(chat_id=CHAT_ID, photo=open(output_image_filename, 'rb'), disable_notification=True)
                if os.path.exists(text_filename):
                    bot.send_message(chat_id=CHAT_ID, text=open(text_filename, 'rt', encoding='UTF-8').read(), parse_mode="Markdown")

schedule.every().day.at("07:50",'Europe/Moscow').do(job, index = 1)
schedule.every().day.at("08:50",'Europe/Moscow').do(job, index = 2)
schedule.every().day.at("09:55",'Europe/Moscow').do(job, index = 3)
schedule.every().day.at("11:05",'Europe/Moscow').do(job, index = 4)
schedule.every().day.at("12:15",'Europe/Moscow').do(job, index = 5)
schedule.every().day.at("13:15",'Europe/Moscow').do(job, index = 6)

half_day = 12 * 60 * 60

for i in range(half_day):
    schedule.run_pending()
    time.sleep(1)