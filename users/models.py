from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser

# Create your models here.

class Stores(models.Model):

    name = models.CharField(max_length=100)

class Categories(models.Model):

    name = models.CharField(max_length=100)

class Product(models.Model):

    name = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=1)
    ingredients = models.TextField()
    url = models.URLField()
    stores = models.ManyToManyField(Stores, related_name="stores", blank=True)
    categories = models.ManyToManyField(Categories, related_name="categories", blank=True)

class Favorites(models.Model):

    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('user email', unique=True)
    USERNAME_FIELD = 'email'
    favorites = models.ManyToManyField(Favorites, related_name="favorites", blank=True)


