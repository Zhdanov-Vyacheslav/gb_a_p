from gb_web_fw.my_web_fw.request import Request
from gb_web_fw.my_web_fw.response import Response
from gb_web_fw.my_web_fw.template_engine import render
from gb_web_fw.my_web_fw.view import View


class About(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, "about.html", **kwargs)
        return Response(body=body)