
from Task import Task
from openai import OpenAI
import os
import json
from PIL import Image

def as_task(dct):
    return Task(dct['group'], dct['title'], dct['prompt'], dct['image_prompt'], dct['task_date'], dct['age'])

tasks = json.load(open('files/tasks.json', 'rt', encoding='UTF-8'), object_hook=as_task)

client = OpenAI()

for i, task in enumerate(tasks):
    folder_name = f"files/{task.group}/{task.title}"
    input_image_filename = f"{folder_name}/image.webp"
    output_image_filename = f"{folder_name}/image.png"

    if os.path.exists(input_image_filename) and not os.path.exists(output_image_filename):
        webp_image = Image.open(input_image_filename)
        png_image = webp_image.convert("RGBA")
        png_image.save(output_image_filename)