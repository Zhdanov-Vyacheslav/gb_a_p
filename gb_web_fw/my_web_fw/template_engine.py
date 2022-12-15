import os
from jinja2 import Template

from .request import Request


class Engine:
    def __init__(self, base_dir: str, template_dir: str):
        self.template_dir = os.path.join(base_dir, template_dir)

    def get_template_as_string(self, template_name: str) -> str:
        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.isfile(template_path):
            raise Exception("{path} is not file".format(path=template_path))
        with open(template_path) as f:
            return f.read()


def render(request: Request, template_name, **kwargs):
    assert request.settings.get("BASE_DIR")
    assert request.settings.get("TEMPLATE_DIR_NAME")

    engine = Engine(
        request.settings.get("BASE_DIR"),
        request.settings.get("TEMPLATE_DIR_NAME")
    )
    template = Template(engine.get_template_as_string(template_name))
    return template.render(**kwargs)
