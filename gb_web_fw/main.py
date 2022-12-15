import os

from my_web_fw.main import MyWebFW
from urls import urlpatterns

settings = {
    "BASE_DIR": os.path.dirname(os.path.abspath(__file__)),
    "TEMPLATE_DIR_NAME": "templates"
}

app = MyWebFW(
    urls=urlpatterns,
    settings=settings
)

