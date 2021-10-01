from django.http import HttpResponse
from django.template import loader
from . models import Product, Categories
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import FavoriteForm
from django.core.exceptions import ObjectDoesNotExist
from algorithm.db_and_objects.product import SubstitutesFetcher, FinalParser


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
        try:
            # title contains the query is and query is not sensitive to case.
            product_query = Product.objects.get(name=query)
            look_alikes = Product.objects.filter(name__icontains=query)
            print(product_query)
            substitutesfetcher = SubstitutesFetcher(query)
            prodselect = substitutesfetcher.get_product_substitutes_2()
            products = FinalParser(substitutesfetcher).result_parser(prodselect)
            for prod in look_alikes:
                products.append(prod)

        except ObjectDoesNotExist:
            message = messages.info(request, "Aucun produit ne correspond à votre demande")
            return render(request, 'users/thank_you.html')

            # Checks if products exists
        if len(products) == 0:

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

        context = {'products': products, 'product_query': product_query, 'form': form}

    return HttpResponse(template.render(context, request=request))
