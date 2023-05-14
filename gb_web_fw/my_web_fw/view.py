from .request import Request
from .response import Response


class View:
    def get(self, request: Request, *args, **kwargs) -> Response:
        pass

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass


# Decorator для роута
class Views:
    def __init__(self, name, prefix: str):
        self.name = name
        self.url = prefix
        self.views = {}

    def route(self, url):
        def wrapper(cls):
            # Использую setdefault, что-бы если будет 2 одинаковых роута, произошла ошибка
            self.views.setdefault(url, cls)
            return cls

        return wrapper
