from gb_web_fw.my_web_fw.request import Request
from gb_web_fw.my_web_fw.response import Response
from gb_web_fw.my_web_fw.template_engine import render
from gb_web_fw.my_web_fw.view import View, Views

user = Views("Category", "/user")


@user.route("/student/list")
class StudentList(View):
    def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
        context = {"students": engine.db["students"]}
        return Response(request, body=render(request, "users/list.html", **context, **kwargs))