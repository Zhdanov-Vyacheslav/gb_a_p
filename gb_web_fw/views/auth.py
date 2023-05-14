import hashlib
import os

import jwt

from gb_web_fw.my_web_fw.request import Request
from gb_web_fw.my_web_fw.response import Response
from gb_web_fw.my_web_fw.template_engine import render
from gb_web_fw.my_web_fw.view import View, Views

auth = Views("Auth", "/auth")


@auth.route("/login")
class Login(View):
    def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
        return Response(request, body=render(request, "auth/login.html", errors=kwargs.pop("errors", {}), **kwargs),
                        **kwargs)

    def post(self, request: Request, engine=None, *args, **kwargs) -> Response:
        cookie = {"wta": jwt.encode({"user_id": 1}, request.settings["SECRET_KEY"], algorithm="HS256")}
        return self.get(request, engine=engine, errors={}, cookie=cookie, *args, **kwargs)


@auth.route("/registration")
class Registration(View):
    def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
        return Response(
            request,
            body=render(request, "auth/registration.html", errors=kwargs.pop("errors", {})),
            cookie=kwargs.pop("cookie", {})
        )

    def post(self, request: Request, engine=None, *args, **kwargs) -> Response:
        errors = {}
        cookie = {}
        context = {}
        raw_email = request.POST.get("email")
        if not raw_email:
            errors["err_email"] = "Необходимо ввести почту"
        raw_password = request.POST.get("password")
        if not raw_password:
            errors["err_password"] = "Необходимо ввести пароль"
        raw_password2 = request.POST.get("password2")
        if not raw_password2:
            errors["err_password2"] = "Необходимо повторить пароль"
        if raw_email and raw_password and raw_password2 and raw_password[0] == raw_password2[0]:
            salt = os.urandom(16)
            passwd = hashlib.pbkdf2_hmac('sha256', raw_password[0].encode('utf-8'), salt, 100000)
            raw_refer = request.POST.get("refer")
            if raw_refer:
                _user = engine.create.user("teacher", raw_email[0], passwd, salt, raw_refer[0])
                engine.db["teachers"][_user.id] = _user
            else:
                _user = engine.create.user("student", raw_email[0], passwd, salt)
                engine.db["students"][_user.id] = _user
            cookie = {
                "wta": "; ".join([
                    "wta=" +jwt.encode({"user_id": _user.id}, request.settings["SECRET_KEY"], algorithm="HS256"),
                    "Domain="+request.settings["DOMAIN"],
                    "Path="+"/"
                ])
            }
        return self.get(request=request, *args, **kwargs, **context, engine=engine, errors=errors, cookie=cookie)


@auth.route("/logout")
class Logout(View):
    def get(self, request: Request, engine=None, *args, **kwargs) -> Response:
        request.cookie.pop("wta")
        return Response(request, body=render(request, "auth/login.html", **kwargs))
