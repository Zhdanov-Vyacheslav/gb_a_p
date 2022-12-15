from urllib.parse import parse_qs


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.build_get_params_dict(environ["QUERY_STRING"])
        self.settings = settings

    def build_get_params_dict(self, raw_params):
        self.GET = parse_qs(raw_params)
