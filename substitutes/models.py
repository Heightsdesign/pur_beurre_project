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
    key_100g = models.TextField()
    url = models.URLField()
    imgurl = models.URLField(null=True)
    stores = models.ManyToManyField(Stores, related_name="stores", blank=True)
    categories = models.ManyToManyField(Categories, related_name="categories", blank=True)
   
    def __str__(self):
        return self.name
