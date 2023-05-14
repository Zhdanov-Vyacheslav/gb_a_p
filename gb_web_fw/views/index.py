from datetime import datetime

from gb_web_fw.my_web_fw.request import Request
from gb_web_fw.my_web_fw.response import Response
from gb_web_fw.my_web_fw.template_engine import render
from gb_web_fw.my_web_fw.view import View, Views

index = Views("HomePage", "/")


@index.route("/")
class HomePage(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        context = {}
        date = datetime.now().date()
        context.setdefault("date", date)
        body = render(request, "index.html", **context, **kwargs)
        return Response(body=body)

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
