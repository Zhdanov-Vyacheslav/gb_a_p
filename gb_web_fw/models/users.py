class User:
    auto_id = 0

    def __init__(self, name, password, salt):
        self.id = self.auto_id
        User.auto_id += 1
        self.name = name
        self.password = password
        self.salt = salt
        self.courses = {}


class Teacher(User):
    def __init__(self, name, password, salt, refer):
        super().__init__(name, password, salt)
        self.refer = refer


class Student(User):
    pass


class Users:
    types = {
        "teacher": Teacher,
        "student": Student
    }

    @classmethod
    def create(cls, _type, *args, **kwargs):
        return cls.types[_type](*args, **kwargs)
