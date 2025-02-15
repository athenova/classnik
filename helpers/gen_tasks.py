
from Task import Task
from datetime import datetime
from datetime import timedelta
from Data import subjects
import json
import math

TOPIC_WORD_LIMIT = 300
TOPIC_IMAGE_PROMPT_SYMBOL_LIMIT = 4000

tasks = []

for i, subject in enumerate(subjects):
    for j, book in enumerate(subject.books):
        start_date = datetime.fromisocalendar(datetime.today().year, book.first_week, 1)
        end_date = datetime.fromisocalendar(datetime.today().year, book.last_week, 1)
        delta = end_date - start_date
        days = delta.days
        period = days / len(book.topics)
        delta = 5 * period / 7
        for k, topic in enumerate(book.topics):
            tasks.append(Task(
                book.title
                , topic.name
                , subject.prompt.format(topic.name, TOPIC_WORD_LIMIT)
                , subject.image_prompt.format(topic.name, TOPIC_IMAGE_PROMPT_SYMBOL_LIMIT) if subject.image_prompt is not None else None
                , (start_date + timedelta(days=math.trunc(k*delta) + 2*math.trunc(k*period/7))).strftime('%Y-%m-%d'), subject.age)                
                )
            
tasks.sort(key=lambda task: task.task_date)

def custom_json(obj):
    if isinstance(obj, Task):
        return {'group': obj.group, 'title': obj.title, 'prompt': obj.prompt, 'image_prompt': obj.image_prompt, 'task_date': obj.task_date, 'age': obj.age}
    raise TypeError(f'Cannot serialize object of {type(obj)}')

json.dump(tasks, open('files/tasks.json', 'wt', encoding='UTF-8'), indent=4, default=custom_json, ensure_ascii=False)