from datetime import datetime

from my_web_fw.view import View
from my_web_fw.request import Request
from my_web_fw.response import Response
from my_web_fw.template_engine import render


class HomePage(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, "index.html", **kwargs)
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
        # Данные для вывода в консоль по пункту 4 дз урока 2
        for_question = {
            "name": raw_name[0] if raw_name else raw_name,
            "email": raw_email[0] if raw_email else raw_email,
            "location": raw_location[0] if raw_location else raw_location,
            "member": raw_member[0] if raw_member else raw_member
        }
        print(for_question)
        # ///
        body = render(request, "index.html", **error, **kwargs)
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
