from json import dumps
from werkzeug.wrappers import Request, Response

from dj_flask.middleware import (
    BaseMiddleWare,
    CustomRequest,
    CustomNext,
    CustomResponse,
)


class CommonMiddlware(BaseMiddleWare):
    def intercept(self, request: CustomRequest, next: CustomNext) -> CustomResponse:
        if not (request.path == "/even-or-odd" and request.method == "GET"):
            return next
        try:
            num = int(request.query["num"])
        except:
            return CustomResponse("Bad request", status=400)
        else:
            json_str = dumps({"isEven": True if num % 2 == 0 else False})
            return CustomResponse(
                json_str,
                mimetype="application/json",
                status=200,
            )


class FlaskMiddleware:
    """
    Simple Flask WSGI middleware
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        if not (request.path == "/even-or-odd" and request.method == "GET"):
            return self.app(environ, start_response)
        else:
            try:
                num = int(request.args["num"])
            except:
                res = Response(u"Bad request", mimetype="text/plain", status=400)
            else:
                json_str = dumps({"isEven": True if num % 2 == 0 else False})
                res = Response(
                    json_str,
                    mimetype="application/json",
                    status=200,
                )

            return res(environ, start_response)
