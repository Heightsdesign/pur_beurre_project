from django.http import HttpResponse
from django.template import loader


def user_page(request):
    template = loader.get_template('substitutes/index.html')
    return HttpResponse(template.render(request=request))
