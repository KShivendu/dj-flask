from json import dumps
from django.http import HttpResponseBadRequest, JsonResponse

from dj_flask.middleware import (
    BaseMiddleWare,
    CustomRequest,
    CustomNext,
    CustomResponse,
    ServerType
)


class CommonMiddleware(BaseMiddleWare):
    """
    Middleware for Django written using the dj_flask library
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ServerType.DJANGO

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

class DjangoMiddleware:
    """
    Middleware for Django written using the conventional approach 
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (request.path == "/even-or-odd" and request.method == "GET"):
            return self.get_response(request)
        try:
            num = int(request.GET.get("num"))
        except:
            return HttpResponseBadRequest('Bad request')

        return JsonResponse({"isEven": True if num % 2 == 0 else False})
