import os
from datetime import datetime

DEBUG = os.getenv("DEBUG", "")
DEBUG = True if "1" == DEBUG or "true" == DEBUG.lower() else False


# Singleton для логгера
class MetaLogger(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if kwargs:
            name = kwargs['name']
        elif args:
            name = args[0]
        else:
            # Если нет ни args, kwargs значит не задано имя логгера
            raise TypeError("__init__() missing 1 required positional argument: 'name'")

        # Если нет логгера с таким именем, создаем
        if name not in cls.__instance:
            cls.__instance[name] = super().__call__(*args, **kwargs)
        return cls.__instance[name]


class Logger(metaclass=MetaLogger):
    def __init__(self, name: str):
        self.__levels = {
            "CRITICAL",
            "FATAL",
            "ERROR",
            "WARNING",
            "INFO",
        }
        if DEBUG:
            self.__levels.add("DEBUG")
        self.__name = name
        self.__path = os.path.join(os.path.split(os.path.dirname(__file__))[0], name.lower() + ".log")

    def __getattr__(self, item):
        if item.upper() in self.__levels:

            def log(*args, **kwargs):
                return self.__log(item.upper(), *args, **kwargs)

            return log
        # Сюда будет прилетать когда debug выключен
        elif item.upper() == "DEBUG":
            return self.__bypass

    # Обход для DEBUG
    def __bypass(self, *args, **kwargs):
        pass

    def __log(self, level, text: str, *args, **kwargs):
        log = "[{time}]-[{level}]-[{name}]: {text}\n".format(
            time=str(datetime.utcnow()).replace(" ", "T")[:-3] + "Z",
            level=level,
            name=self.__name,
            text=text
        )
        print(log)
        with open(self.__path, "a", encoding="UTF-8") as f:
            f.write(log)
