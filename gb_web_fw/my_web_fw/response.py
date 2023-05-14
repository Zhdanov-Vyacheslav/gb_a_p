from typing import List, Tuple

from .request import Request
from http.cookies import SimpleCookie


class Response:
    def __init__(self, request: Request, body: str = "",
                 cookie: dict = None, status_code: int = 200, headers: dict = None):
        self.status_code = status_code
        self.__headers = {}
        self.body = b""
        self.cookie = request.cookie
        self._set_base_headers()
        if headers is not None:
            self.update_headers(headers)
        if cookie is not None:
            self.set_cookie(cookie)
        self._set_body(body)

    @property
    def headers(self) -> List[Tuple[str, str]]:
        _headers = list(self.__headers.items())
        if self.cookie:
            _headers += [("Set-Cookie", el.output(header="")) for el in self.cookie.values()]
        return _headers

    @property
    def status(self) -> str:
        if self.status_code in [200, 201]:
            status = "OK"
        else:
            status = "ERROR"
        return "{code} {status}".format(code=self.status_code, status=status)

    def _set_base_headers(self):
        self.__headers = {
            "Content-Type":  "text/html; charset=utf-8",
            "Content-Length": 0
        }

    def _set_body(self, raw_body: str):
        self.body = raw_body.encode("utf-8")
        self.update_headers(
            {"Content-Length": str(len(self.body))}
        )

    def update_headers(self, headers: dict):
        self.__headers.update(headers)

    def set_cookie(self, cookie: dict):
        _cookie = {}
        for k, v in cookie.items():
            _cookie.update(SimpleCookie(v))
        self.cookie.update(_cookie)
