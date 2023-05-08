import os
import re
from typing import List, Type

from .exceptions import NotFound, NotAllowed
from .template_engine import render
from .urls import Url
from .view import View
from .request import Request
from .response import Response


class MyWebFW:
    __slots__ = ("urls", "settings", "engine", "__code_404")

    def __init__(self, urls: List[Url], settings: dict, engine):
        self.urls = urls
        self.settings = settings
        self.engine = engine
        self.__code_404 = None

    def __call__(self, environ: dict, start_response):
        request = self._get_request(environ)
        try:
            view = self._get_view(environ)
            response = self._get_response(environ, view, request)
        except NotFound as ex:
            # Заглушка от краша
            if environ["PATH_INFO"] == "/favicon.ico":
                print("/favicon.ico NOT FOUND")
                response = Response(body="", status_code=201)
            # Сохраняем 404 страницу
            elif self.__code_404 is None:
                path = os.path.join(self.settings["BASE_DIR"], self.settings["TEMPLATE_DIR_NAME"], "404.html")
                # Если есть шаблон, используем
                if os.path.isfile(path):
                    self.__code_404 = Response(body=render(request, "404.html"), status_code=ex.code)
                else:
                    self.__code_404 = Response(body=ex.text, status_code=ex.code)
                response = self.__code_404
            else:
                response = self.__code_404
        start_response(
            str(response.status),
            list(response.headers.items())
        )
        return iter([response.body])


    @staticmethod
    def _prepare_url(url: str) -> str:
        if url[-1] == "/":
            return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        url = self._prepare_url(raw_url)
        for path in self.urls:
            match = re.match(path.url, url)
            if match is not None:
                return path.view
        raise NotFound

    def _get_view(self, environ) -> View:
        raw_url = environ["PATH_INFO"]
        view = self._find_view(raw_url)()
        return view

    def _get_request(self, environ: dict) -> Request:
        return Request(environ, settings=self.settings)

    def _get_response(self, environ: dict, view: View, request: Request) -> Response:
        method = environ["REQUEST_METHOD"].lower()
        if not hasattr(view, method):
            raise NotAllowed
        return getattr(view, method)(request, engine=self.engine)
