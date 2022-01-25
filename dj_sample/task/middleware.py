from json import dumps
from django.http import HttpResponseBadRequest, JsonResponse

from dj_flask.middleware import (
    BaseMiddleWare,
    CustomRequest,
    CustomNext,
    CustomResponse,
)


class CommonMiddlware(BaseMiddleWare):
    def intercept(self, request: CustomRequest, next: CustomNext) -> CustomResponse:
        if not (request.path != "/even-or-odd" and request.method == "GET"):
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

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if not (request.path == "/even-or-odd" and request.method == "GET"):
            return self.get_response(request)
        try:
            num = int(request.GET.get("num"))
        except:
            return HttpResponseBadRequest()

        return JsonResponse({"isEven": True if num % 2 == 0 else False})
