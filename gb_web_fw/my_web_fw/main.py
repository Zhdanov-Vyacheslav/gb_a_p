import re
from typing import List, Type

from .exceptions import NotFound, NotAllowed
from .urls import Url
from .view import View
from .request import Request
from .response import Response


class MyWebFW:
    __slots__ = ("urls", "settings")

    def __init__(self, urls: List[Url], settings: dict):
        self.urls = urls
        self.settings = settings

    def __call__(self, environ: dict, start_response):
        try:
            view = self._get_view(environ)
            request = self._get_request(environ)
            response = self._get_response(environ, view, request)
            start_response(
                str(response.status),
                list(response.headers.items())
            )
            return iter([response.body])
        except NotFound:
            # Заглушка от краша
            if environ["PATH_INFO"] == "/favicon.ico":
                print("/favicon.ico NOT FOUND")
                start_response("201 NOT_FOUND", [
                    ("Content-Type", "text/plain; charset=utf-8"),
                    ("Content-Length", "0")
                ])
                return iter([b""])

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

    @staticmethod
    def _get_response(environ: dict, view: View, request: Request) -> Response:
        method = environ["REQUEST_METHOD"].lower()
        if not hasattr(view, method):
            raise NotAllowed
        return getattr(view, method)(request)
