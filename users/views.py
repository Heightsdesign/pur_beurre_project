from users.models import NewUser
from django.http import HttpResponse
from django.template import loader
from users.forms import UserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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

def subscribe_page(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data.get('first_name')
            user_name = form.cleaned_data.get('user_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            

            newuser = NewUser.objects.filter(user_name=user_name)

            if not newuser.exists():
                newuser = NewUser.objects.create(
                    first_name=first_name,
                    user_name=user_name,
                    email=email,
                    password=password
                )
            messages.success(request, f'Nouveau compt créer pour {user_name}!')
            return render(request, 'users/thank_you.html')
    else:
        form = UserCreationForm()
    context = {'form':form}

    return render(request, 'users/subscribe_form.html', context)

def connexion_page(request):

    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Utilisateur connecté: {username}!')
            
        else:
            messages.info(request, "Nom d'utilisateur ou Mot de Passe incorrect")
        
        return render(request, 'users/thank_you.html')
    #else:
        #form = LoginForm()
    context = {}

    return render(request, 'users/connexion_form.html', context)
