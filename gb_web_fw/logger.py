import os
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

DEBUG = os.getenv("DEBUG", "")
DEBUG = True if "1" == DEBUG or "true" == DEBUG.lower() else False


# Strategy для логера
class Writer(metaclass=ABCMeta):
    @abstractmethod
    def write(self, msg, name):
        pass


class ConsoleWriter(Writer):
    def write(self, msg, name):
        print(msg)


class LogFileWriter(Writer):
    def __init__(self):
        self.__path = os.path.dirname(__file__)

    def write(self, msg, name):
        path = os.path.join(os.path.split(self.__path)[0], name.lower() + ".log")
        with open(path, "a", encoding="UTF-8") as f:
            f.write(msg)


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
    def __init__(self, name: str, writers: List[Writer] = None):
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
        self.__writers = writers if writers else [ConsoleWriter(), LogFileWriter()]

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
        for writer in self.__writers:
            writer.write(log, self.__name)
