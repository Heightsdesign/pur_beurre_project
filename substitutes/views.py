from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('substitutes/index.html')
    return HttpResponse(template.render(request=request))

def search(request):
    obj = str(request.GET)
    query = request.GET['query']
    message = "propriété GET : {} et requête : {}".format(obj, query)
    return HttpResponse(message)

def product_detail(request, product_id):
    template = loader.get_template('substitutes/product.html')
    id = int(product_id) # make sure we have an integer.
    message = "L'id du produit est : {}".format(id)
    return HttpResponse(template.render(request=request))
