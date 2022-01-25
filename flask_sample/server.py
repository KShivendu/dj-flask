from dj_flask.middleware import BaseMiddleWare

# from .middleware import FlaskMiddleware
from flask import Flask

app = Flask('DemoApp')

# calling our middleware
app.wsgi_app = CommonMiddleWare(app.wsgi_app)

@app.route('/even-or-odd', methods=['GET', 'POST'])
def even_or_odd():
    return "Middleware didn't work. This response was sent by the controller"


@app.route('/hello', methods=['GET', 'POST'])
def greet():
    return "Hello world"

if __name__ == "__main__":
    app.run('127.0.0.1', '5000', debug=True)