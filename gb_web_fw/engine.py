from gb_web_fw.logger import Logger
from models import Courses, Category

log_creator = Logger("Creator")


class Creator:
    def __init__(self):
        self.__models = {
            "course": Courses.create,
            "category": self.__category
        }

    def __getattr__(self, item):
        if item.lower() in self.__models:
            def interlayer(*args, **kwargs):
                log_creator.info("Создается {}, параметры: {args}, {kwargs}".format(item, args=args, kwargs=kwargs))
                return self.__models[item](*args, **kwargs)
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
            "categories": {}
        }
        self.__engine = {
            "create": Creator(),
            "get": Getter(self.db)
        }

    def __getattr__(self, item):
        if item.lower() in self.__engine:
            return self.__engine[item]
