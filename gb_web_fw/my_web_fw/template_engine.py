import os
from jinja2 import Template, Environment, FileSystemLoader

from .request import Request


class Engine:
    def __init__(self, base_dir: str, template_dir: str):
        self.template_dir = os.path.join(base_dir, template_dir)

    def get_template(self, template_name: str) -> Template:
        template_path = os.path.join(self.template_dir)
        file_loader = FileSystemLoader(template_path)
        environment = Environment(loader=file_loader)
        template = environment.get_template(template_name)
        return template


def render(request: Request, template_name, **kwargs):
    assert request.settings.get("BASE_DIR")
    assert request.settings.get("TEMPLATE_DIR_NAME")

    engine = Engine(
        request.settings.get("BASE_DIR"),
        request.settings.get("TEMPLATE_DIR_NAME")
    )
    template = engine.get_template(template_name)
    return template.render(**kwargs)
