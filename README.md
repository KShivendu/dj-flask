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
    - Returns `{"isEven": true}` because num is even
2. http://localhost:8000/even-or-odd?num=23
    - Returns `{"isEven": true}` because num is odd
3. http://localhost:8000/even-or-odd
    - Returns Bad request (400) because num wasn't passed.
4. http://localhost:8000/hello (Middleware passes it to the controller.)
    - The controller returns "Hello world" because the middleware passed the request.
