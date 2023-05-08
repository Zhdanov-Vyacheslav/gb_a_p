from datetime import datetime

from . import Category


class Course:
    auto_id = 0

    def __init__(self, name: str, start: datetime, text: str):
        self.id = Course.auto_id
        Course.auto_id += 1
        self.name = name
        self.start = start
        self.text = text


class Offline(Course):
    def __init__(self, name: str, start: datetime, text: str, location: str):
        super().__init__(name, start, text)
        self.location = location


class Online(Course):
    def __init__(self, name: str, start: datetime, text: str, url: str):
        super().__init__(name, start, text)
        self.url = url


# Factory для курсов
class Courses:
    types = {
        "offline": Offline,
        "online": Online
    }

    @classmethod
    def create(cls, _type, *args, **kwargs):
        return cls.types[_type](*args, **kwargs)
