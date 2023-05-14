from urllib.parse import parse_qs
from http.cookies import SimpleCookie

import jwt


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.build_get_params_dict(environ["QUERY_STRING"])
        self.build_post_params_dict(self.get_wsgi_input(environ))
        self.cookie = SimpleCookie(environ.get("HTTP_COOKIE", ""))
        self.settings = settings

    def is_authenticate(self):
        try:
            auth_header = self.cookie["wta"] if "wta" in self.cookie else False
            if auth_header:
                payload = jwt.decode(auth_header.value, self.settings["SECRET_KEY"], algorithms=['HS256'])
                # Проверяем, что пользователь авторизован
                if "user_id" in payload:
                    return True
            raise Exception("Unauthorized")
        except Exception as e:
            return False

    def recognize(self):
        if self.is_authenticate():
            return jwt.decode(self.cookie["wta"].value, self.settings["SECRET_KEY"], algorithms=['HS256'])["user_id"]

    @staticmethod
    def get_wsgi_input(environ: dict) -> bytes:
        content_length = environ.get("CONTENT_LENGTH")
        content_length = int(content_length) if content_length else 0
        return environ["wsgi.input"].read(content_length) if content_length > 0 else b""

    def build_get_params_dict(self, raw_params: str):
        self.GET = parse_qs(raw_params)

    def build_post_params_dict(self, raw_bytes: bytes):
        raw_params = raw_bytes.decode("UTF-8")
        self.POST = parse_qs(raw_params)
