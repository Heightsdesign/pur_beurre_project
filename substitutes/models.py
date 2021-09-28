from django.db import models
# Create your models here.


class Nutriments(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Categories(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=1)
    url = models.URLField()
    imgurl = models.URLField(null=True)
    nutriments = models.ManyToManyField(Nutriments, related_name="nutriments", blank=True)
    categories = models.ManyToManyField(Categories, related_name="categories", blank=True)
   
    def __str__(self):
        return self.name
