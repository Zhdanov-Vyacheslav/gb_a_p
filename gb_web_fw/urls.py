from my_web_fw.urls import Url
from view import HomePage, About

urlpatterns = [
    Url("^$", HomePage),
    Url("^/about$", About),
]
