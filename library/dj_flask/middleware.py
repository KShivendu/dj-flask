from django.http import HttpResponse as DjangoResponse
from werkzeug.wrappers import Request as FlaskRequest, Response as FlaskResponse


class ServerType:
    DJANGO = 0
    FLASK = 1


class CustomRequest:
    def __init__(self, path, method, query) -> None:
        self.path = path
        self.method = method
        self.query = query


class CustomResponse:
    def __init__(self, body, mimetype="text/plain", status=200) -> None:
        self.body = body
        self.mimetype = mimetype
        self.status = status


class CustomNext:
    def __init__(self) -> None:
        pass


class BaseMiddleWare:
    def __init__(self, *args, **kwargs):
        self.server_next_callback = args[0]
        # Determine the server type (Django/Flask) based on the 'get_response' property
        # It's present only in case of Django.
        self.type = (
            ServerType.DJANGO
            if hasattr(self.server_next_callback, "get_response")
            else ServerType.FLASK
        )

    def _get_request(self):
        if self.type == ServerType.FLASK:
            environ, _ = self.call_args
            server_req = FlaskRequest(environ)
            query = server_req.args

        elif self.type == ServerType.DJANGO:
            server_req = self.call_args[0]
            query = server_req.GET

        request = CustomRequest(
            path=server_req.path, method=server_req.method, query=query
        )
        return request

    def _handle_next(self):
        # TODO: Think What if the request was changed by the middleware?
        return self.server_next_callback(*self.call_args)

    def _handle_response(self, req: CustomRequest):
        if self.type == ServerType.DJANGO:
            response = DjangoResponse(content=req.body, content_type=req.mimetype)
            response.status_code = req.status
            return response
        elif self.type == ServerType.FLASK:
            response = FlaskResponse(req.body, mimetype=req.mimetype, status=req.status)
            return response(*self.call_args)

    def __call__(self, *args, **kwargs):
        self.call_args = args
        request = self._get_request()
        next = CustomNext()

        middleware_res = self.intercept(request, next)

        if type(middleware_res) == CustomNext:
            return self._handle_next()
        else:
            return self._handle_response(middleware_res)

    def intercept(self, request: CustomRequest, next: CustomNext) -> CustomResponse:
        raise NotImplementedError()
