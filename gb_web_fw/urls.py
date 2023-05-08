from my_web_fw.urls import Url
from views import HomePage, About, Course, Category

urlpatterns = [
    Url("^$", HomePage),
    Url("^/about$", About),
    Url("^/course/list$", Course.List),
    Url("^/course/create$", Course.Create),
    Url("^/category/list$", Category.List),
    Url("^/category/create$", Category.Create)

]
