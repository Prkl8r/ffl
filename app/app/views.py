from django.http import HttpResponse


def index(request):
    variable = "My Variable"
    return HttpResponse('Hello World!')