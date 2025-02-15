class Topic:
    def __init__(self, name, author=None, week = 54, messages = None):
        self.name = name  # Название темы (обязательное поле)
        self.author = author  # Автор темы (необязательное поле)
        self.week = week # Неделя года
        self.messages = messages if messages is not None else []

    def __str__(self):
        if self.author:
            return f"Тема: {self.name}, Автор: {self.author}"
        else:
            return f"Тема: {self.name}"
