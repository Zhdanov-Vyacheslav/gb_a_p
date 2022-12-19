from my_web_fw.urls import Url
from view import HomePage, About, Feedback

urlpatterns = [
    Url("^$", HomePage),
    Url("^/about$", About),
    Url("/feedback", Feedback)
]
