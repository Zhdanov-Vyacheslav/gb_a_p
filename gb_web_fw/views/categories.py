from gb_web_fw.my_web_fw.request import Request
from gb_web_fw.my_web_fw.response import Response
from gb_web_fw.my_web_fw.template_engine import render
from gb_web_fw.my_web_fw.view import View


# Вложенность исключительно для удобства
class Category:
    class List(View):
        def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
            context = {}
            context["categories"] = engine.db["categories"]
            return Response(body=render(request, "categories/list.html", **context, **kwargs))

    class Create(View):
        def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
            return Response(body=render(request, "categories/create.html", errors=kwargs.pop("errors", {}), **kwargs))

        def post(self, request: Request, engine=None, *args, **kwargs) -> Response:
            errors = {}
            context = {}
            raw_name = request.POST.get("name")
            if not raw_name:
                errors["err_name"] = "Необходимо ввести название"
            if raw_name:
                category = engine.create.category(name=raw_name[0])
                engine.db["categories"][category.id] = category
            return self.get(request, *args, **kwargs, **context, engine=engine, errors=errors)
