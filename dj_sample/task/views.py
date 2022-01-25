from django.http import HttpResponse


def handle_even_or_odd(request):
    return HttpResponse("Hello world")

def handle_api(request):
    return HttpResponse("API response")
