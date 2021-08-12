from django.http import HttpResponse
from django.template import loader


def user_page(request):
    message = "user page"
    return HttpResponse(message)
