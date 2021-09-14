from django.http import HttpResponse
from django.template import loader
from . models import Product, Categories
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from users.models import User


def index(request):

    template = loader.get_template('substitutes/index.html')
    return HttpResponse(template.render(request=request))


def listing(request):

    products = ["<li>{}</li>".format(product['name']) for product in Product]
    message = """<ul>{}</ul>""".format("\n".join(products))
    return HttpResponse(message)


def product_detail(request, product_id):

    template = loader.get_template('substitutes/product.html')
    product = get_object_or_404(Product, pk=product_id)
    categories = " ".join([category.name for category in product.categories.all()])
    context = {'product':product, 'categories':categories}
    return HttpResponse(template.render(context, request=request))


def search(request):

    if request.user.is_authenticated and request.method == 'POST':
        user = request.user.id
        product = request.POST['product']
        #add product to user favorites and return success page

    else:
        query = request.GET.get('query')
        template = loader.get_template('substitutes/list.html')
        error_template = loader.get_template('404.html')
        if not query:
            products = Product.objects.all()
        else:
            # title contains the query is and query is not sensitive to case.
            products = Product.objects.filter(name__icontains=query)

            if not products.exists():

                context = {}
                return HttpResponse(error_template.render(context, request=request))

            else:
                products_categories = Categories.objects.filter(categories__name__icontains=query)
                context = {'products':products, 'products_categories':products_categories}

    return HttpResponse(template.render(context, request=request))
