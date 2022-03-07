# Dj-Flask

A simple library that allows you to write middlewares that run in Django and well as Flask.

## Setup
- Run `cd library && python setup.py bdist_wheel` to generate files required for installation
- Run `pip install -r requirements.txt` to install the library

## Running the examples
- For Django: `cd dj_sample && python manage.py runserver`
- For Flask: `cd flask_sample && python server.py`

## Example

```python
# middleware.py

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
```

### For Django:
```python
# examples/django/app/settings.py

MIDDLEWARE = [
    'task.middleware.CommonMiddleware',
    '...'
]
```

### For Flask:
```python
# examples/flask/server.py

from middleware import CommonMiddlware
from flask import Flask

app = Flask('DemoApp')

app.wsgi_app = CommonMiddlware(app.wsgi_app)
```

### Endpoints

1. http://localhost:8000/even-or-odd?num=22
    - The middleware returns `{"isEven": true}` because num is even
2. http://localhost:8000/even-or-odd?num=23
    - The middleware returns `{"isEven": true}` because num is odd
2. http://localhost:8000/even-or-odd?num=foo
    - The middleware returns Bad request (400) because num is not an integer.
3. http://localhost:8000/even-or-odd
    - The middleware returns Bad request (400) because num is missing.
4. http://localhost:8000/hello (Middleware passes it to the controller.)
    - The controller returns "Hello world" because the middleware passed the request.
