from django.http import HttpResponse
from django.template import loader
from users.forms import UserCreationForm
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import User
from substitutes.models import Product


def user_page(request, user_id):

    template = loader.get_template("users/index.html")
    user = User.objects.get(pk=user_id)
    context = {"user": user}
    return HttpResponse(template.render(context, request=request))


def favorites_page(request, user_id):

    template = loader.get_template("users/favorites.html")

    if request.user.is_authenticated and user_id is not None:

        user = request.user
        user_id = user.id
        user_favorites = Product.objects.filter(
            favorites__id__icontains=user_id
        )
        context = {"user": user, "user_favorites": user_favorites}

    return HttpResponse(template.render(context, request=request))


def subscribe_page(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            first_name = form.cleaned_data.get("first_name")

            user = User.objects.filter(email=email)

            if not user.exists():
                user = User.objects.create_user(
                    email=email, password=password, first_name=first_name
                )
                message = messages.success(
                    request, f"Nouveau compte crée pour {email}!"
                )
                success = True
                context = {"success": success}

            else:
                message = messages.info(request, "Ce compte existe déjà")

            return render(request, "users/thank_you.html", context)
    else:
        form = UserCreationForm()
    context = {"form": form}

    return render(request, "users/subscribe_form.html", context)


def connexion_page(request):

    if request.method == "POST":

        username = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Utilisateur connecté: {username}!")

        else:
            messages.info(
                request,
                "Nom d'utilisateur ou Mot de Passe incorrect"
            )

        return render(request, "users/thank_you.html")

    return render(request, "users/connexion_form.html")


def logout_view(request):

    logout(request)
    messages.success(request, "Utilisateur déconnecté!")
    return render(request, "users/logout.html")
