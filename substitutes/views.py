from django.http import HttpResponse
from django.template import loader
from . models import Product, Categories
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import FavoriteForm


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

            if request.method == 'POST':

                form = FavoriteForm(request.POST)

                if form.is_valid() and request.user.is_authenticated:
                    user = request.user
                    product_id = form.cleaned_data.get("product_id")
                    product = Product.objects.get(id=product_id)
                    user.favorites.add(product)
                    messages.success(request, f'{product} Ajouter aux favoris !')

                else:
                    messages.info(request, f'Veuillez vous connecter !')

                return render(request, 'users/thank_you.html')

            else:
                form = FavoriteForm()

            context = {'products': products, 'products_categories': products_categories, 'form': form}

    return HttpResponse(template.render(context, request=request))
