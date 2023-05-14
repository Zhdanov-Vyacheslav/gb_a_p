import os

from gb_web_fw.engine import Engine
from my_web_fw.main import MyWebFW
from views import views

settings = {
    "BASE_DIR": os.path.dirname(os.path.abspath(__file__)),
    "TEMPLATE_DIR_NAME": "templates"
}

engine = Engine()

app = MyWebFW(
    views=views,
    settings=settings,
    engine=engine
)
