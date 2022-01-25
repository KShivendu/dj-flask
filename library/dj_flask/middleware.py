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
        self.type = (
            ServerType.FLASK
            if True # TODO: Find the best way to determine the server type (Django/Flask)
            else ServerType.DJANGO  # type(args[0]) == Flask.wsgi_app
        )

    def _get_request(self):
        if self.type == ServerType.FLASK:
            environ, start_response = self.args
            server_req = FlaskRequest(environ)
            query = server_req.args

        elif self.type == ServerType.DJANGO:
            server_req = self.args[0]
            query = server_req.GET

        request = CustomRequest(
            path=server_req.path, method=server_req.method, query=query
        )
        return request

    def _handle_next(self):
        # TODO: Think What if the request was changed by the middleware?
        return self.server_next_callback(*self.args)

    def _handle_response(self, req: CustomRequest):
        if self.type == ServerType.DJANGO:
            response = DjangoResponse(
                content=req.body, staus_code=req.status, content_type=req.mimetype
            )
            return response
        elif self.type == ServerType.FLASK:
            response = FlaskResponse(req.body, mimetype=req.mimetype, status=req.status)
            return response(*self.args)

    def __call__(self, *args, **kwargs):
        self.args = args
        request = self._get_request()
        next = CustomNext()

        middleware_res = self.intercept(request, next)

        if type(middleware_res) == CustomNext:
            return self._handle_next()
        else:
            return self._handle_response(middleware_res)

    def intercept(self, request: CustomRequest, next: CustomNext) -> CustomResponse:
        raise NotImplementedError()
