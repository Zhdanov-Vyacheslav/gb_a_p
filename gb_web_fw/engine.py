from gb_web_fw.logger import Logger
from models import Courses, Category, Users

log_creator = Logger("Creator")


class Creator:
    def __init__(self):
        self._models = {
            "course": Courses.create,
            "category": self.__category,
            "user": Users.create
        }

    def __getattr__(self, item):
        _item = item.lower()
        if _item in self._models:
            def interlayer(*args, **kwargs):
                log_creator.info("Создается {}, параметры: {args}, {kwargs}".format(item, args=args, kwargs=kwargs))
                return self._models[item](*args, **kwargs)
            return interlayer

    @staticmethod
    def __category(*args, **kwargs) -> Category:
        return Category(*args, **kwargs)


class Getter:
    def __init__(self, db: dict):
        self.db = db
        self.__models = {
            "course": self.db["courses"],
            "category": self.db["categories"],
            "teacher": self.db["teachers"],
            "student": self.db["students"]
        }

    def __getattr__(self, item):
        if item.lower() in self.__models:
            def get(**kwargs):
                result = None
                if "id" in kwargs:
                    result = self.__models[item][kwargs["id"]]
                elif "name" in kwargs:
                    name = kwargs["name"]
                    for el in self.__models[item]:
                        if name == el.name:
                            result = el
                    # raise Exception("Not Found: {} with {} = {}".format(item, "name", name))
                return result

            return get


class Engine:
    def __init__(self):
        self.db = {
            "courses": {},
            "categories": {},
            "teachers": {},
            "students": {}
        }
        self.__engine = {
            "create": Creator(),
            "get": Getter(self.db)
        }

    def __getattr__(self, item):
        if item.lower() in self.__engine:
            return self.__engine[item]
