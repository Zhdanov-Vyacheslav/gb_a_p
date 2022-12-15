from my_web_fw.urls import Url
from view import HomePage, About, TestTemplate

urlpatterns = [
    Url("^$", HomePage),
    Url("^/about$", About),
    Url("^/test$", TestTemplate)
]
