from django.http import HttpResponse
from django.template import loader
from . models import Product, Stores, Categories

def index(request):
    template = loader.get_template('substitutes/index.html')
    return HttpResponse(template.render(request=request))

def listing(request):
    products = ["<li>{}</li>".format(product['name']) for product in Product]
    message = """<ul>{}</ul>""".format("\n".join(products))
    return HttpResponse(message)

def product_detail(request, product_id):
    template = loader.get_template('substitutes/product.html')
    product = Product.objects.get(pk=product_id)
    categories = " ".join([category.name for category in product.categories.all()])
    message = """Le nom du produit est {},
    Son nutriscore est : {},
    Son Repère nutritionnel est : {},
    Ses categories sont :  {}.""".format(product.name, product.key_100g, product.nutriscore, categories)
    return HttpResponse(message)

def search(request):
    query = request.GET.get('query')
    if not query:
        products = Product.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        products = Product.objects.filter(name__icontains=query)

    if not products.exists():
        products = Product.objects.filter(products__name__icontains=query)

    if not products.exists():
        message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    else:
        products_names = ["<li>{}</li>".format(product.name) for product in products]
        nutriscores = ["<li>{}</li>".format(product.nutriscore) for product in products]
        products_categories = Categories.objects.filter(categories__name__icontains=query)
        categories = ["<li>{}</li>".format(category.name) for category in products_categories]
        message = """
            Nous avons trouvé les produits correspondant à votre requête ! Les voici :
            <ul>{}</ul>
            Voici leur nutriscore
            <ul>{}</ul>
            Voici leur catégories
            <ul>{}</ul>
        """.format("</li><li>".join(products_names), "</li><li>".join(nutriscores), "</li><li>".join(categories))

    return HttpResponse(message)
