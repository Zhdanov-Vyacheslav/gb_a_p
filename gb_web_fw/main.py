import os

from gb_web_fw.engine import Engine
from my_web_fw.main import MyWebFW
from urls import urlpatterns

settings = {
    "BASE_DIR": os.path.dirname(os.path.abspath(__file__)),
    "TEMPLATE_DIR_NAME": "templates"
}

engine = Engine()

app = MyWebFW(
    urls=urlpatterns,
    settings=settings,
    engine=engine
)

