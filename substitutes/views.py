from django.http import HttpResponse
from django.template import loader
from . models import Product, Categories
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import FavoriteForm


def index(request):

    template = loader.get_template('substitutes/index.html')
    return HttpResponse(template.render(request=request))


def product_detail(request, product_id):

    template = loader.get_template('substitutes/product.html')
    product = get_object_or_404(Product, pk=product_id)
    categories = " ".join([category.name for category in product.categories.all()])
    context = {'product': product, 'categories': categories}
    return HttpResponse(template.render(context, request=request))


def search(request):

    # gets the query
    query = request.GET.get('query')

    # loads the template list.html
    template = loader.get_template('substitutes/list.html')
    # loads error template
    error_template = loader.get_template('404.html')

    # Checks if there is a query
    if not query:
        # Gets all products
        products = Product.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        products = Product.objects.filter(name__icontains=query)

        # Checks if products exists
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
                    message = messages.success(request, f'{product} Ajouter aux favoris !')

                else:
                    message = messages.info(request, f'Veuillez vous connecter !')

                return render(request, 'users/thank_you.html')

            else:
                form = FavoriteForm()

        context = {'products': products, 'products_categories': products_categories, 'form': form}

    return HttpResponse(template.render(context, request=request))
