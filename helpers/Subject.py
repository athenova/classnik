class Subject:
    def __init__(self, name, form, age, prompt, image_prompt=None, books=None):
        self.name = name  # Название предмета
        self.form = form  # Класс
        self.age = age # Возраст ребёнка
        self.prompt = prompt
        self.image_prompt = image_prompt
        self.books = books if books is not None else []  # Список книг (по умолчанию пустой)


    def add_book(self, book):
        """Добавляет книгу в список книг предмета."""
        self.books.append(book)

    def __str__(self):
        books_str = "\n".join([str(book) for book in self.books]) if self.books else "нет книг"
        return f"Предмет: {self.name}\nКниги:\n{books_str}"