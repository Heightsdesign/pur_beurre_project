from users.models import NewUser
from django.http import HttpResponse
from django.template import loader
from . models import NewUser, CustomAccountManager
from substitutes.models import Product

def user_page(request, user_id):
    template = loader.get_template('users/index.html')
    user = NewUser.objects.get(pk=user_id)
    context = {'user': user}
    return HttpResponse(template.render(context, request=request))

def favorites_page(request):
    query = request.GET.get('query')
    template = loader.get_template('users/favorites.html')
    user = NewUser.objects.filter(id__icontains=query)

    if not user.exists():
        message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    else:
        user_favorites = Product.objects.filter(favorites__id__icontains=query)
        context = {'user':user, 'user_favorites':user_favorites}

    return HttpResponse(template.render(context, request=request))
