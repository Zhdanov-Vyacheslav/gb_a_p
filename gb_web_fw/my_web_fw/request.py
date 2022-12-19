from urllib.parse import parse_qs


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.build_get_params_dict(environ["QUERY_STRING"])
        self.build_post_params_dict(self.get_wsgi_input(environ))
        self.settings = settings

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
