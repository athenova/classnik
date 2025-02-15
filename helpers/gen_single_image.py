from openai import OpenAI
import os
import json
from PIL import Image
import requests
from Task import as_task

AI_TEXT_MODEL = 'gpt-4o-mini'
AI_IMAGE_MODEL = 'dall-e-3'

tasks = [json.loads('''{
        "group": "История 5 класс",
        "title": "Ослабление Эллады. Возвышение Македонии",
        "prompt": "Напиши, один интересный факт по теме 'Ослабление Эллады. Возвышение Македонии', используй не более 300 слов, заинтересуй аудиторию в изучении темы",
        "image_prompt": "Напиши промт для генерации изображения по теме 'Ослабление Эллады. Возвышение Македонии', используй не более 4000 символов",
        "task_date": "2025-02-16",
        "age": 12
    }''', object_hook=as_task)]

client = OpenAI()

for i, task in enumerate(tasks):
    folder_name = f"files/{task.group}"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    folder_name = f"{folder_name}/{task.title}"

    title_filename = f"{folder_name}/title.txt"
    text_filename = f"{folder_name}/text.txt"
    image_propmpt_filename = f"{folder_name}/image.txt"
    input_image_filename = f"{folder_name}/image.webp"
    output_image_filename = f"{folder_name}/image.png"

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        
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
        else:
            image_prompt = open(image_propmpt_filename, 'rt', encoding='UTF-8').read()

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