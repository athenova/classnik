class Book:
    def __init__(self, title, author, topics=None, first_week=54, last_week=54):
        self.title = title  # Название книги
        self.author = author  # Автор книги
        self.topics = topics if topics is not None else []  # Список тем (по умолчанию пустой)
        self.first_week = first_week
        self.last_week = last_week

    def add_topic(self, topic):
        """Добавляет тему в список тем книги."""
        self.topics.append(topic)

    def __str__(self):
        topics_str = ", ".join(self.topics) if self.topics else "нет тем"
        return f"Книга: {self.title}, Автор: {self.author}, Темы: {topics_str}"
