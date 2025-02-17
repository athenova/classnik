
from Task import as_task
from openai import OpenAI
import os
import json

AI_TEXT_MODEL = 'gpt-4o-mini'
AI_PROMPT_LIMIT = 4000
TOPIC_WORD_LIMIT = 300
TOPIC_IMAGE_PROMPT_WORD_LIMIT = 300

tasks = json.load(open('files/tasks.json', 'rt', encoding='UTF-8'), object_hook=as_task)

client = OpenAI()

for i, task in enumerate(tasks):
    folder_name = f"files/{task.group}"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    folder_name = f"{folder_name}/{task.title}"
    title_filename = f"{folder_name}/title.txt"
    text_filename = f"{folder_name}/text.txt"
    image_propmpt_filename = f"{folder_name}/image.txt"

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
