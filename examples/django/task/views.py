from django.http import HttpResponse


def even_or_odd(request):
    return HttpResponse("Middleware didn't work. This response was sent by the controller")

def greet(request):
    return HttpResponse("Hello world")
