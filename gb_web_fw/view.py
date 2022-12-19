from datetime import datetime

from my_web_fw.view import View
from my_web_fw.request import Request
from my_web_fw.response import Response
from my_web_fw.template_engine import render


class HomePage(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        context = {}
        date = datetime.now().date()
        context.setdefault("date", date)
        body = render(request, "index.html", **context, **kwargs)
        return Response(body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        error = {}
        raw_name = request.POST.get("name")
        raw_email = request.POST.get("email")
        raw_location = request.POST.get("location")
        raw_member = request.POST.get("member")
        if raw_name and raw_email and raw_location and raw_member:
            # Данные для дальнейшего использования если пользователь все ввел
            context = {
                "name": raw_name[0],
                "email": raw_email[0],
                "location": raw_location[0],
                "member": raw_member[0]
            }
        else:
            error.setdefault("error_registration", "Не все поля заполнены")
        return self.get(request, *args, **kwargs, **error)


class About(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, "about.html", **kwargs)
        return Response(body=body)
