# Dj-Flask

A simple library that allows you to write middlewares that run in Django and well as Flask.

## Setup
- Run `cd library && python setup.py bdist_wheel` to generate files required for installation
- Run `pip install -r requirements.txt` to install the library

## Running the examples
- For Django: `cd dj_sample && python manage.py runserver`
- For Flask: `cd flask_sample && python server.py`

## Example endpoints
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
