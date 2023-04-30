from datetime import datetime

from my_web_fw.view import View
from my_web_fw.request import Request
from my_web_fw.response import Response
from my_web_fw.template_engine import render


class HomePage(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, "index.html", **kwargs)
        return Response(body=body)


class About(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = "Good info about this site"
        info = request.GET.get("info")
        if info:
            body += "\nВаше info={info}".format(info=info)
        time = request.GET.get("time")
        if time:
            body += "\nТекущее время: {time}".format(time=datetime.now().time().isoformat(timespec="seconds"))
        return Response(body=body)


class TestTemplate(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(body="Пустая страница, без html шаблона")
