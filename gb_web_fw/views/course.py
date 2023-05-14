from gb_web_fw.my_web_fw.request import Request
from gb_web_fw.my_web_fw.response import Response
from gb_web_fw.my_web_fw.template_engine import render
from gb_web_fw.my_web_fw.view import View, Views

course = Views("Course", "/course")


@course.route("/enroll")
class Enroll(View):
    def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
        user_id = request.recognize()
        if user_id is not None:
            raw_id = request.GET.get("id")
            if raw_id:
                try:
                    _user = engine.get.student(id=int(user_id))
                    _course = engine.get.course(id=int(raw_id[0]))
                    _user.courses.setdefault(_course.id, _course)
                except Exception:
                    pass
        return Response(request, body=render(request, "courses/list.html", courses=engine.db["courses"], **kwargs))


@course.route("/list")
class List(View):
    def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
        return Response(request, body=render(request, "courses/list.html", courses=engine.db["courses"], **kwargs))


@course.route("/create")
class Create(View):
    def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
        raw_id = request.GET.get("id")
        context = {}
        if raw_id is not None:
            category = engine.get.category(id=int(raw_id[0]))
            context["name"] = category.name
        return Response(request, body=render(
            request,
            "courses/create.html",
            errors=kwargs.pop("errors", {}),
            **context,
            **kwargs
        ))

    def post(self, request: Request, engine=None, *args, **kwargs) -> Response:
        errors = {}
        context = {}
        raw_name = request.POST.get("name")
        if not raw_name:
            errors["err_name"] = "Необходимо ввести название"
        raw_start = request.POST.get("start")
        if not raw_start:
            errors["err_start"] = "Необходимо ввести дату начала"
        raw_text = request.POST.get("text")
        if not raw_text:
            errors["err_text"] = "Необходимо ввести описание"
        raw_type = request.POST.get("type")
        if not raw_type:
            errors["err_type"] = "Необходимо выбрать тип курса"
        raw_address = request.POST.get("address")
        if not raw_address:
            errors["err_address"] = "Необходимо ввести адрес проведения курса"
        if raw_text and raw_name and raw_start and raw_type and raw_address:
            additional = {"location": raw_address[0]} if raw_type[0] == "offline" else {"url": raw_address[0]}
            _course = engine.create.course(raw_type[0],
                                           name=raw_name[0],
                                           start=raw_start[0],
                                           text=raw_text[0],
                                           **additional
                                           )
            raw_id = request.GET.get("id")
            if raw_id:
                category = engine.db["categories"].get(int(raw_id[0]), None)
                if category:
                    engine.db["courses"][_course.id] = _course
                    category.courses.append(_course)
        return self.get(request, *args, **kwargs, **context, engine=engine, errors=errors)
