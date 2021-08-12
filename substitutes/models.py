from django.db import models
# Create your models here.

class Stores(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Categories(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=1)
    ingredients = models.TextField()
    url = models.URLField()
    stores = models.ManyToManyField(Stores, related_name="stores", blank=True)
    categories = models.ManyToManyField(Categories, related_name="categories", blank=True)

    def __str__(self):
        return self.name

class Favorites(models.Model):

    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.idProduct