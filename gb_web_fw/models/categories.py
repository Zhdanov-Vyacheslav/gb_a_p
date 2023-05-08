class Category:
    auto_id = 0

    def __init__(self, name: str):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.courses = []
