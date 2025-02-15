class Task:
    def __init__(self, group:str, title: str, prompt: str, image_prompt: str, task_date: str, age = 11):
        self.group = group
        self.title = title
        self.prompt = prompt
        self.image_prompt = image_prompt
        self.task_date = task_date
        self.age = age

def as_task(dct):
    return Task(dct['group'], dct['title'], dct['prompt'], dct['image_prompt'], dct['task_date'], dct['age'])
