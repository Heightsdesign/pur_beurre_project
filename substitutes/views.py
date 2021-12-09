from django.http import HttpResponse
from django.template import loader
from .models import Product, Query
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import FavoriteForm
from django.core.exceptions import ObjectDoesNotExist
from algorithm.db_and_objects.product import SubstitutesFetcher, FinalParser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0

def index(request):

    template = loader.get_template("substitutes/index.html")
    return HttpResponse(template.render(request=request))


def product_detail(request, product_id):

    template = loader.get_template("substitutes/product.html")
    product = get_object_or_404(Product, pk=product_id)
    nutriments = product.nutriments.exclude(value=0)
    context = {"product": product, "nutriments": nutriments}
    return HttpResponse(template.render(context, request=request))


def legal_mentions(request):

    template = loader.get_template("substitutes/legal.html")
    return HttpResponse(template.render(request=request))


def search(request):

    # gets the query
    query = request.GET.get("query")

    if query:
        try:
            db_query = Query(name=query)
            db_query.save()
            # title contains the query is and query is not sensitive to case.
            product_query = Product.objects.get(name=query)
            look_alikes = Product.objects.filter(name__icontains=query)
            substitutesfetcher = SubstitutesFetcher(query)
            prodselect = substitutesfetcher.get_product_substitutes_2()
            product_list = FinalParser(
                substitutesfetcher).result_parser(prodselect)

            for prod in look_alikes:
                product_list.append(prod)

            paginator = Paginator(product_list, 6)
            page_num = request.GET.get("page")

            try:
                products = paginator.get_page(page_num)

            except PageNotAnInteger:
                products = paginator.get_page(1)

        except ObjectDoesNotExist:

            messages.info(request, "Pas de produits correspondants !")
            return render(request, "substitutes/no_product.html")

    else:
        db_query = Query.objects.latest('time')
        query = db_query.name

        product_query = Product.objects.get(name=query)
        look_alikes = Product.objects.filter(name__icontains=query)
        substitutesfetcher = SubstitutesFetcher(query)
        prodselect = substitutesfetcher.get_product_substitutes_2()
        product_list = FinalParser(
            substitutesfetcher).result_parser(prodselect)

        for prod in look_alikes:
            product_list.append(prod)

        paginator = Paginator(product_list, 6)
        page_num = request.GET.get("page")

        try:
            products = paginator.get_page(page_num)

        except PageNotAnInteger:
            products = paginator.get_page(1)

        except EmptyPage:
            products = paginator.page(paginator.num_pages)

    if request.method == "POST":

        form = FavoriteForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            user = request.user
            product_id = form.cleaned_data.get("product_id")
            product = Product.objects.get(id=product_id)
            user.favorites.add(product)
            messages.success(
                request, f"{product} Ajouter aux favoris !"
            )

        else:
            messages.info(request, f"Veuillez vous connecter !")

        return render(request, "substitutes/product_added.html")

    else:
        form = FavoriteForm()

    context = {
        "product_query": product_query,
        "products": products,
        "form": form,
        "paginate": True,
    }

    return render(request, "substitutes/list.html", context)
