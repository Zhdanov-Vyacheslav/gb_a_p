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

    def post(self, request: Request, *args, **kwargs) -> Response:
        errors = {}
        context = {}
        raw_email = request.POST.get("email")
        if not raw_email:
            errors.setdefault("err_email", "Необходимо ввести email")
        raw_comment = request.POST.get("comment")
        if not raw_comment:
            errors.setdefault("err_comment", "Необходимо ввести текст")
        if raw_comment and raw_email:
            context = {
                "message": "Спасибо за отзыв. Вы оставили отзыв c текстом: " \
                           "<p>{comment}</p>" \
                           "<p>Ваша почта: {email}</p>".format(comment=raw_comment[0], email=raw_email[0])
            }
            # Данные для вывода в консоль по пункту 4 дз урока 2
            print(context)
            # ///
        return self.get(request, *args, **kwargs, **errors, **context)
